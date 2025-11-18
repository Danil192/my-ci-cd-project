pipeline {
    agent any

    environment {
        DEPLOY_DIR = "C:/deploy/my_app"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Ветка из которой выполняется сборка: ${env.BRANCH_NAME}"
                echo "Код уже скачан Jenkins автоматически"
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
                    if (env.BRANCH_NAME == 'dev') {
                        echo "dev ветка, тестируем новый код"
                    } else if (env.BRANCH_NAME == 'feature/add-tests') {
                        echo "feature ветка, идёт разработка"
                    } else if (env.BRANCH_NAME == 'main') {
                        echo "main ветка, готовим деплой"
                    } else {
                        echo "неизвестная ветка, просто тестируем"
                    }
                }
            }
        }

        stage('Deploy') {
            when {
                branch "dev"
            }
            steps {
                script {
                    echo "Запуск CD деплоя"

                    bat """
                        if not exist "${DEPLOY_DIR}" mkdir "${DEPLOY_DIR}"
                        xcopy /E /Y * "${DEPLOY_DIR}"
                    """

                    echo "Деплой выполнен успешно"
                }
            }
        }

        stage('Build complete') {
            steps {
                echo "CI CD процесс завершен"
            }
        }
    }
}
