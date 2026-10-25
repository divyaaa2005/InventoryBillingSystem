
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from GitHub'
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
    }

    post {
        success {
            echo 'CI pipeline completed successfully!'
        }
        failure {
            echo 'CI pipeline failed. Check the console output.'
        }
    }
}
