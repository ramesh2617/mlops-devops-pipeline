pipeline {
    agent any

    environment {
        // Python path for Windows Jenkins
        PYTHON_EXE = "C:\\Users\\Mahi\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"

        // Docker image info
        IMAGE_NAME = "mlops-api"
        IMAGE_TAG  = "jenkins-${BUILD_NUMBER}"
        K8S_DEPLOYMENT = "mlops-api"
        K8S_CONTAINER  = "mlops-api"
        K8S_NAMESPACE  = "default"
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

        stage('Deploy to Kubernetes (Update Image)') {
            steps {
                bat """
                kubectl set image deployment/%K8S_DEPLOYMENT% \
                  %K8S_CONTAINER%=%IMAGE_NAME%:%IMAGE_TAG% \
                  -n %K8S_NAMESPACE%
                """
            }
        }
    }

    post {
        success {
            echo "✅ Jenkins CI/CD successful | Kubernetes deployment updated"
        }
        failure {
            echo "❌ Jenkins CI/CD failed"
        }
    }
}
