pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'dev', url: 'https://github.com/Danil192/my-ci-cd-project'
            }
        }
        stage('Install dependencies') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }
        stage('Run tests') {
            steps {
                bat 'pytest --maxfail=1 --disable-warnings -q'
            }
        }
        stage('Build complete') {
            steps {
                echo 'Все тесты пройдены! Сборка завершена успешно.'
            }
        }
    }
}
