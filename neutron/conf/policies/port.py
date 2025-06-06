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

from neutron_lib import policy as neutron_policy
from oslo_log import versionutils
from oslo_policy import policy

from neutron.conf.policies import base

DEPRECATED_REASON = (
    "The port API now supports project scope and default roles.")


COLLECTION_PATH = '/ports'
RESOURCE_PATH = '/ports/{id}'
TAGS_PATH = RESOURCE_PATH + '/tags'
TAG_PATH = RESOURCE_PATH + '/tags/{tag_id}'

ACTION_POST = [
    {'method': 'POST', 'path': COLLECTION_PATH},
]
ACTION_PUT = [
    {'method': 'PUT', 'path': RESOURCE_PATH},
]
ACTION_DELETE = [
    {'method': 'DELETE', 'path': RESOURCE_PATH},
]
ACTION_GET = [
    {'method': 'GET', 'path': COLLECTION_PATH},
    {'method': 'GET', 'path': RESOURCE_PATH},
]
ACTION_GET_TAGS = [
    {'method': 'GET', 'path': TAGS_PATH},
    {'method': 'GET', 'path': TAG_PATH},
]
ACTION_PUT_TAGS = [
    {'method': 'PUT', 'path': TAGS_PATH},
    {'method': 'PUT', 'path': TAG_PATH},
]
ACTION_POST_TAGS = [
    {'method': 'POST', 'path': TAGS_PATH},
]
ACTION_DELETE_TAGS = [
    {'method': 'DELETE', 'path': TAGS_PATH},
    {'method': 'DELETE', 'path': TAG_PATH},
]


