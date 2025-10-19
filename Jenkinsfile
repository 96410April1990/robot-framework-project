pipeline {
    agent any

    tools {
        python 'Python3'
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/your/repo.git'
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''
                python3 -m venv venv
                source venv/bin/activate
                pip install -r robot-framework-project/requirements.txt
                '''
            }
        }

        stage('Run Robot Tests') {
            steps {
                sh '''
                source venv/bin/activate
                robot -d robot-framework-project/ robot-framework-project/tests/
                '''
            }
        }

        stage('Publish Robot Report') {
            steps {
                robot outputPath: 'robot-framework-project/'
            }
        }
    }
}
