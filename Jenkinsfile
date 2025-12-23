pipeline {
    agent any

    environment {
        IMAGE_NAME = "mlops-api"
        IMAGE_TAG  = "jenkins-${BUILD_NUMBER}"
        PYTHON     = "C:\\Users\\Mahi\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                bat '''
                %PYTHON% -m venv venv
                venv\\Scripts\\python -m pip install --upgrade pip
                venv\\Scripts\\pip install -r requirements.txt
                '''
            }
        }

        stage('Data Preprocessing') {
            steps {
                bat '''
                venv\\Scripts\\python -m src.data_processing.preprocess
                '''
            }
        }

        stage('Model Training') {
            steps {
                bat '''
                venv\\Scripts\\python -m src.training.train
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

        stage('Update K8s Manifest (GitOps)') {
            steps {
                bat """
                %PYTHON% -c \"from pathlib import Path; \
p=Path('k8s/deployment.yaml'); \
lines=p.read_text().splitlines(); \
out=[('        image: %IMAGE_NAME%:%IMAGE_TAG%' if l.strip().startswith('image:') else l) for l in lines]; \
p.write_text('\\\\n'.join(out))\"
                """
            }
        }

        stage('Commit & Push Manifest') {
            steps {
                bat '''
                git config user.email "jenkins@local"
                git config user.name "jenkins"
                git add k8s\\deployment.yaml
                git commit -m "Update image tag to %IMAGE_TAG%" || exit 0
                git push origin main
                '''
            }
        }
    }

    post {
        success {
            echo "MLOps CI pipeline completed successfully"
        }
        failure {
            echo "MLOps CI pipeline failed"
        }
    }
}
