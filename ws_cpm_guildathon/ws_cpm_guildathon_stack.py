import os
from aws_cdk import core, aws_dynamodb as dynamodb, aws_iam as iam
from cdk_chalice import Chalice

class WsCpmGuildathonStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.connections_table = dynamodb.Table(self, f"WSPlaygroundConnections",
                                             partition_key=dynamodb.Attribute(
                                                 name="connection_id",
                                                 type=dynamodb.AttributeType.STRING),
                                                 billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
                                                 removal_policy=core.RemovalPolicy.DESTROY)

        self.records_table = dynamodb.Table(self, f"WSPlaygroundRecords",
                                             partition_key=dynamodb.Attribute(
                                                 name="connection_id",
                                                 type=dynamodb.AttributeType.STRING),
                                                 billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
                                                 removal_policy=core.RemovalPolicy.DESTROY)
        self.service_role = self._create_service_role()

        chalice_dir = os.path.join(os.path.dirname(__file__), os.pardir, "ws")
        chalice_config = self._create_chalice_stage_config()

        self.chalice = Chalice(self, id, source_dir=chalice_dir, stage_config=chalice_config)



    def _create_chalice_stage_config(self):
        chalice_stage_config = {
            'api_gateway_stage': 'v1',
            'lambda_functions': {
                'api_handler': {
                    'manage_iam_role': False,
                    'iam_role_arn': self.service_role.role_arn,
                    'environment_variables': {  },
                    'lambda_memory_size': 128,
                    'lambda_timeout': 10
                }
            }
        }
        return chalice_stage_config



    def _create_service_role(self):
       role = iam.Role(self, "WSServiceRole",
                       assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"), inline_policies={
                "AccountsServicePolicy": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            actions=[
                                "logs:CreateLogGroup",
                                "logs:CreateLogStream",
                                "logs:PutLogEvents",
                                "logs:DescribeLogGroups",
                            ],
                            resources=["arn:aws:logs:*:*:*"],
                            effect=iam.Effect.ALLOW),
                        iam.PolicyStatement(
                            actions=[
                                "ssm:Describe*",
                                "ssm:Get*",
                                "ssm:List*"
                            ],
                            resources=["arn:aws:ssm:*"],
                            effect=iam.Effect.ALLOW)
                    ])
            })
       return role