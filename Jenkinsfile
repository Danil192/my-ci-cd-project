pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/Danil192/my-ci-cd-project'
        DEPLOY_DIR = 'C:/deploy/my_app'
    }

    stages {

        stage('Checkout') {
            steps {
                script {
                    echo "Выполняется загрузка кода из репозитория"
                    git url: "${REPO_URL}"
                    echo "Текущая ветка: ${env.GIT_BRANCH}"
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
                        echo "dev ветка, тесты прошли успешно"
                    } else if (env.BRANCH_NAME == 'feature/add-tests') {
                        echo "feature ветка, идет разработка"
                    } else if (env.BRANCH_NAME == 'main') {
                        echo "main ветка, готовим деплой"
                    } else {
                        echo "другая ветка, выполняем только тесты"
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
                echo "CI/CD процесс успешно завершен"
            }
        }
    }
}
