pipeline {
    agent any

    tools {
        python 'Python-3.12'
    }

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

        stage('Verify Python') {
            steps {
                bat 'python --version'
            }
        }

        stage('Setup Python Environment') {
            steps {
                bat '''
                python -m venv venv
                venv\\Scripts\\python -m pip install --upgrade pip
                venv\\Scripts\\pip install -r requirements.txt
                '''
            }
        }

        stage('Run ML Training') {
            steps {
                bat '''
                venv\\Scripts\\python src\\train.py
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                bat '''
                venv\\Scripts\\pytest tests
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
            echo "✅ Jenkins MLOps pipeline completed successfully"
        }
        failure {
            echo "❌ Jenkins pipeline failed"
        }
    }
}
