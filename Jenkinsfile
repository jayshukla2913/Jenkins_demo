pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'jayshukla2913'
        DOCKERHUB_PASSWORD = 'dckr_pat_f_8R8RnU5gezPvHVJQ0dcSWFqjY'   // Credential ID in Jenkins
        IMAGE_NAME = 'flask-mongo-app'
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Fetching source code..."
                checkout scm
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                echo "Building and pushing Docker image..."
                sh '''
                    echo "---- DEBUG START ----"
                    echo "Docker username: $DOCKERHUB_USER"
                    echo "Password length: ${#DOCKERHUB_PASSWORD}"
                    echo "---- DEBUG END ----"

                    echo "$DOCKERHUB_PASSWORD" | docker login -u "$DOCKERHUB_USER" --password-stdin
                    docker build -t $DOCKERHUB_USER/$IMAGE_NAME:latest .
                    docker push $DOCKERHUB_USER/$IMAGE_NAME:latest
                '''
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                echo "Deploying app using Docker Compose..."
                sh '''
                    docker compose down || true
                    docker compose pull
                    docker compose up -d
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful!"
        }
        failure {
            echo "❌ Deployment failed. Check the logs for errors."
        }
    }
}
