pipeline {
    agent { label 'slave' }

    environment {
        IMAGE_NAME = "flask-app"                    // Docker image name
        DOCKERHUB_CREDENTIALS = "Docker_Master_Credentials"  // Jenkins Docker Hub credential ID
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
                sh """
                    docker stop $CONTAINER_NAME || true
                    docker rm $CONTAINER_NAME || true
                    docker run -d --name $CONTAINER_NAME -p 5000:5000 \\
                        -e DATABASE_URL=postgresql://user:password@localhost:5432/mydb \\
                        $DH_USER/$IMAGE_NAME:latest
                """
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
