from aws_cdk import Fn, SecretValue, Stack
from aws_cdk import (
    aws_codebuild as codebuild,
)
from aws_cdk import (
    aws_codepipeline as codepipeline,
)
from aws_cdk import (
    aws_codepipeline_actions as codepipeline_actions,
)
from aws_cdk import aws_iam as iam
from constructs import Construct


class BackendDeploymentPipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_function_arn = Fn.import_value("LambdaFunctionArn")
        # lambda_alias_arn = Fn.import_value("LambdaAliasArn")
        ecr_repo_uri = Fn.import_value("ECRRepositoryUri")

        self.pipeline = codepipeline.Pipeline(self, "AirtableChat2BackendPipeline")

        # Source Stage
        source_output = codepipeline.Artifact()
        source_action = codepipeline_actions.GitHubSourceAction(
            action_name="GitHub_Source",
            owner="isischameleon",
            repo="airtable-chat2",
            branch="main",
            oauth_token=SecretValue.secrets_manager("test/airtable-chat-2/github-token"),
            output=source_output,
            trigger=codepipeline_actions.GitHubTrigger.WEBHOOK
        )

        # Build Stage
        build_project = codebuild.PipelineProject(
            self, "BuildProject",
            build_spec=codebuild.BuildSpec.from_object({
                "version": "0.2",
                "phases": {
                    "build": {
                        "commands": [
                            "cd ../backend",
                            "docker build -t $ECR_REPO_URI:$CODEBUILD_RESOLVED_SOURCE_VERSION .",
                            "docker push $ECR_REPO_URI:$CODEBUILD_RESOLVED_SOURCE_VERSION",
                            "aws lambda update-function-code --function-name $FUNCTION_NAME --image-uri $ECR_REPO_URI:$CODEBUILD_RESOLVED_SOURCE_VERSION"
                        ]
                    }
                }
            }),
            environment_variables={
                "ECR_REPO_URI": codebuild.BuildEnvironmentVariable(value=ecr_repo_uri),
                "FUNCTION_NAME": codebuild.BuildEnvironmentVariable(value=Fn.select(6, Fn.split(':', lambda_function_arn)))
            },
            environment=codebuild.BuildEnvironment(privileged=True)
        )

        build_output = codepipeline.Artifact()
        build_action = codepipeline_actions.CodeBuildAction(
            action_name="Build",
            project=build_project,
            input=source_output,
            outputs=[build_output],
        )

        # Deploy Stage
        update_lambda_project = codebuild.PipelineProject(
            self, "UpdateLambdaProject",
            build_spec=codebuild.BuildSpec.from_object({
                "version": "0.2",
                "phases": {
                    "build": {
                        "commands": [
                            f"aws lambda update-function-code --function-name {Fn.select(6, Fn.split(':', lambda_function_arn))} --image-uri $ECR_REPO_URI:latest"
                        ]
                    }
                }
            }),
            environment_variables={
                "ECR_REPO_URI": codebuild.BuildEnvironmentVariable(value=ecr_repo_uri)
            }
        )

        # Add permissions to update Lambda
        update_lambda_project.add_to_role_policy(iam.PolicyStatement(
            actions=["lambda:UpdateFunctionCode"],
            resources=[lambda_function_arn]
        ))

        deploy_action = codepipeline_actions.CodeBuildAction(
            action_name="UpdateLambda",
            project=update_lambda_project,
            input=build_output,
            run_order=1
        )

        self.pipeline.add_stage(stage_name="Source", actions=[source_action])
        self.pipeline.add_stage(stage_name="Build", actions=[build_action])
        self.pipeline.add_stage(stage_name="Deploy", actions=[deploy_action])