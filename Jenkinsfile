pipeline {
    agent any
    
    tools {
        maven 'Maven'  // Name as defined under Manage Jenkins → Global Tool Configuration
    }

    environment {
        DOCKERHUB_USER = 'jayshukla2913'
        IMAGE_NAME = 'flask-mongo-app'
        SONARQUBE_SERVER_NAME = 'Jenkins_SonarQube'
        SONARQUBE_TOKEN = credentials('SonarQube_creds') // Jenkins credential
        NEXUS_PASSWORD = credentials('nexus_credentials') // Jenkins credential
        NEXUS_URL = '98.90.57.144:8081/repository/docker-repo/'
        NEXUS_URL2 = '98.90.57.144:8081/repository/docker-image-repo/'
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

        stage('Demo Maven Test') {
            steps {
                echo "🧪 Running Maven tests..."
                sh 'mvn test'
            }
        }

        stage('Python Test & Coverage') {
            steps {
                echo "🐍 Installing Python dependencies and running tests..."
                sh '''
                    # Upgrade pip
                    apt install python3-pip -y
                    
                    # Install Python dependencies
                    python3 -m pip install flask sqlalchemy pytest pytest-cov

                    # Run tests with coverage
                    pytest --maxfail=1 --disable-warnings --cov=. --cov-report=xml
                '''
            }
        }

        stage('SonarQube Scan') {
            steps {
                echo "🔍 Running SonarQube scan..."
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
                echo '⏳ Quality Gate check (optional, currently not aborting)...'
                script {
                    timeout(time: 15, unit: 'MINUTES') {
                        // If you want to enforce Quality Gate, uncomment below
                        // def qg = waitForQualityGate abortPipeline: true
                        echo "Quality Gate step completed (pipeline continues)"
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

        stage('Docker Image Save') {
            steps {
                echo "💾 Saving Docker image as tar file..."
                sh '''
                    docker save -o ${IMAGE_NAME}.tar ${DOCKERHUB_USER}/${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Nexus Raw Upload') {
            steps {
                echo "📦 Uploading Docker image tar file to Nexus..."
                withCredentials([usernamePassword(credentialsId: 'nexus_credentials', 
                                                 usernameVariable: 'NEXUS_USER', 
                                                 passwordVariable: 'NEXUS_PASS')]) {
                    script {
                        nexusArtifactUploader (
                            nexusVersion: 'NEXUS3',
                            protocol: 'http',
                            nexusUrl: "${NEXUS_URL}",
                            groupId: 'com.jenkins.demo',
                            version: '1.0.0',
                            repository: 'docker-repo',
                            artifacts: [[artifactId: 'flask-mongo-app', 
                                         classifier: '', 
                                         file: "${WORKSPACE}/${IMAGE_NAME}.tar", 
                                         type: 'tar',
                                         version: '1.0.0']], 
                            credentialsId: 'nexus_credentials'
                        )
                    }
                }
            }
        }

        stage('Deploy with Docker Compose') {
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
