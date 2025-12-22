pipeline {
    agent any

    environment {
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

        stage('Setup Python Environment') {
            steps {
                bat '''
                python -m venv venv
                venv\\Scripts\\activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run ML Training') {
            steps {
                bat '''
                venv\\Scripts\\activate
                python src\\train.py
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                bat '''
                venv\\Scripts\\activate
                pytest tests
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                docker build -t %IMAGE_NAME%:%IMAGE_TAG% .
                '''
            }
        }
    }

    post {
        success {
            echo "✅ MLOps CI pipeline completed successfully"
        }
        failure {
            echo "❌ Pipeline failed – check logs"
        }
    }
}
