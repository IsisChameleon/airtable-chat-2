#!/usr/bin/env python3
from aws_cdk import App

from infra.backend_deployment_stack import BackendDeploymentPipelineStack
from infra.backend_stack import BackendStack

app = App()
backend_stack = BackendStack(app, "AirtableChat2BackendStack")
pipeline_stack = BackendDeploymentPipelineStack(app, "AirtableChat2BackendDeploymentPipelineStack")

# Add dependency to ensure BackendStack is created first
pipeline_stack.add_dependency(backend_stack)

app.synth()