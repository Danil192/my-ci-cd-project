pipeline {
    agent any

    environment {
        DEPLOY_DIR = "C:/deploy/my_app"
        PYTHON = "python"
    }

    stages {

        stage('Checkout SCM') {
            steps {
                echo "Ветка из которой идет сборка: ${env.BRANCH_NAME}"
                echo "Код был скачан Jenkins автоматически"
            }
        }

        stage('Install dependencies') {
            steps {
                bat """
                    ${PYTHON} -m pip install --upgrade pip
                    ${PYTHON} -m pip install -r requirements.txt
                """
            }
        }

        stage('Run tests') {
            steps {
                echo "Запуск тестов проекта"
                bat "pytest --maxfail=1 --disable-warnings -q"
            }
        }

        stage('Branch logic') {
            steps {
                script {
                    if (env.BRANCH_NAME == 'dev') {
                        echo "dev ветка, идет активная разработка и тестирование"
                    } else if (env.BRANCH_NAME == 'feature/add-tests') {
                        echo "feature ветка, разработка нового функционала"
                    } else if (env.BRANCH_NAME == 'main') {
                        echo "main ветка, код готов к боевому деплою"
                    } else {
                        echo "неизвестная ветка, выполняем только CI проверку"
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
                    echo "Запуск CD деплоя, подготовка директории"

                    bat """
                        if not exist "${DEPLOY_DIR}" mkdir "${DEPLOY_DIR}"
                        xcopy /E /Y * "${DEPLOY_DIR}"
                    """

                    echo "Деплой завершен успешно"
                }
            }
        }

        stage('Build complete') {
            steps {
                echo "CI CD процесс завершен, пайплайн отработал корректно"
            }
        }
    }

    post {
        success {
            echo "Сборка прошла успешно"
        }
        failure {
            echo "Сборка упала"
        }
    }
}
