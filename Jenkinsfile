
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

        stage('Run Django Tests') {
            steps {
                bat 'docker run --rm inventory-billing-system python manage.py test'
            }
        }
    }

    post {
        success {
            echo 'All CI stages completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check Console Output.'
        }
    }
}
