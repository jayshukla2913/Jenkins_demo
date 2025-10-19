pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask-jenkins-demo"
        DOCKERHUB_USER = "jayshukla2913"
    }

    stages {
        stage('Source') {
            steps {
                echo "Cloning source code..."
                git branch: 'main', url: 'https://github.com/jayshukla2913/Jenkins_demo.git'
            }
        }

        stage('Build') {
            steps {
                echo "Building Docker image..."
                sh 'docker build -t $DOCKERHUB_USER/$IMAGE_NAME:latest .'
            }
        }

        stage('Test') {
            steps {
                echo "Testing container startup..."
                sh '''
                    docker run -d --name flask-stark -p 5000:5001 $DOCKERHUB_USER/$IMAGE_NAME:latest
                    sleep 5
                    curl -f http://98.90.57.144:5000 || (echo "Test failed" && exit 1)
                    docker stop test-container && docker rm test-container
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo "Deploying app container..."
                sh '''
                    docker ps -q --filter "name=flask-app" | grep -q . && docker stop flask-app && docker rm flask-app || true
                    docker run -d -p 8081:5001 --name flask-app $DOCKERHUB_USER/$IMAGE_NAME:latest
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful!"
        }
        failure {
            echo "❌ Build failed!"
        }
    }
}

