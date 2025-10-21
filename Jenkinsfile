pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'your-dockerhub-username'
        IMAGE_NAME = 'flask-mongo-app'
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Fetching source code..."
                checkout scm
            }
        }

        stage('Docker Login & Build') {
            steps {
                echo "Logging into Docker Hub and building the image..."
                withCredentials([usernamePassword(credentialsId: 'Jenkins_MongoDB', 
                                                 usernameVariable: 'USER', 
                                                 passwordVariable: 'PASS')]) {
                    sh """
                        echo \$PASS | docker login -u \$USER --password-stdin
                        docker build -t \$USER/\$IMAGE_NAME:latest .
                        docker push \$USER/\$IMAGE_NAME:latest
                    """
                }
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                echo "Deploying Flask + MongoDB using Docker Compose..."
                sh """
                    docker compose down || true
                    docker compose pull
                    docker compose up -d
                """
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful!"
        }
        failure {
            echo "❌ Deployment failed. Check logs for details."
        }
    }
}
