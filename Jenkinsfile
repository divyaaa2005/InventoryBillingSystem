
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
                bat 'docker compose up -d --build'
            }
        }

        stage('Run Django Tests') {
            steps {
                bat 'docker compose exec -T web python manage.py test inventory'
            }
        }
    }

    post {
        success {
            echo 'All CI stages and Django tests completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check Console Output.'
        }
    }
}
