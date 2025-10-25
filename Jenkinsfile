pipeline {
    agent { label 'slave' }

    environment {
        IMAGE_NAME = "flask-app"
        DOCKERHUB_CREDENTIALS = "dockerhub-creds"
        CONTAINER_NAME = "flask-app-container"
    }

    stages {
        stage('Docker Build & Push') {
            steps {
                echo "🐳 Building Docker image and pushing to Docker Hub..."
                withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS}", usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
                    sh """
                        set -e
                        echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
                        docker build -t $DH_USER/$IMAGE_NAME:latest .
                        docker push $DH_USER/$IMAGE_NAME:latest
                    """
                }
            }
        }

        stage('Deploy') {
            steps {
                echo "🚀 Deploying the Docker container..."
                withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS}", usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
                    sh """
                        set -e
                        # Stop/remove previous container
                        docker stop $CONTAINER_NAME || true
                        docker rm $CONTAINER_NAME || true

                        # Run container and mount .env file
                        docker run --env-file .env -d --name $CONTAINER_NAME -p 5000:5000 $DH_USER/$IMAGE_NAME:latest
                    """
                }
            }
        }
    }

    post {
        always {
            echo "🔹 Pipeline finished. Container status:"
            sh 'docker ps -a | grep flask-app-container || echo "No container running"'
        }
    }
}
