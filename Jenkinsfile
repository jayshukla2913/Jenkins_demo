pipeline {
    agent any

    environment {
        // Adjust these to match your Jenkins configuration / credentials IDs
        SONAR_SERVER_NAME = 'Jenkins_Master_Sonarqube'
        SONAR_SCANNER_TOOL = 'Sonar_Master_Scanner'
        SONAR_TOKEN = credentials('Sonarqube_master_token')

        DOCKERHUB_USER = 'jayshukla2913'
        IMAGE_NAME = 'flask-mongo-app'

        NEXUS_CREDENTIALS = 'nexus_master_credentials'
        DOCKERHUB_CREDENTIALS = 'Docker_Master_Credentials'
    }

    stages {
        stage('Checkout') {
            steps {
                echo "📥 Checking out source..."
                checkout scm
            }
        }

        stage('Ensure venv & Install Python deps') {
            steps {
                echo "🐍 Ensure venv exists and install Python test dependencies..."
                sh '''
                    set -e

                    # remove stale pytest cache and compiled files to avoid import mismatches
                    find . -type d -name "__pycache__" -exec rm -rf {} + || true
                    rm -rf .pytest_cache || true

                    # create venv if missing
                    if [ ! -d "venv" ]; then
                        python3 -m venv venv
                    fi

                    # Use bash -lc so 'source' works reliably
                    bash -lc "source venv/bin/activate && python -m pip install --upgrade pip && pip install flask sqlalchemy pytest pytest-cov"
                '''
            }
        }

        stage('Run Tests & Generate Coverage') {
            steps {
                echo "🧪 Running pytest and generating coverage.xml..."
                sh '''
                    set -e

                    # ensure caches are clean
                    find . -type d -name "__pycache__" -exec rm -rf {} + || true
                    rm -rf .pytest_cache || true

                    # run tests - explicitly reference test file(s)
                    bash -lc "source venv/bin/activate && pytest test_app.py --maxfail=1 --disable-warnings --cov=app --cov-report=xml"
                '''
            }
        }

        stage('SonarQube Scan') {
            steps {
                echo "🔍 Running SonarQube scanner (using Jenkins tool)..."
                script {
                    // resolve scanner installation directory from Jenkins tools
                    def scannerHome = tool name: "${SONAR_SCANNER_TOOL}", type: 'hudson.plugins.sonar.SonarRunnerInstallation'
                    withSonarQubeEnv("${SONAR_SERVER_NAME}") {
                        sh """
                            set -e
                            # activate venv so sonar-scanner can pick up any python env if needed (not required for scanner itself)
                            bash -lc "source venv/bin/activate && ${scannerHome}/bin/sonar-scanner \
                              -Dsonar.projectKey=flask-app \
                              -Dsonar.sources=. \
                              -Dsonar.python.coverage.reportPaths=coverage.xml \
                              -Dsonar.host.url=http://http://13.219.17.222:9000 \
                              -Dsonar.login=${SONAR_TOKEN}"
                        """
                    }
                }
            }
        }

         stage('Quality Gate') {
             steps {
                timeout(time: 15, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                 }
             }
         }
    


        stage('Docker Build & Push') {
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

        stage('Deploy (Docker Compose)') {
            steps {
                echo "🚀 Deploying with docker compose..."
                sh '''
                    set -e
                    docker compose down || true
                    docker compose pull || true
                    docker compose up -d
                '''
            }
        }
    }

    post {
        always {
            echo "🧹 Cleanup: remove venv, caches"
            sh '''
                set +e
                rm -rf venv
                find . -type d -name "__pycache__" -exec rm -rf {} + || true
                rm -rf .pytest_cache coverage.xml || true
            '''
        }
        success {
            echo "✅ Pipeline succeeded"
        }
        failure {
            echo "❌ Pipeline failed — check console output"
        }
    }
}
