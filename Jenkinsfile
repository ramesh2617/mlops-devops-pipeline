pipeline {
    agent any

    environment {
        PYTHON_EXE = "C:\\Users\\Mahi\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
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

        stage('Update K8s Image Tag (GitOps)') {
            steps {
                bat """
                powershell -NoProfile -Command "& {
                    (Get-Content 'k8s\\deployment.yaml') `
                        -replace 'image: mlops-api:.*', 'image: mlops-api:%IMAGE_TAG%' |
                    Set-Content 'k8s\\deployment.yaml'
                }"
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
            echo "✅ Jenkins CI successful | Argo CD will auto-deploy"
        }
        failure {
            echo "❌ Jenkins CI failed"
        }
    }
}
