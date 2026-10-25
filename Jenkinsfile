
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Code fetched from GitHub'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t inventory-billing-system .'
            }
        }

        stage('Django System Check') {
            steps {
                bat 'docker run --rm inventory-billing-system python manage.py check'
            }
        }

        stage('Start Services') {
            steps {
                bat '"C:\\Users\\DIVYADARSHNI  KUMAR\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker-compose.exe" up -d --build'
            }
        }

        stage('Run Django Tests') {
            steps {
                bat '"C:\\Users\\DIVYADARSHNI  KUMAR\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker-compose.exe" exec -T web python manage.py test inventory'
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Docker build, Django check, and tests completed!'
        }

        failure {
            echo 'FAILED: Check the Console Output for the error.'
        }
    }
}
