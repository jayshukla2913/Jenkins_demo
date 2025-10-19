pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'your_dockerhub_username'
        IMAGE_NAME = 'flaskapp'
        # Docker Hub password stored as Jenkins secret
        DOCKERHUB_PASSWORD = credentials('dockerhub-password-id')
    }

    stages {

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                sh '''
                    docker build -t $DOCKERHUB_USER/$IMAGE_NAME:latest .
                    echo $DOCKERHUB_PASSWORD | docker login -u $DOCKERHUB_USER --password-stdin
                    docker push $DOCKERHUB_USER/$IMAGE_NAME:latest
                '''
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                echo "Deploying Flask app with DB using Docker Compose..."
                sh '''
                    # Stop and remove old containers if any
                    docker-compose down || true

                    # Pull latest image from Docker Hub
                    docker-compose pull

                    # Start containers in detached mode
                    docker-compose up -d
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully! Access your app at http://<EC2_PUBLIC_IP>:5000"
        }
        failure {
            echo "Pipeline failed. Check Jenkins console for details."
        }
    }
}
