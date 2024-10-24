#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from neutron.tests import base

from neutron.privileged.agent.ovsdb.native import helpers


class OvsdbNativeHelpersTestCase(base.BaseTestCase):

    def test__connect_to_manager_uri_ipv4(self):
        self.assertEqual(
            'ptcp:6640:127.0.0.1',
            helpers._connection_to_manager_uri('tcp:127.0.0.1:6640'))
        self.assertEqual(
            'ptls:6640:127.0.0.1',
            helpers._connection_to_manager_uri('tls:127.0.0.1:6640'))
        self.assertEqual(
            'ptcp:127.0.0.1',
            helpers._connection_to_manager_uri('tcp:127.0.0.1'))

    def test__connect_to_manager_uri_ipv6(self):
        self.assertEqual(
            'ptcp:6640:[::1]',
            helpers._connection_to_manager_uri('tcp:[::1]:6640'))
        self.assertEqual(
            'ptls:6640:[::1]',
            helpers._connection_to_manager_uri('tls:[::1]:6640'))
        self.assertEqual(
            'ptcp:[::1]',
            helpers._connection_to_manager_uri('tcp:[::1]'))

    def test__connect_to_manager_uri_hostname(self):
        self.assertEqual(
            'ptcp:6640:localhost',
            helpers._connection_to_manager_uri('tcp:localhost:6640'))
        self.assertEqual(
            'ptls:6640:localhost',
            helpers._connection_to_manager_uri('tls:localhost:6640'))
        self.assertEqual(
            'ptcp:localhost',
            helpers._connection_to_manager_uri('tcp:localhost'))