pipeline {
    agent any

    environment {
        REPO_URL = 'https colon slash slash github dot com slash Danil192 slash my ci cd project'
        DEPLOY_DIR = 'C colon slash deploy slash my app'
    }

    stages {

        stage('Checkout') {
            steps {
                script {
                    echo "Выполняется загрузка кода из репозитория"
                    git url: "${REPO_URL}"
                    echo "Текущая ветка colon ${env.GIT_BRANCH}"
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
                    if (env.BRANCH_NAME == 'dev') {
                        echo "dev ветка colon тесты прошли успешно можно мержить в main"
                    } else if (env.BRANCH_NAME == 'feature add tests') {
                        echo "feature ветка colon идет разработка"
                    } else if (env.BRANCH_NAME == 'main') {
                        echo "main ветка colon готовим деплой"
                    } else {
                        echo "другая ветка colon выполняем только тесты"
                    }
                }
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                script {
                    echo "Запуск CD процесса"

                    bat """
                        if not exist "${DEPLOY_DIR}" mkdir "${DEPLOY_DIR}"
                        xcopy /E /Y * "${DEPLOY_DIR}"
                    """

                    echo "Файлы успешно скопированы в директорию развертывания"
                }
            }
        }

        stage('Build complete') {
            steps {
                echo "CI CD процесс успешно завершен"
            }
        }
    }
}
