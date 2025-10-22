pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'jayshukla2913'
        IMAGE_NAME = 'flask-mongo-app'
        SONARQUBE_SERVER_NAME = 'Jenkins_SonarQube'
        SONARQUBE_TOKEN = credentials('SonarQube_creds') // Jenkins credential
    }

    stages {

        stage('Checkout') {
            steps {
                echo "📥 Fetching source code..."
                checkout scm
            }
        }

        stage('SonarQube Scan') {
            steps {
                echo "🔍 Running SonarQube scan..."
                script {
                    // Dynamically locate sonar-scanner installation
                    def scannerHome = tool name: 'Jenkins_Scanner', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
                    withSonarQubeEnv("${SONARQUBE_SERVER_NAME}") {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                                -Dsonar.projectKey=Flask_MongoDB_App \
                                -Dsonar.sources=. \
                                -Dsonar.host.url=http://98.90.57.144:9000 \
                                -Dsonar.login=${SONARQUBE_TOKEN}
                        """
                    }
                }
            }
        }

        stage('Quality Gate Check') {
            steps {
                echo '⏳ Quality Gate check skipped for debug purposes'
                script {
                    // Timeout block kept for future use
                    timeout(time: 15, unit: 'MINUTES') {
                        // def qg = waitForQualityGate abortPipeline: true
                        // echo "Pipeline will continue without Quality Gate"
                    }
                }
            }
        }

        stage('Docker Login & Build') {
            steps {
                echo "🐳 Logging into Docker Hub and building the image..."
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
                echo "🚀 Deploying Flask + PostgreSQL using Docker Compose..."
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
