# Copyright 2016 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from unittest import mock

from neutron_lib.callbacks import events
from neutron_lib.callbacks import priority_group
from neutron_lib.callbacks import resources
from neutron_lib import fixture

from neutron.api.rpc.callbacks import resource_manager
from neutron.services.trunk.rpc import backend
from neutron.tests import base


class ServerSideRpcBackendTest(base.BaseTestCase):
    # TODO(fitoduarte): add more test to improve coverage of module
    def setUp(self):
        super().setUp()
        self._mgr = mock.Mock()
        self.useFixture(fixture.CallbackRegistryFixture(
            callback_manager=self._mgr))
        self.register_mock = mock.patch.object(
            resource_manager.ResourceCallbacksManager, "register").start()

    def test___init__(self,):
        test_obj = backend.ServerSideRpcBackend()

        calls = [mock.call(
                    test_obj.process_event,
                    resources.TRUNK,
                    events.AFTER_CREATE,
                    priority_group.PRIORITY_DEFAULT,
                    False),
                 mock.call(
                    test_obj.process_event,
                    resources.TRUNK,
                    events.AFTER_DELETE,
                    priority_group.PRIORITY_DEFAULT,
                    False),
                 mock.call(
                    test_obj.process_event,
                    resources.SUBPORTS,
                    events.AFTER_CREATE,
                    priority_group.PRIORITY_DEFAULT,
                    False),
                 mock.call(
                    test_obj.process_event,
                    resources.SUBPORTS,
                    events.AFTER_DELETE,
                    priority_group.PRIORITY_DEFAULT,
                    False),
                 ]
        self._mgr.subscribe.assert_has_calls(calls, any_order=True)

    def test_process_event(self):
        test_obj = backend.ServerSideRpcBackend()
        test_obj._stub = mock_stub = mock.Mock()
        trunk_plugin = mock.Mock()

        test_obj.process_event(
            resources.TRUNK, events.AFTER_CREATE, trunk_plugin,
            events.DBEventPayload("context",
                                  resource_id="id",
                                  states=("current_trunk",)))

        test_obj.process_event(
            resources.TRUNK, events.AFTER_DELETE, trunk_plugin,
            events.DBEventPayload("context",
                                  resource_id="id",
                                  states=("original_trunk",)))

        calls = [mock.call.trunk_created("context",
                                         "current_trunk"),
                 mock.call.trunk_deleted("context",
                                         "original_trunk")]
        mock_stub.assert_has_calls(calls, any_order=False)
