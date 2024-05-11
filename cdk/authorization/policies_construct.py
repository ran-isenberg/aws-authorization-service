import json

from aws_cdk import aws_verifiedpermissions as avp
from constructs import Construct


class PoliciesConstruct(Construct):
    def __init__(self, scope: Construct, id_: str) -> None:
        super().__init__(scope, id_)
        self.id_ = id_
        self.policy_store = self._create_policy_store()
        self._create_default_policies()

    def _create_policy_store(self):
        my_schema = {
            'Orders': {
                'entityTypes': {
                    'Role': {'memberOfTypes': [], 'shape': {'attributes': {'user_id': {'required': False, 'type': 'String'}}, 'type': 'Record'}},
                    'Customer': {
                        'memberOfTypes': [],
                        'shape': {
                            'type': 'Record',
                            'attributes': {'region': {'type': 'String', 'required': False}, 'user_id': {'type': 'String', 'required': False}},
                        },
                    },
                },
                'actions': {
                    'CreateOrder': {
                        'memberOf': [],
                        'appliesTo': {
                            'context': {
                                'type': 'Record',
                                'attributes': {'ip_address': {'required': False, 'type': 'String'}, 'weekday': {'required': False, 'type': 'String'}},
                            },
                            'principalTypes': ['Role'],
                            'resourceTypes': ['Customer'],
                        },
                    },
                    'ManageOrders': {
                        'memberOf': [],
                        'appliesTo': {
                            'context': {
                                'type': 'Record',
                                'attributes': {'ip_address': {'required': False, 'type': 'String'}, 'weekday': {'type': 'String', 'required': False}},
                            },
                            'principalTypes': ['Role'],
                            'resourceTypes': ['Customer'],
                        },
                    },
                },
            }
        }
        # Create a Policy Store
        cfn_policy_store = avp.CfnPolicyStore(
            self,
            'OrdersDefaultPolicyStore',
            validation_settings=avp.CfnPolicyStore.ValidationSettingsProperty(mode='STRICT'),
            description='default policy store for orders service',
            schema=avp.CfnPolicyStore.SchemaDefinitionProperty(cedar_json=json.dumps(my_schema)),
        )
        return cfn_policy_store

    def _create_default_policies(self):
        mgr_policy_def = avp.CfnPolicy.PolicyDefinitionProperty(
            static=avp.CfnPolicy.StaticPolicyDefinitionProperty(
                statement='permit (principal == MSP::Role::"mgr", action in [MSP::Action::"CreateOrder"], resource) when { true };',  # pylint: disable=line-too-long
                description='default policy for manager user',
            )
        )
        avp.CfnPolicy(self, 'ManagerDefaultPolicy', definition=mgr_policy_def, policy_store_id=self.policy_store.attr_policy_store_id)
