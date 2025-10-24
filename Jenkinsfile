pipeline {
    agent any

    tools {
        maven 'Maven'  // Must match Jenkins global tool name
    }

    environment {
        DOCKERHUB_USER = 'jayshukla2913'
        IMAGE_NAME = 'flask-mongo-app'
        SONARQUBE_SERVER_NAME = 'Jenkins_SonarQube'
        SONARQUBE_TOKEN = credentials('SonarQube_creds')
        NEXUS_PASSWORD = credentials('nexus_credentials')
        NEXUS_URL = '98.90.57.144:8081/repository/docker-repo/'
    }

    stages {

        stage('Checkout') {
            steps {
                echo "📥 Fetching source code..."
                checkout scm
            }
        }

        stage('Maven Build') {
            steps {
                echo "🔨 Building with Maven..."
                sh 'mvn clean install'
            }
        }

        stage('Python Unit Test') {
            steps {
                echo "🧪 Running Python tests with coverage..."
                sh """
                    pip install pytest pytest-cov flask sqlalchemy
                    pytest --maxfail=1 --disable-warnings --cov=. --cov-report=xml
                """
            }
        }

        stage('SonarQube Scan') {
            steps {
                echo "🔍 Running SonarQube analysis..."
                script {
                    def scannerHome = tool name: 'Jenkins_Scanner', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
                    withSonarQubeEnv("${SONARQUBE_SERVER_NAME}") {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                                -Dsonar.projectKey=Flask_MongoDB_App \
                                -Dsonar.sources=. \
                                -Dsonar.python.coverage.reportPaths=coverage.xml \
                                -Dsonar.host.url=http://98.90.57.144:9000 \
                                -Dsonar.login=${SONARQUBE_TOKEN}
                        """
                    }
                }
            }
        }

        stage('Quality Gate Check') {
            steps {
                echo '⏳ Waiting for SonarQube Quality Gate result...'
                script {
                    timeout(time: 15, unit: 'MINUTES') {
                        def qg = waitForQualityGate abortPipeline: true
                        echo "Quality Gate status: ${qg.status}"
                    }
                }
            }
        }

        stage('Docker Login & Build') {
            steps {
                echo "🐳 Building & pushing Docker image..."
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

        stage('Save Docker Image') {
            steps {
                echo "💾 Saving Docker image to TAR..."
                sh "docker save -o ${IMAGE_NAME}.tar ${DOCKERHUB_USER}/${IMAGE_NAME}:latest"
            }
        }

        stage('Nexus Upload') {
            steps {
                echo "📦 Uploading artifact to Nexus..."
                script {
                    nexusArtifactUploader(
                        nexusVersion: 'NEXUS3',
                        protocol: 'http',
                        nexusUrl: "${NEXUS_URL}",
                        groupId: 'com.jenkins.demo',
                        version: '1.0.0',
                        repository: 'docker-repo',
                        artifacts: [[
                            artifactId: 'flask-mongo-app',
                            classifier: '',
                            file: "${WORKSPACE}/${IMAGE_NAME}.tar",
                            type: 'tar',
                            version: '1.0.0'
                        ]],
                        credentialsId: 'nexus_credentials'
                    )
                }
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                echo "🚀 Deploying Flask + PostgreSQL..."
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
