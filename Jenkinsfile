pipeline {
    agent { label 'slave' }

    environment {
        IMAGE_NAME = "flask-app"
        CONTAINER_NAME = "flask-app-container"
        POSTGRES_CONTAINER = "flask-db-container"
        DOCKERHUB_CREDENTIALS = "Docker_Master_Credentials"
        NETWORK_NAME = "docker-network"
        VOLUME_NAME = "pgdata"
    }

    stages {
        stage('Docker Build & Push Flask App') {
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

        stage('Setup Network & Volume') {
            steps {
                echo "🌐 Creating Docker network and volume if not exists..."
                sh """
                    docker network inspect $NETWORK_NAME >/dev/null 2>&1 || docker network create $NETWORK_NAME
                    docker volume inspect $VOLUME_NAME >/dev/null 2>&1 || docker volume create $VOLUME_NAME
                """
            }
        }

        stage('Deploy PostgreSQL') {
            steps {
                echo "🛢️ Deploying PostgreSQL container..."
                sh """
                    docker stop $POSTGRES_CONTAINER || true
                    docker rm $POSTGRES_CONTAINER || true
                    docker run -d \
                        --name $POSTGRES_CONTAINER \
                        --network $NETWORK_NAME \
                        -v $VOLUME_NAME:/var/lib/postgresql/data \
                        --env-file .env \
                        postgres:15
                """
            }
        }

        stage('Deploy Flask App') {
            steps {
                echo "🚀 Deploying Flask container..."
                withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS}", usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
                    sh """
                        docker stop $CONTAINER_NAME || true
                        docker rm $CONTAINER_NAME || true
                        docker run -d \
                            --name $CONTAINER_NAME \
                            --network $NETWORK_NAME \
                            -p 5000:5000 \
                            --env-file .env \
                            $DH_USER/$IMAGE_NAME:latest
                    """
                }
            }
        }
    }

    post {
        always {
            echo "🔹 Pipeline finished. Container status:"
            sh 'docker ps -a | grep -E "flask-app-container|flask-db-container" || echo "No container running"'
        }
    }
}
