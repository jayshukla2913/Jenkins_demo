pipeline {
    agent { label 'slave' }

    environment {
        IMAGE_NAME = "flask-app"                    // Docker image name
        DOCKERHUB_CREDENTIALS = "dockerhub-creds"  // Jenkins Docker Hub credential ID
        CONTAINER_NAME = "flask-app-container"
    }

    stages {
        stage('Docker Build & Push') {
            steps {
                echo "🐳 Building Docker image and pushing to Docker Hub..."
                // Use withCredentials to access Docker Hub credentials safely
                withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS}", usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
                    sh """
                        set -e
                        # Login to Docker Hub
                        echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin

                        # Build Docker image with multi-stage Dockerfile
                        docker build -t $DH_USER/$IMAGE_NAME:latest .

                        # Push image to Docker Hub
                        docker push $DH_USER/$IMAGE_NAME:latest
                    """
                }
            }
        }

        stage('Deploy') {
            steps {
                echo "🚀 Deploying the Docker container..."
                // Wrap deploy stage in withCredentials if using Docker Hub image
                withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS}", usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
                    sh """
                        set -e
                        # Stop/remove any previous container
                        docker stop $CONTAINER_NAME || true
                        docker rm $CONTAINER_NAME || true

                        # Run the new container
                        docker run -d --name $CONTAINER_NAME -p 5000:5000 \\
                            -e DATABASE_URL=postgresql://user:password@localhost:5432/mydb \\
                            $DH_USER/$IMAGE_NAME:latest
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
