pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'jayshukla2913'
        IMAGE_NAME = 'flask-mongo-app'
        SONARQUBE_SERVER_NAME = 'Jenkins_SonarQube'
        SONARQUBE_TOKEN = credentials('SonarQube_creds')
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Fetching source code..."
                checkout scm
            }
        }

        stage('SonarQube Scan') {
            steps {
                echo "Running SonarQube scan"
                withSonarQubeEnv('Jenkins_SonarQube') {
                    sh """
                        sonar-scanner \
                            -Dsonar.projectKey=Flask_MongoDB_App \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=http://98.90.57.144:9000 \
                            -Dsonar.login=$SONARQUBE_TOKEN
                    """
                }
            }
        }

        stage('Quality Gate Check') {
            steps {
                echo 'Waiting for SonarQube Quality Gate status...'
                script {
                    timeout(time: 5, unit: 'MINUTES') {
                        def qg = waitForQualityGate abortPipeline: true
                        if (qg.status != 'OK') {
                            error "Pipeline failed: SonarQube Quality Gate status is ${qg.status}"
                        }
                    }
                }
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
                echo "Deploying Flask + Postgres using Docker Compose..."
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
