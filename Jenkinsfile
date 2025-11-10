pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/Danil192/my-ci-cd-project'
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
                        echo "Это dev-ветка: тесты успешно прошли, можно мёржить в main."
                    } else if (env.GIT_BRANCH == 'origin/feature/add-tests' || env.BRANCH_NAME == 'feature/add-tests') {
                        echo "Это feature-ветка: идёт отладка новых функций."
                    } else if (env.GIT_BRANCH == 'origin/main' || env.BRANCH_NAME == 'main') {
                        echo "Это main-ветка: стабильная сборка, можно выполнять деплой."
                    } else {
                        echo "Неизвестная ветка, просто тестируем код."
                    }
                }
            }
        }

        stage('Build complete') {
            steps {
                echo 'Все этапы пайплайна успешно завершены.'
            }
        }
    }
}
