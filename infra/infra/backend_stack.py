#!/usr/bin/env python3
from aws_cdk import App, Duration, Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_ecr_assets as ecr_assets
from aws_cdk import aws_ecr as ecr

class BackendStack(Stack):
    def __init__(self, scope: App, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a VPC
        self.vpc = ec2.Vpc(self, "Airtable2VPC",
            max_azs=2,  # Use 2 Availability Zones for high availability
            nat_gateways=1  # Shortcut: Use only 1 NAT Gateway to reduce costs
        )

        # Create an ECR repository
        self.ecr_repository = ecr.Repository(self, "BackendECRRepository",
            repository_name="airtable2-backend-repo"
        )

        # Create a Docker image from the AWS Python base image
        self.docker_image = ecr_assets.DockerImageAsset(
            self, "BackendDockerImage",
            directory='../backend',  # Path to your Dockerfile and Lambda code
            file='Dockerfile',  # Name of your Dockerfile
        )

        # Create the Lambda function using the Docker image
        self.airtable2_lambda = lambda_.DockerImageFunction(
            self, "AirtableChat2Function",
            code=lambda_.DockerImageCode.from_ecr(
                repository=ecr.Repository.from_repository_name(
                    self, "ECRRepo",
                    repository_name="airtable2-backend-repo"
                ),
                tag="latest"
            ),
            memory_size=1024,
            timeout=Duration.seconds(30),
        )

        version = self.airtable2_lambda.current_version

        # Create an alias
        self.function_alias = lambda_.Alias(
            self, "FunctionAlias",
            alias_name="live",
            version=version,
                        environment={
                # Add any environment variables your function needs
            }
        )

        # Output the function ARN for use in other stacks
        self.airtable2_lambda_arn = self.airtable2_lambda.function_arn

        # # Create a Lambda function
        # airtable2_lambda = lambda_.Function(self, "Airtable2FastAPILambda",
        #     runtime=lambda_.Runtime.PYTHON_3_11,
        #     handler="main.handler",
        #     code=lambda_.Code.from_asset("../backend"),  # Assumes FastAPI code is in the backend directory
        #     timeout=Duration.seconds(30),  
        #     memory_size=1024,  
        #     environment={
        #         "PYTHONPATH": "/var/task",
        #         # Add other environment variables as needed
        #     }
        # )

        # Create an API Gateway
        self.api = apigw.LambdaRestApi(self, "Airtable2Api",
            handler=self.airtable2_lambda,
            proxy=True  # Shortcut: Use proxy integration for simplicity
        )