1.
Source stage (GitHub):
Monitors your GitHub repository for changes (e.g., pushes to a specific branch)
When changes are detected, it pulls the latest code from the repository
2.
Build stage (CodeBuild):
Takes the code from the Source stage
Runs your build process (e.g., installing dependencies, running tests)
Creates the Docker image for your Lambda function
Pushes the Docker image to Amazon ECR
3.
Deploy stage (updating the Lambda function):
Updates your Lambda function to use the newly built Docker image
Can include additional deployment steps like updating API Gateway or other related resources
