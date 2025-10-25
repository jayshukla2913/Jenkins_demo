pipeline {
    agent { label 'slave' }
    stages {
        stage('Build') {
            steps {
                sh 'echo "Building on $(hostname)"'
                sh 'whoami'
            }
        }
        stage('Test') {
            steps {
                sh 'echo "Running tests..."'
            }
        }
    }
}
