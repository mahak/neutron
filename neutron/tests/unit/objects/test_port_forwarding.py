# Copyright (c) 2018 OpenStack Foundation.
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

import netaddr
from oslo_utils import uuidutils

from neutron.objects import port_forwarding
from neutron.objects import router
from neutron.tests import tools
from neutron.tests.unit.objects import test_base as obj_test_base
from neutron.tests.unit import testlib_api


class PortForwardingObjectTestCase(obj_test_base.BaseObjectIfaceTestCase):

    _test_class = port_forwarding.PortForwarding

    def setUp(self):
        super().setUp()
        # 'portforwardings' table will store the 'internal_ip_address' and
        # 'internal_port' as a single 'socket' column.
        # Port forwarding object accepts 'internal_ip_address' and
        # 'internal_port', but can not filter the records in db, so the
        # valid filters can not contain them.
        not_supported_filter_fields = ['internal_ip_address', 'internal_port']
        invalid_fields = set(
            self._test_class.synthetic_fields).union(
            set(not_supported_filter_fields))
        self.valid_field = [f for f in self._test_class.fields
                            if f not in invalid_fields][0]

        self.mock_load_fip = mock.patch.object(
            self._test_class, '_load_attr_from_fip', autospec=True,
            side_effect=self._mock_load_attr_from_fip).start()

        for obj_fields in self.obj_fields:
            obj_fields['floating_ip_address'] = tools.get_random_ip_address(4)
            obj_fields['router_id'] = uuidutils.generate_uuid()

    def _mock_load_attr_from_fip(self, fp_obj, attrname):
        def random_generate_fip_db(fip_id):
            fip_fields = self.get_random_db_fields(router.FloatingIP)
            fip_fields['id'] = fip_id
            fip_fields['floating_ip_address'] = tools.get_random_ip_address(4)
            return router.FloatingIP.db_model(**fip_fields)

        if not fp_obj.db_obj:
            fp_db_attrs = {
                'floatingip_id': fp_obj.floatingip_id,
                'external_port_start': fp_obj.external_port,
                'external_port_end': fp_obj.external_port,
                'internal_neutron_port_id': fp_obj.internal_port_id,
                'protocol': fp_obj.protocol,
                'internal_port_start': fp_obj.internal_port,
                'internal_port_end': fp_obj.internal_port,
                'floating_ip': random_generate_fip_db(fp_obj.floatingip_id)
            }
            fp_obj._captured_db_model = (
                port_forwarding.PortForwarding.db_model(**fp_db_attrs))

        if not fp_obj.db_obj.floating_ip:
            fp_obj.db_obj.floating_ip = random_generate_fip_db(
                fp_obj.floatingip_id)

        # From PortForwarding._load_attr_from_fip
        value = getattr(fp_obj.db_obj.floating_ip, attrname)
        setattr(self, attrname, value)
        fp_obj.obj_reset_changes([attrname])


class PortForwardingDbObjectTestCase(obj_test_base.BaseDbObjectTestCase,
                                     testlib_api.SqlTestCase):

    _test_class = port_forwarding.PortForwarding

    def setUp(self):
        super().setUp()
        self.update_obj_fields(
            {'floatingip_id':
                lambda: self._create_test_fip_id_for_port_forwarding(),
             'internal_port_id': lambda: self._create_test_port_id()})
        # 'portforwardings' table will store the 'internal_ip_address' and
        # 'internal_port' as a single 'socket' column.
        # Port forwarding object accepts 'internal_ip_address' and
        # 'internal_port', but can not filter the records in db, so the
        # valid filters can not contain them.
        not_supported_filter_fields = ['internal_ip_address', 'internal_port']
        invalid_fields = set(
            self._test_class.synthetic_fields).union(
            set(not_supported_filter_fields))
        self.valid_field = [f for f in self._test_class.fields
                            if f not in invalid_fields][0]
        self.valid_field_filter = {self.valid_field:
                                   self.obj_fields[-1][self.valid_field]}

    def _create_test_fip_id_for_port_forwarding(self):
        fake_fip = '172.23.3.0'
        ext_net_id = self._create_external_network_id()
        router_id = self._create_test_router_id()
        values = {
            'floating_ip_address': netaddr.IPAddress(fake_fip),
            'floating_network_id': ext_net_id,
            'floating_port_id': self._create_test_port_id(
                network_id=ext_net_id),
            'router_id': router_id,
        }
        fip_obj = router.FloatingIP(self.context, **values)
        fip_obj.create()
        return fip_obj.id

    def test_db_obj(self):
        # The reason for rewriting this test is:
        # 1. Currently, the existing test_db_obj test in
        #    obj_test_base.BaseDbObjectTestCase is not suitable for the case,
        #    for example, the db model is not the same with obj fields
        #    definition.
        # 2. For port forwarding, the db model will store and accept 'socket',
        #    but the obj fields just only support accepting the parameters
        #    generate 'socket', such as 'internal_ip_address' and
        #    'internal_port'.
        obj = self._make_object(self.obj_fields[0])
        self.assertIsNone(obj.db_obj)

        obj.create()
        self.assertIsNotNone(obj.db_obj)

        fields_to_update = self.get_updatable_fields(self.obj_fields[1])
        if fields_to_update:
            old_fields = {}
            for key, val in fields_to_update.items():
                db_model_attr = (
                    obj.fields_need_translation.get(key, key))

                old_fields[db_model_attr] = obj.db_obj[
                    db_model_attr] if hasattr(
                    obj.db_obj, db_model_attr) else getattr(
                    obj, db_model_attr)
                setattr(obj, key, val)
            obj.update()
            self.assertIsNotNone(obj.db_obj)
            # Then check all update fields had been updated.
            for k, v in obj.modify_fields_to_db(fields_to_update).items():
                self.assertEqual(v, obj.db_obj[k], '%s attribute differs' % k)

        obj.delete()
        self.assertIsNone(obj.db_obj)

    def test_get_objects_queries_constant(self):
        # NOTE(bzhao) Port Forwarding uses query FLoatingIP for injecting
        # floating_ip_address and router_id, not depends on relationship,
        # so it will cost extra SQL query each time for finding the
        # associated Floating IP by floatingip_id each time(or each
        # Port Forwarding Object). Rework this if this customized OVO
        # needs to be changed.
        pass
