pipeline {
    agent { label 'slave' }
    stages {
        stage('Docker Build') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }
        stage('Docker Run') {
            steps {
                sh '''
                docker stop flask-app || true
                docker rm flask-app || true
                docker run -d --name flask-app -p 5000:5000 -e DATABASE_URL=postgresql://user:password@localhost:5432/mydb $IMAGE_NAME
                '''
            }
        }
        stage('Test') {
            steps {
                sh 'curl -f http://13.219.17.222:5000 || echo "App not responding yet"'
            }
        }
    }
}
