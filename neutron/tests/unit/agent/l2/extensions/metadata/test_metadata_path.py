# Copyright (c) 2023 China Unicom Cloud Data Co.,Ltd.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from unittest import mock

from neutron_lib import context
from oslo_config import cfg

from neutron.agent.common import ovs_lib
from neutron.agent.l2.extensions.metadata import metadata_path
from neutron.api.rpc.callbacks import resources
from neutron.conf.plugins.ml2.drivers import ovs_conf
from neutron.plugins.ml2.drivers.openvswitch.agent \
    import ovs_agent_extension_api as ovs_ext_api
from neutron.tests import base


class MetadataPathAgentExtensionTestCase(base.BaseTestCase):

    def setUp(self):
        super(MetadataPathAgentExtensionTestCase, self).setUp()
        ovs_conf.register_ovs_agent_opts(cfg=cfg.CONF)
        cfg.CONF.set_override('provider_cidr', '240.0.0.0/31', 'METADATA')
        self.context = context.get_admin_context()
        self.int_br = mock.Mock()
        self.meta_br = mock.Mock()
        self.plugin_rpc = mock.Mock()
        self.remote_resource_cache = mock.Mock()
        self.plugin_rpc.remote_resource_cache = self.remote_resource_cache
        self.meta_ext = metadata_path.MetadataPathAgentExtension()
        self.bridge_mappings = {"meta": "br-meta"}
        self.int_ofport = 200
        self.phys_ofport = 100
        self.agent_api = ovs_ext_api.OVSAgentExtensionAPI(
            self.int_br,
            tun_br=mock.Mock(),
            phys_brs={"meta": self.meta_br},
            plugin_rpc=self.plugin_rpc,
            phys_ofports={"meta": self.phys_ofport},
            bridge_mappings=self.bridge_mappings)
        self.meta_ext.consume_api(self.agent_api)
        mock.patch(
            "neutron.agent.linux.ip_lib.IpLinkCommand.set_address").start()
        mock.patch(
            "neutron.agent.linux.ip_lib.IpAddrCommand.add").start()
        mock.patch(
            "neutron.agent.linux.ip_lib.IpLinkCommand.set_up").start()
        self.meta_ext._set_port_vlan = mock.Mock()
        self.meta_ext.initialize(None, None)
        # set int_br back to mock
        self.meta_ext.int_br = self.int_br
        # set meta_br back to mock
        self.meta_ext.meta_br = self.meta_br
        self.get_port_ofport = mock.patch.object(
            self.int_br, 'get_port_ofport',
            return_value=self.int_ofport).start()

        self.meta_daemon = mock.Mock()
        self.meta_ext.meta_daemon = mock.Mock()

        self.port_provider_ip = "100.100.100.100"
        self.port_provider_mac = "fa:16:ee:11:22:33"

        def m_get_value_from_ovsdb_other_config(p, key, value_type=None):
            if key == "provider_ip":
                return self.port_provider_ip
            if key == "provider_mac":
                return self.port_provider_mac

        mock.patch.object(
            self.int_br, 'get_value_from_other_config',
            side_effect=m_get_value_from_ovsdb_other_config).start()
        mock.patch.object(
            self.int_br, 'set_value_to_other_config').start()

        mock.patch.object(
            self.meta_br, 'set_value_to_other_config').start()

    def test_handle_port(self):
        port_mac_address = "aa:aa:aa:aa:aa:aa"
        port_name = "tap-p1"
        port_id = "p1"
        port_ofport = 1
        port_device_owner = "compute:test"
        with mock.patch.object(self.meta_ext.meta_daemon,
                 "config") as h_config, mock.patch.object(
                     self.meta_ext.ext_api,
                     "get_provider_ip_info") as get_p_info:
            get_p_info.return_value = {
                'instance_id': 'instance_uuid_1',
                'project_id': 'project_id_1',
                'provider_ip': self.port_provider_ip,
                'provider_port_mac': self.port_provider_mac
            }

            port = {"port_id": port_id,
                    "fixed_ips": [{"ip_address": "1.1.1.1",
                                   "subnet_id": "1"}],
                    "vif_port": ovs_lib.VifPort(port_name, port_ofport,
                                                port_id,
                                                port_mac_address, "br-int"),
                    "device_owner": port_device_owner,
                    "network_id": "net_id_1",
                    "mac_address": port_mac_address}
            self.meta_ext.handle_port(self.context, port)

            get_p_info.assert_called_once_with(
                port['port_id'],
                self.port_provider_ip,
                self.port_provider_mac)
            h_config.assert_called_once_with(
                list(self.meta_ext.instance_infos.values()))

    def test_get_port_no_more_provider_ip(self):

        def m_get_value_from_ovsdb_other_config(p, key, value_type=None):
            if key == "provider_ip":
                return
            if key == "provider_mac":
                return

        mock.patch.object(
            self.int_br, 'get_value_from_other_config',
            side_effect=m_get_value_from_ovsdb_other_config).start()
        mock.patch.object(
            self.int_br, 'set_value_to_other_config').start()

        port_device_owner = "compute:test"

        class Port(object):
            def __init__(self):
                self.device_id = "d1"
                self.project_id = "p1"

        with mock.patch.object(self.meta_ext.meta_daemon,
                 "config"), mock.patch.object(
                     self.meta_ext.ext_api.cache_api,
                     "get_resource_by_id",
                     return_value=Port()) as get_res:
            port1_mac_address = "aa:aa:aa:aa:aa:aa"
            port1_name = "tap-p1"
            port1_id = "p1"
            port1_ofport = 1
            port1 = {"port_id": port1_id,
                     "fixed_ips": [{"ip_address": "1.1.1.1",
                                    "subnet_id": "1"}],
                     "vif_port": ovs_lib.VifPort(port1_name, port1_ofport,
                                                 port1_id,
                                                 port1_mac_address, "br-int"),
                     "device_owner": port_device_owner,
                     "network_id": "net_id_1",
                     "mac_address": port1_mac_address}
            self.meta_ext.handle_port(self.context, port1)

            get_res.assert_called_once_with(
                resources.PORT,
                port1['port_id'])

            port2_id = "p2"
            self.assertRaises(
                metadata_path.NoMoreProviderRes,
                self.meta_ext.ext_api.get_provider_ip_info,
                port2_id, None, None)

    def test_delete_port(self):
        port_mac_address = "aa:aa:aa:aa:aa:aa"
        port_name = "tap-p1"
        port_id = "p1"
        port_ofport = 1
        port_device_owner = "compute:test"
        with mock.patch.object(self.meta_ext.meta_daemon,
                 "config") as h_config:
            port = {"port_id": port_id,
                    "fixed_ips": [{"ip_address": "1.1.1.1",
                                   "subnet_id": "1"}],
                    "vif_port": ovs_lib.VifPort(port_name, port_ofport,
                                                port_id,
                                                port_mac_address, "br-int"),
                    "device_owner": port_device_owner,
                    "network_id": "net_id_1",
                    "mac_address": port_mac_address}
            self.meta_ext.handle_port(self.context, port)
            instance_info_values = list(self.meta_ext.instance_infos.values())

            self.meta_ext.delete_port(self.context, {"port_id": port_id})
            h_config.assert_has_calls([mock.call(instance_info_values),
                                       mock.call([])])
            self.assertNotIn(self.port_provider_ip,
                             self.meta_ext.ext_api.allocated_ips)
            self.assertNotIn(self.port_provider_mac,
                             self.meta_ext.ext_api.allocated_macs)
