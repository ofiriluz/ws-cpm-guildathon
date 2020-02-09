from aws_cdk import core, aws_dynamodb as dynamodb

class WsCpmGuildathonStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.connections_table = dynamodb.Table(self, f"WSPlaygroundConnections",
                                             partition_key=dynamodb.Attribute(
                                                 name="connection_id",
                                                 type=dynamodb.AttributeType.STRING),
                                             billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
                                             removal_policy=core.RemovalPolicy.DESTROY)

        self.connections_table = dynamodb.Table(self, f"WSPlaygroundRecords",
                                             partition_key=dynamodb.Attribute(
                                                 name="connection_id",
                                                 type=dynamodb.AttributeType.STRING),
                                             billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
                                             removal_policy=core.RemovalPolicy.DESTROY)
