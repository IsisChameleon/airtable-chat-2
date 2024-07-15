from aws_cdk import (
    CfnOutput,
    Duration,
    Stack,
)
from aws_cdk import (
    aws_apigateway as apigw,
)
from aws_cdk import (
    aws_ec2 as ec2,
)
from aws_cdk import aws_ecr_assets as ecr_assets
from aws_cdk import (
    aws_lambda as lambda_,
)
from constructs import Construct


class BackendStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a VPC
        self.vpc = ec2.Vpc(
            self, 
            "Airtable2VPC",
            max_azs=2,
            nat_gateways=1,
        )

        # # ECR Repository
        # self.ecr_repository = ecr.Repository.from_repository_name(
        #     self, 
        #     "BackendECRRepository", 
        #     repository_name="airtable2-backend-repo"
        # )

                # Create a Docker image from the AWS Python base image
        self.docker_image = ecr_assets.DockerImageAsset(
            self,
            "BackendDockerImage",
            directory="../backend",
            file="Dockerfile",
        )

        # Create the Lambda function using the Docker image
        self.airtable2_lambda = lambda_.DockerImageFunction(
            self,
            "AirtableChat2Function",
            code=lambda_.DockerImageCode.from_ecr(
                repository=self.docker_image.repository,
                tag_or_digest=self.docker_image.image_tag,
            ),
            memory_size=1024,
            timeout=Duration.seconds(30),
        )

        # Create an alias
        self.function_alias = lambda_.Alias(
            self, 
            "FunctionAlias", 
            alias_name="live", 
            version=self.airtable2_lambda.current_version
        )

        # Create an API Gateway
        self.api = apigw.LambdaRestApi(
            self,
            "Airtable2Api",
            handler=self.airtable2_lambda,
            proxy=True,
        )

        # Outputs
# Outputs
        CfnOutput(self, "LambdaFunctionArnOutput", 
                value=self.airtable2_lambda.function_arn, 
                export_name="LambdaFunctionArn")
        CfnOutput(self, "LambdaAliasArnOutput", 
                value=self.function_alias.function_arn,
                export_name="LambdaAliasArn")
        # CfnOutput(self, "ECRRepositoryUriOutput", 
        #         value=self.ecr_repository.repository_uri, 
        #         export_name="ECRRepositoryUri")
        CfnOutput(self, "ECRRepositoryUriOutput", 
            value=self.docker_image.repository.repository_uri, 
            export_name="ECRRepositoryUri")
        CfnOutput(self, "ApiGatewayUrlOutput", 
                value=self.api.url, 
                export_name="ApiGatewayUrl")