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
                    echo "Текущая ветка: ${env.GIT_BRANCH}"
                    git branch: 'dev', url: "${REPO_URL}"
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
                    if (env.GIT_BRANCH == 'origin/dev' || env.BRANCH_NAME == 'dev') {
                        echo "Это dev ветка, тесты прошли успешно"
                    } else if (env.GIT_BRANCH == 'origin/feature/add-tests' || env.BRANCH_NAME == 'feature/add-tests') {
                        echo "Это feature ветка, идет разработка"
                    } else if (env.GIT_BRANCH == 'origin/main' || env.BRANCH_NAME == 'main') {
                        echo "Это main ветка, готовим деплой"
                    } else {
                        echo "Неизвестная ветка, только тестируем"
                    }
                }
            }
        }

        stage('Deploy') {
            when {
                anyOf {
                    environment name: 'BRANCH_NAME', value: 'main'
                    expression { return env.GIT_BRANCH == 'origin/main' }
                }
            }
            steps {
                script {
                    echo "Запуск CD процесса"

                    bat """
                        if not exist "${DEPLOY_DIR}" mkdir "${DEPLOY_DIR}"
                        xcopy /E /Y * "${DEPLOY_DIR}"
                    """

                    echo "Файлы скопированы в папку развертывания"
                }
            }
        }

        stage('Build complete') {
            steps {
                echo 'Все этапы CI CD завершены'
            }
        }
    }
}
