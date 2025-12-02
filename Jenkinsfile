pipeline {
    agent any

    environment {
        DEPLOY_DIR = "C:/deploy/my_app"
    }

    stages {

        stage('Checkout') {
            steps {
                // Jenkins уже автоматически делает checkout нужной ветки
                echo "Код успешно загружен из репозитория"
            }
        }

        stage('Detect branch') {
            steps {
                script {
                    // Jenkins устанавливает GIT_BRANCH как, например, 'origin/dev'
                    env.BRANCH_NAME = env.GIT_BRANCH?.replace('origin/', '') ?: 'UNKNOWN'
                    echo "Определённая ветка: ${env.BRANCH_NAME}"
                }
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

        stage('Branch logic') {
            steps {
                script {
                    switch(env.BRANCH_NAME) {
                        case 'dev':
                            echo "Ветка dev: тестируем и готовим к развёртыванию"
                            break
                        case 'main':
                            echo "Ветка main: стабильная версия"
                            break
                        default:
                            echo "Неизвестная ветка: только тестирование"
                    }
                }
            }
        }

        stage('Deploy to disk') {
    when {
        branch 'dev'
    }
    steps {
        script {
            echo "Запуск CD: развёртывание на локальный диск C:"

            bat """
                if exist "C:\\deploy\\my_app" (
                    rmdir /s /q "C:\\deploy\\my_app"
                )
                mkdir /p "C:\\deploy\\my_app"
                robocopy . "C:\\deploy\\my_app" /E /XD .git
            """

            echo "Развёртывание завершено: приложение доступно в C:/deploy/my_app"
        }
    }
}

        stage('Build complete') {
            steps {
                echo "CI/CD процесс успешно завершён"
            }
        }
    }
}