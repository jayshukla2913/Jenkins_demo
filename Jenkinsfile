pipeline {
    agent any

    tools {
        maven 'Maven'  // Make sure Maven is installed and configured in Jenkins
    }

    environment {
        DOCKERHUB_USER = 'jayshukla2913'
        IMAGE_NAME = 'flask-mongo-app'
        SONARQUBE_SERVER_NAME = 'Jenkins_SonarQube'
        SONARQUBE_TOKEN = credentials('SonarQube_creds') // Jenkins credential
        NEXUS_PASSWORD = credentials('nexus_credentials') // Jenkins credential
        NEXUS_URL = '98.90.57.144:8081/repository/docker-repo/'
    }

    stages {

        stage('Checkout') {
            steps {
                echo "📥 Fetching source code..."
                checkout scm
            }
        }

        stage('Python Test & Coverage') {
            steps {
                echo "🐍 Installing Python dependencies in venv and running tests..."
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install flask sqlalchemy pytest pytest-cov
                    pytest --maxfail=1 --disable-warnings --cov=. --cov-report=xml
                '''
            }
        }

        stage('SonarQube Scan') {
            steps {
                echo "🔍 Running SonarQube scan..."
                script {
                    // Use sonar-scanner installation defined in Jenkins
                    def scannerHome = tool name: 'Jenkins_Scanner', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
                    withSonarQubeEnv("${SONARQUBE_SERVER_NAME}") {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                                -Dsonar.projectKey=Flask_MongoDB_App \
                                -Dsonar.sources=. \
                                -Dsonar.host.url=http://98.90.57.144:9000 \
                                -Dsonar.login=${SONARQUBE_TOKEN} \
                                -Dsonar.python.coverage.reportPaths=coverage.xml
                        """
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
                    sh '''
                        echo $PASS | docker login -u $USER --password-stdin
                        docker build -t $USER/$IMAGE_NAME:latest .
                        docker push $USER/$IMAGE_NAME:latest
                    '''
                }
            }
        }

        stage('Docker Compose Deploy') {
            steps {
                echo "🚀 Deploying Flask + PostgreSQL using Docker Compose..."
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
            echo "❌ Deployment failed. Check logs for details."
        }
    }
}
