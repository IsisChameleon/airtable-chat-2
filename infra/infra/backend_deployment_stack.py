from aws_cdk import (
    SecretValue,
    Stack,
)
from aws_cdk import (
    aws_codebuild as codebuild,
)
from aws_cdk import (
    aws_codedeploy as codedeploy,
)
from aws_cdk import (
    aws_codepipeline as codepipeline,
)
from aws_cdk import (
    aws_codepipeline_actions as codepipeline_actions,
)
from aws_cdk import (
    aws_lambda as lambda_,
)
from constructs import Construct


class BackendDeploymentPipelineStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        lambda_function: lambda_.Function,
        function_alias: lambda_.Alias,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.pipeline = codepipeline.Pipeline(self, "AirtableChat2BackendPipeline")

        self.source_output = codepipeline.Artifact()
        self.source_action = codepipeline_actions.GitHubSourceAction(
            action_name="GitHubSourceBackend",
            output=self.source_output,
            owner="isischameleon",
            repo="airtable-chat2",
            branch="main",
            oauth_token=SecretValue.secrets_manager(
                "test/airtable-chat-2/github-token"
            ),
            trigger=codepipeline_actions.GitHubTrigger.WEBHOOK,
            filter_group=[
                codepipeline_actions.GitHubSourceFilter.path("backend/"),
            ],
        )

        build_project = codebuild.PipelineProject(
            self,
            "BuildProject",
            build_spec=codebuild.BuildSpec.from_object(
                {
                    "version": "0.2",
                    "phases": {
                        "build": {
                            "commands": [
                                "cd backend",
                                "docker build -t airtable-chat2 .",
                                "docker push ${REPOSITORY_URI}:latest",
                            ]
                        }
                    },
                }
            ),
            environment=codebuild.BuildEnvironment(
                privileged=True,
            ),
        )

        self.build_output = codepipeline.Artifact()
        self.build_action = codepipeline_actions.CodeBuildAction(
            action_name="BuildAction",
            project=build_project,
            input=self.source_output,
            outputs=[self.build_output],
        )

        # Create a Lambda deployment group
        self.deployment_group = codedeploy.LambdaDeploymentGroup(
            self,
            "LambdaDeploymentGroup",
            alias=function_alias,
            deployment_config=codedeploy.LambdaDeploymentConfig.ALL_AT_ONCE,
        )

        # Use CodeDeployServerDeployAction for Lambda deployment
        self.deploy_action = codepipeline_actions.CodeDeployServerDeployAction(
            action_name="DeployAction",
            deployment_group=self.deployment_group,
            input=self.build_output,
        )

        self.pipeline.add_stage(stage_name="Source", actions=[self.source_action])

        self.pipeline.add_stage(stage_name="Build", actions=[self.build_action])

        self.pipeline.add_stage(stage_name="Deploy", actions=[self.deploy_action])
