chown -R node /home/vscode/.minikube
chmod -R u+wrx /home/vscode/.minikube
cd backend
poetry install
cd ../infra
poetry install
cd ../infra
cd ../frontend
npm install;