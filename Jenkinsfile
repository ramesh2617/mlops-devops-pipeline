pipeline {
    /* 
     * Run pipeline on any available Jenkins agent
     */
    agent any

    /*
     * Global environment variables
     */
    environment {
        // Absolute path to system-installed Python (required for Windows Jenkins)
        PYTHON_EXE = "C:\\Users\\Mahi\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"

        // Docker image name and dynamic tag using Jenkins build number
        IMAGE_NAME = "mlops-api"
        IMAGE_TAG  = "jenkins-${BUILD_NUMBER}"
    }

    stages {

        /*
         * Stage 1: Checkout source code from GitHub
         */
        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-creds',
                    url: 'https://github.com/ramesh2617/mlops-devops-pipeline.git'
            }
        }

        /*
         * Stage 2: Verify Python availability for Jenkins agent
         */
        stage('Verify Python') {
            steps {
                bat '"%PYTHON_EXE%" --version'
            }
        }

        /*
         * Stage 3: Create Python virtual environment and install dependencies
         */
        stage('Setup Python Environment') {
            steps {
                bat '''
                "%PYTHON_EXE%" -m venv venv
                venv\\Scripts\\python -m pip install --upgrade pip
                venv\\Scripts\\pip install -r requirements.txt
                '''
            }
        }

        /*
         * Stage 4: Train ML model (MLOps step)
         */
        stage('Run ML Training') {
            steps {
                bat '''
                venv\\Scripts\\python src\\train.py
                '''
            }
        }

        /*
         * Stage 5: Run unit tests using pytest
         */
        stage('Run Unit Tests') {
            steps {
                bat '''
                venv\\Scripts\\pytest tests
                '''
            }
        }

        /*
         * Stage 6: Build Docker image for the ML inference service
         */
        stage('Build Docker Image') {
            steps {
                bat '''
                docker build -t %IMAGE_NAME%:%IMAGE_TAG% .
                '''
            }
        }

        /*
         * Stage 7: Load locally built image into Minikube
         * This avoids ImagePullBackOff in local Kubernetes clusters
         */
        stage('Load Image into Minikube') {
            steps {
                bat '''
                minikube image load %IMAGE_NAME%:%IMAGE_TAG%
                '''
            }
        }

        /*
         * Stage 8: Update Kubernetes deployment manifest with new image tag
         * This is the GitOps handoff to Argo CD
         */
        stage('Update K8s Image Tag (GitOps)') {
            steps {
                bat '''
                powershell -Command "(Get-Content k8s\\deployment.yaml) `
                  -replace 'image: mlops-api:.*', 'image: mlops-api:%IMAGE_TAG%' `
                  | Set-Content k8s\\deployment.yaml"
                '''
            }
        }

        /*
         * Stage 9: Commit and push updated Kubernetes manifests
         * Argo CD will automatically detect and deploy the change
         */
        stage('Commit & Push K8s Manifests') {
            steps {
                bat '''
                git config user.email "jenkins@local"
                git config user.name "jenkins"
                git add k8s\\deployment.yaml
                git commit -m "Update image tag to %IMAGE_TAG%" || exit 0
                git push
                '''
            }
        }
    }

    /*
     * Post-build notifications
     */
    post {
        success {
            echo "✅ Jenkins CI completed successfully | Argo CD will deploy automatically"
        }
        failure {
            echo "❌ Jenkins CI pipeline failed"
        }
    }
}