rules = [
    policy.RuleDefault(
        name='network_device',
        check_str='field:port:device_owner=~^network:',
        description='Definition of port with network device_owner'),
    policy.RuleDefault(
        name='admin_or_data_plane_int',
        check_str=neutron_policy.policy_or(
            'rule:context_is_admin',
            'role:data_plane_integrator'),
        description='Rule for data plane integration'),

    policy.DocumentedRuleDefault(
        name='create_port',
        check_str=neutron_policy.policy_or(
            base.ADMIN_OR_PROJECT_MEMBER,
            base.SERVICE),
        scope_types=['project'],
        description='Create a port',
        operations=ACTION_POST,
        deprecated_rule=policy.DeprecatedRule(
            name='create_port',
            check_str=neutron_policy.RULE_ANY,
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='create_port:device_id',
        check_str=neutron_policy.policy_or(
            base.ADMIN_OR_PROJECT_MEMBER,
            base.SERVICE),
        scope_types=['project'],
        description='Specify ``device_id`` attribute when creating a port',
        operations=ACTION_POST,
        deprecated_rule=policy.DeprecatedRule(
            name='create_port:device_id',
            check_str=neutron_policy.RULE_ANY,
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='create_port:device_owner',
        check_str=neutron_policy.policy_or(
            'not rule:network_device',
            base.ADMIN_OR_SERVICE,
            base.PROJECT_MANAGER,
            base.NET_OWNER_MEMBER
        ),
        scope_types=['project'],
        description='Specify ``device_owner`` attribute when creating a port',
        operations=ACTION_POST,
        deprecated_rule=policy.DeprecatedRule(
            name='create_port:device_owner',
            check_str=neutron_policy.policy_or(
                'not rule:network_device',
                neutron_policy.RULE_ADVSVC,
                neutron_policy.RULE_ADMIN_OR_NET_OWNER),
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='create_port:mac_address',
        check_str=neutron_policy.policy_or(
            base.ADMIN_OR_SERVICE,
            base.PROJECT_MANAGER,
            base.NET_OWNER_MEMBER),
        scope_types=['project'],
        description='Specify ``mac_address`` attribute when creating a port',
        operations=ACTION_POST,
        deprecated_rule=policy.DeprecatedRule(
            name='create_port:mac_address',
            check_str=neutron_policy.policy_or(
                neutron_policy.RULE_ADVSVC,
                neutron_policy.RULE_ADMIN_OR_NET_OWNER),
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='create_port:fixed_ips',
        check_str=neutron_policy.policy_or(
            base.ADMIN_OR_SERVICE,
            base.PROJECT_MANAGER,
            base.NET_OWNER_MEMBER,
            'rule:shared'),
        scope_types=['project'],
        description='Specify ``fixed_ips`` information when creating a port',
        operations=ACTION_POST,
        deprecated_rule=policy.DeprecatedRule(
            name='create_port:fixed_ips',
            check_str=neutron_policy.policy_or(
                neutron_policy.RULE_ADVSVC,
                neutron_policy.RULE_ADMIN_OR_NET_OWNER,
                'rule:shared'),
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='create_port:fixed_ips:ip_address',
        check_str=neutron_policy.policy_or(
            base.ADMIN_OR_SERVICE,
            base.PROJECT_MANAGER,
            base.NET_OWNER_MEMBER),
        scope_types=['project'],
        description='Specify IP address in ``fixed_ips`` when creating a port',
        operations=ACTION_POST,
        deprecated_rule=policy.DeprecatedRule(
            name='create_port:fixed_ips:ip_address',
            check_str=neutron_policy.policy_or(
                neutron_policy.RULE_ADVSVC,
                neutron_policy.RULE_ADMIN_OR_NET_OWNER),
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='create_port:fixed_ips:subnet_id',
        check_str=neutron_policy.policy_or(
            base.ADMIN_OR_SERVICE,
            base.PROJECT_MANAGER,
            base.NET_OWNER_MEMBER,
            'rule:shared'),
        scope_types=['project'],
        description='Specify subnet ID in ``fixed_ips`` when creating a port',
        operations=ACTION_POST,
        deprecated_rule=policy.DeprecatedRule(
            name='create_port:fixed_ips:subnet_id',
            check_str=neutron_policy.policy_or(
                neutron_policy.RULE_ADVSVC,
                neutron_policy.RULE_ADMIN_OR_NET_OWNER,
                'rule:shared'),
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='create_port:port_security_enabled',
        check_str=neutron_policy.policy_or(
            base.ADMIN_OR_SERVICE,
            base.PROJECT_MANAGER,
            base.NET_OWNER_MEMBER),
        scope_types=['project'],
        description=(
            'Specify ``port_security_enabled`` '
            'attribute when creating a port'
        ),
        operations=ACTION_POST,
        deprecated_rule=policy.DeprecatedRule(
            name='create_port:port_security_enabled',
            check_str=neutron_policy.policy_or(
                neutron_policy.RULE_ADVSVC,
                neutron_policy.RULE_ADMIN_OR_NET_OWNER),
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='create_port:binding:host_id',
        check_str=base.ADMIN_OR_SERVICE,
        scope_types=['project'],
        description=(
            'Specify ``binding:host_id`` '
            'attribute when creating a port'
        ),
        operations=ACTION_POST,
        deprecated_rule=policy.DeprecatedRule(
            name='create_port:binding:host_id',
            check_str=neutron_policy.RULE_ADMIN_ONLY,
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='create_port:binding:profile',
        check_str=base.SERVICE,
        scope_types=['project'],
        description=(
            'Specify ``binding:profile`` attribute '
            'when creating a port'
        ),
        operations=ACTION_POST,
        deprecated_rule=policy.DeprecatedRule(
            name='create_port:binding:profile',
            check_str=neutron_policy.RULE_ADMIN_ONLY,
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='create_port:binding:vnic_type',
        check_str=neutron_policy.policy_or(
            base.ADMIN_OR_PROJECT_MEMBER,
            base.SERVICE),
        scope_types=['project'],
        description=(
            'Specify ``binding:vnic_type`` '
            'attribute when creating a port'
        ),
        operations=ACTION_POST,
        deprecated_rule=policy.DeprecatedRule(
            name='create_port:binding:vnic_type',
            check_str=neutron_policy.RULE_ANY,
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='create_port:allowed_address_pairs',
        check_str=neutron_policy.policy_or(
            base.ADMIN_OR_NET_OWNER_MEMBER,
            base.PROJECT_MANAGER,
            base.SERVICE),
        scope_types=['project'],
        description=(
            'Specify ``allowed_address_pairs`` '
            'attribute when creating a port'
        ),
        operations=ACTION_POST,
        deprecated_rule=policy.DeprecatedRule(
            name='create_port:allowed_address_pairs',
            check_str=neutron_policy.RULE_ADMIN_OR_NET_OWNER,
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='create_port:allowed_address_pairs:mac_address',
        check_str=neutron_policy.policy_or(
            base.ADMIN_OR_NET_OWNER_MEMBER,
            base.PROJECT_MANAGER,
            base.SERVICE),
        scope_types=['project'],
        description=(
            'Specify ``mac_address` of `allowed_address_pairs`` '
            'attribute when creating a port'
        ),
        operations=ACTION_POST,
        deprecated_rule=policy.DeprecatedRule(
            name='create_port:allowed_address_pairs:mac_address',
            check_str=neutron_policy.RULE_ADMIN_OR_NET_OWNER,
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='create_port:allowed_address_pairs:ip_address',
        check_str=neutron_policy.policy_or(
            base.ADMIN_OR_NET_OWNER_MEMBER,
            base.PROJECT_MANAGER,
            base.SERVICE),
        scope_types=['project'],
        description=(
            'Specify ``ip_address`` of ``allowed_address_pairs`` '
            'attribute when creating a port'
        ),
        operations=ACTION_POST,
        deprecated_rule=policy.DeprecatedRule(
            name='create_port:allowed_address_pairs:ip_address',
            check_str=neutron_policy.RULE_ADMIN_OR_NET_OWNER,
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='create_port:hints',
        check_str=base.ADMIN,
        scope_types=['project'],
        description=(
            'Specify ``hints`` attribute when creating a port'
        ),
        operations=ACTION_POST,
    ),
    policy.DocumentedRuleDefault(
        name='create_port:trusted',
        check_str=base.ADMIN,
        scope_types=['project'],
        description=(
            'Specify ``trusted`` attribute when creating a port'
        ),
        operations=ACTION_POST,
    ),
    policy.DocumentedRuleDefault(
        name='create_port:tags',
        check_str=neutron_policy.policy_or(
            base.ADMIN_OR_PROJECT_MEMBER,
            neutron_policy.RULE_ADVSVC
        ),
        scope_types=['project'],
        description='Create the port tags',
        operations=ACTION_POST_TAGS,
        deprecated_rule=policy.DeprecatedRule(
            name='create_ports_tags',
            check_str=neutron_policy.policy_or(
                base.ADMIN_OR_PROJECT_MEMBER,
                neutron_policy.RULE_ADVSVC
            ),
            deprecated_reason="Name of the rule is changed.",
            deprecated_since="2025.1")
    ),

    policy.DocumentedRuleDefault(
        name='get_port',
        check_str=neutron_policy.policy_or(
            base.ADMIN_OR_SERVICE,
            base.NET_OWNER_READER,
            base.PROJECT_READER
        ),
        scope_types=['project'],
        description='Get a port',
        operations=ACTION_GET,
        deprecated_rule=policy.DeprecatedRule(
            name='get_port',
            check_str=neutron_policy.policy_or(
                neutron_policy.RULE_ADVSVC,
                'rule:admin_owner_or_network_owner'),
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='get_port:binding:vif_type',
        check_str=base.ADMIN_OR_SERVICE,
        scope_types=['project'],
        description='Get ``binding:vif_type`` attribute of a port',
        operations=ACTION_GET,
        deprecated_rule=policy.DeprecatedRule(
            name='get_port:binding:vif_type',
            check_str=neutron_policy.RULE_ADMIN_ONLY,
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='get_port:binding:vif_details',
        check_str=base.ADMIN_OR_SERVICE,
        scope_types=['project'],
        description='Get ``binding:vif_details`` attribute of a port',
        operations=ACTION_GET,
        deprecated_rule=policy.DeprecatedRule(
            name='get_port:binding:vif_details',
            check_str=neutron_policy.RULE_ADMIN_ONLY,
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='get_port:binding:host_id',
        check_str=base.ADMIN_OR_SERVICE,
        scope_types=['project'],
        description='Get ``binding:host_id`` attribute of a port',
        operations=ACTION_GET,
        deprecated_rule=policy.DeprecatedRule(
            name='get_port:binding:host_id',
            check_str=neutron_policy.RULE_ADMIN_ONLY,
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='get_port:binding:profile',
        check_str=base.ADMIN_OR_SERVICE,
        scope_types=['project'],
        description='Get ``binding:profile`` attribute of a port',
        operations=ACTION_GET,
        deprecated_rule=policy.DeprecatedRule(
            name='get_port:binding:profile',
            check_str=neutron_policy.RULE_ADMIN_ONLY,
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='get_port:resource_request',
        check_str=base.ADMIN,
        scope_types=['project'],
        description='Get ``resource_request`` attribute of a port',
        operations=ACTION_GET,
        deprecated_rule=policy.DeprecatedRule(
            name='get_port:resource_request',
            check_str=neutron_policy.RULE_ADMIN_ONLY,
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='get_port:hints',
        check_str=base.ADMIN,
        scope_types=['project'],
        description='Get ``hints`` attribute of a port',
        operations=ACTION_GET,
    ),
    policy.DocumentedRuleDefault(
        name='get_port:trusted',
        check_str=base.ADMIN,
        scope_types=['project'],
        description='Get ``trusted`` attribute of a port',
        operations=ACTION_GET,
    ),
    policy.DocumentedRuleDefault(
        name='get_port:tags',
        check_str=neutron_policy.policy_or(
            neutron_policy.RULE_ADVSVC,
            base.ADMIN_OR_NET_OWNER_READER,
            base.PROJECT_READER
        ),
        scope_types=['project'],
        description='Get the port tags',
        operations=ACTION_GET_TAGS,
        deprecated_rule=policy.DeprecatedRule(
            name='get_ports_tags',
            check_str=neutron_policy.policy_or(
                neutron_policy.RULE_ADVSVC,
                base.ADMIN_OR_NET_OWNER_READER,
                base.PROJECT_READER
            ),
            deprecated_reason="Name of the rule is changed.",
            deprecated_since="2025.1")
    ),
    # TODO(amotoki): Add get_port:binding:vnic_type
    # TODO(amotoki): Add get_port:binding:data_plane_status

    policy.DocumentedRuleDefault(
        name='update_port',
        check_str=neutron_policy.policy_or(
            base.ADMIN_OR_SERVICE,
            base.PROJECT_MEMBER,
        ),
        scope_types=['project'],
        description='Update a port',
        operations=ACTION_PUT,
        deprecated_rule=policy.DeprecatedRule(
            name='update_port',
            check_str=neutron_policy.policy_or(
                neutron_policy.RULE_ADMIN_OR_OWNER,
                neutron_policy.RULE_ADVSVC),
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='update_port:device_id',
        check_str=neutron_policy.policy_or(
            base.ADMIN_OR_PROJECT_MEMBER,
            base.SERVICE),
        scope_types=['project'],
        description='Update ``device_id`` attribute of a port',
        operations=ACTION_PUT,
        deprecated_rule=policy.DeprecatedRule(
            name='update_port:device_id',
            check_str=neutron_policy.RULE_ANY,
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='update_port:device_owner',
        check_str=neutron_policy.policy_or(
            'not rule:network_device',
            base.ADMIN_OR_SERVICE,
            base.PROJECT_MANAGER,
            base.NET_OWNER_MEMBER,
        ),
        scope_types=['project'],
        description='Update ``device_owner`` attribute of a port',
        operations=ACTION_PUT,
        deprecated_rule=policy.DeprecatedRule(
            name='update_port:device_owner',
            check_str=neutron_policy.policy_or(
                'not rule:network_device',
                neutron_policy.RULE_ADVSVC,
                neutron_policy.RULE_ADMIN_OR_NET_OWNER),
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='update_port:mac_address',
        check_str=neutron_policy.policy_or(
            base.ADMIN_OR_SERVICE,
            base.PROJECT_MANAGER
        ),
        scope_types=['project'],
        description='Update ``mac_address`` attribute of a port',
        operations=ACTION_PUT,
        deprecated_rule=policy.DeprecatedRule(
            name='update_port:mac_address',
            check_str=neutron_policy.policy_or(
                neutron_policy.RULE_ADMIN_ONLY,
                neutron_policy.RULE_ADVSVC),
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='update_port:fixed_ips',
        check_str=neutron_policy.policy_or(
            base.ADMIN_OR_SERVICE,
            base.PROJECT_MANAGER,
            base.NET_OWNER_MEMBER
        ),
        scope_types=['project'],
        description='Specify ``fixed_ips`` information when updating a port',
        operations=ACTION_PUT,
        deprecated_rule=policy.DeprecatedRule(
            name='update_port:fixed_ips',
            check_str=neutron_policy.policy_or(
                neutron_policy.RULE_ADVSVC,
                neutron_policy.RULE_ADMIN_OR_NET_OWNER),
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='update_port:fixed_ips:ip_address',
        check_str=neutron_policy.policy_or(
            base.ADMIN_OR_SERVICE,
            base.PROJECT_MANAGER,
            base.NET_OWNER_MEMBER
        ),
        scope_types=['project'],
        description=(
            'Specify IP address in ``fixed_ips`` '
            'information when updating a port'
        ),
        operations=ACTION_PUT,
        deprecated_rule=policy.DeprecatedRule(
            name='update_port:fixed_ips:ip_address',
            check_str=neutron_policy.policy_or(
                neutron_policy.RULE_ADVSVC,
                neutron_policy.RULE_ADMIN_OR_NET_OWNER),
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='update_port:fixed_ips:subnet_id',
        check_str=neutron_policy.policy_or(
            base.ADMIN_OR_SERVICE,
            base.PROJECT_MANAGER,
            base.NET_OWNER_MEMBER,
            'rule:shared'
        ),
        scope_types=['project'],
        description=(
            'Specify subnet ID in ``fixed_ips`` '
            'information when updating a port'
        ),
        operations=ACTION_PUT,
        deprecated_rule=policy.DeprecatedRule(
            name='update_port:fixed_ips:subnet_id',
            check_str=neutron_policy.policy_or(
                neutron_policy.RULE_ADVSVC,
                neutron_policy.RULE_ADMIN_OR_NET_OWNER,
                'rule:shared'),
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='update_port:port_security_enabled',
        check_str=neutron_policy.policy_or(
            base.ADMIN_OR_SERVICE,
            base.PROJECT_MANAGER,
            base.NET_OWNER_MEMBER
        ),
        scope_types=['project'],
        description='Update ``port_security_enabled`` attribute of a port',
        operations=ACTION_PUT,
        deprecated_rule=policy.DeprecatedRule(
            name='update_port:port_security_enabled',
            check_str=neutron_policy.policy_or(
                neutron_policy.RULE_ADVSVC,
                neutron_policy.RULE_ADMIN_OR_NET_OWNER),
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='update_port:binding:host_id',
        check_str=base.ADMIN_OR_SERVICE,
        scope_types=['project'],
        description='Update ``binding:host_id`` attribute of a port',
        operations=ACTION_PUT,
        deprecated_rule=policy.DeprecatedRule(
            name='update_port:binding:host_id',
            check_str=neutron_policy.RULE_ADMIN_ONLY,
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='update_port:binding:profile',
        check_str=base.SERVICE,
        scope_types=['project'],
        description='Update ``binding:profile`` attribute of a port',
        operations=ACTION_PUT,
        deprecated_rule=policy.DeprecatedRule(
            name='update_port:binding:profile',
            check_str=neutron_policy.RULE_ADMIN_ONLY,
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='update_port:binding:vnic_type',
        check_str=neutron_policy.policy_or(
            base.ADMIN_OR_SERVICE,
            base.PROJECT_MEMBER,
        ),
        scope_types=['project'],
        description='Update ``binding:vnic_type`` attribute of a port',
        operations=ACTION_PUT,
        deprecated_rule=policy.DeprecatedRule(
            name='update_port:binding:vnic_type',
            check_str=neutron_policy.policy_or(
                neutron_policy.RULE_ADMIN_OR_OWNER,
                neutron_policy.RULE_ADVSVC),
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='update_port:allowed_address_pairs',
        check_str=neutron_policy.policy_or(
            base.ADMIN_OR_NET_OWNER_MEMBER,
            base.PROJECT_MANAGER,
            base.SERVICE),
        scope_types=['project'],
        description='Update ``allowed_address_pairs`` attribute of a port',
        operations=ACTION_PUT,
        deprecated_rule=policy.DeprecatedRule(
            name='update_port:allowed_address_pairs',
            check_str=neutron_policy.RULE_ADMIN_OR_NET_OWNER,
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='update_port:allowed_address_pairs:mac_address',
        check_str=neutron_policy.policy_or(
            base.ADMIN_OR_NET_OWNER_MEMBER,
            base.PROJECT_MANAGER,
            base.SERVICE),
        scope_types=['project'],
        description=(
            'Update ``mac_address`` of ``allowed_address_pairs`` '
            'attribute of a port'
        ),
        operations=ACTION_PUT,
        deprecated_rule=policy.DeprecatedRule(
            name='update_port:allowed_address_pairs:mac_address',
            check_str=neutron_policy.RULE_ADMIN_OR_NET_OWNER,
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='update_port:allowed_address_pairs:ip_address',
        check_str=neutron_policy.policy_or(
            base.ADMIN_OR_NET_OWNER_MEMBER,
            base.PROJECT_MANAGER,
            base.SERVICE),
        scope_types=['project'],
        description=(
            'Update ``ip_address`` of ``allowed_address_pairs`` '
            'attribute of a port'
        ),
        operations=ACTION_PUT,
        deprecated_rule=policy.DeprecatedRule(
            name='update_port:allowed_address_pairs:ip_address',
            check_str=neutron_policy.RULE_ADMIN_OR_NET_OWNER,
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='update_port:data_plane_status',
        check_str=neutron_policy.policy_or(
            base.ADMIN,
            'role:data_plane_integrator'),
        scope_types=['project'],
        description='Update ``data_plane_status`` attribute of a port',
        operations=ACTION_PUT,
        deprecated_rule=policy.DeprecatedRule(
            name='update_port:data_plane_status',
            check_str='rule:admin_or_data_plane_int',
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='update_port:hints',
        check_str=base.ADMIN,
        scope_types=['project'],
        description='Update ``hints`` attribute of a port',
        operations=ACTION_PUT,
    ),
    policy.DocumentedRuleDefault(
        name='update_port:trusted',
        check_str=base.ADMIN,
        scope_types=['project'],
        description='Update ``trusted`` attribute of a port',
        operations=ACTION_PUT,
    ),
    policy.DocumentedRuleDefault(
        name='update_port:tags',
        check_str=neutron_policy.policy_or(
            base.ADMIN_OR_PROJECT_MEMBER,
            neutron_policy.RULE_ADVSVC
        ),
        scope_types=['project'],
        description='Update the port tags',
        operations=ACTION_PUT_TAGS,
        deprecated_rule=policy.DeprecatedRule(
            name='update_ports_tags',
            check_str=neutron_policy.policy_or(
                base.ADMIN_OR_PROJECT_MEMBER,
                neutron_policy.RULE_ADVSVC
            ),
            deprecated_reason="Name of the rule is changed.",
            deprecated_since="2025.1")
    ),

    policy.DocumentedRuleDefault(
        name='delete_port',
        check_str=neutron_policy.policy_or(
            base.ADMIN_OR_SERVICE,
            base.NET_OWNER_MEMBER,
            base.PROJECT_MEMBER,
        ),
        scope_types=['project'],
        description='Delete a port',
        operations=ACTION_DELETE,
        deprecated_rule=policy.DeprecatedRule(
            name='delete_port',
            check_str=neutron_policy.policy_or(
                neutron_policy.RULE_ADVSVC,
                'rule:admin_owner_or_network_owner'),
            deprecated_reason=DEPRECATED_REASON,
            deprecated_since=versionutils.deprecated.WALLABY)
    ),
    policy.DocumentedRuleDefault(
        name='delete_port:tags',
        check_str=neutron_policy.policy_or(
            neutron_policy.RULE_ADVSVC,
            base.PROJECT_MEMBER,
            base.ADMIN_OR_NET_OWNER_MEMBER
        ),
        scope_types=['project'],
        description='Delete the port tags',
        operations=ACTION_DELETE_TAGS,
        deprecated_rule=policy.DeprecatedRule(
            name='delete_ports_tags',
            check_str=neutron_policy.policy_or(
                neutron_policy.RULE_ADVSVC,
                base.PROJECT_MEMBER,
                base.ADMIN_OR_NET_OWNER_MEMBER
            ),
            deprecated_reason="Name of the rule is changed.",
            deprecated_since="2025.1")
    )
]


def list_rules():
    return rules
