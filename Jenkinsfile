
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out Inventory and Billing System from GitHub'
                git branch: 'main',
                    url: 'https://github.com/divyaaa2005/InventoryBillingSystem.git'
            }
        }

        stage('Verify Project') {
            steps {
                echo 'GitHub repository cloned successfully!'
                bat 'dir'
            }
        }
    }
}
