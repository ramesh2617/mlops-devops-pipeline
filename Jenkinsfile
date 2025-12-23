pipeline {
    agent any

    environment {
        // Python executable path (Windows Jenkins)
        PYTHON_EXE = "C:\\Users\\Mahi\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"

        // Docker image details
        IMAGE_NAME = "mlops-api"
        IMAGE_TAG  = "jenkins-${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-creds',
                    url: 'https://github.com/ramesh2617/mlops-devops-pipeline.git'
            }
        }

        stage('Verify Python') {
            steps {
                bat "\"%PYTHON_EXE%\" --version"
            }
        }

        stage('Setup Python Environment') {
            steps {
                bat """
                "%PYTHON_EXE%" -m venv venv
                venv\\Scripts\\python -m pip install --upgrade pip
                venv\\Scripts\\pip install -r requirements.txt
                """
            }
        }

        stage('Run ML Training') {
            steps {
                bat "venv\\Scripts\\python src\\train.py"
            }
        }

        stage('Run Unit Tests') {
            steps {
                bat "venv\\Scripts\\pytest tests"
            }
        }

        stage('Build Docker Image') {
            steps {
                bat "docker build -t %IMAGE_NAME%:%IMAGE_TAG% ."
            }
        }

        stage('Update K8s Manifest Image Tag (GitOps)') {
            steps {
                bat """
                "%PYTHON_EXE%" - <<EOF
from pathlib import Path

file = Path("k8s/deployment.yaml")
data = file.read_text()

new_data = []
for line in data.splitlines():
    if line.strip().startswith("image:"):
        new_data.append(f"        image: {\"mlops-api\"}:{\"%IMAGE_TAG%\"}")
    else:
        new_data.append(line)

file.write_text("\\n".join(new_data))
print("Updated image tag to %IMAGE_TAG%")
EOF
                """
            }
        }

        stage('Commit & Push K8s Manifests') {
            steps {
                bat """
                git config user.email "jenkins@local"
                git config user.name "jenkins"
                git add k8s\\deployment.yaml
                git commit -m "Update image tag to %IMAGE_TAG%" || exit 0
                git push
                """
            }
        }
    }

    post {
        success {
            echo "✅ Jenkins CI finished | Argo CD will deploy from Git"
        }
        failure {
            echo "❌ Jenkins CI failed"
        }
    }
}
