#!/usr/bin/env python3
import aws_cdk as cdk

from infra.backend_stack import BackendStack
from infra.backend_deployment_stack import BackendDeploymentPipelineStack

app = cdk.App()
backend_stack = BackendStack(app, "Airtable2BackendStack")
pipeline_stack = BackendDeploymentPipelineStack(app, "BackendDeploymentPipelineStack", 
                                                lambda_function=backend_stack.airtable2_lambda,
                                                function_alias=backend_stack.function_alias)
app.synth()
