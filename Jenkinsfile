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

        stage('Detect branch') {
            steps {
                script {
                    def branch = bat(script: 'git rev-parse --abbrev-ref HEAD', returnStdout: true)
                    env.BRANCH_NAME = branch
                    echo "Определенная ветка, ${env.BRANCH_NAME}"
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
                branch 'main'
            }
            steps {
                script {
                    echo "Запуск CD деплоя - merge в ветку main"
                    
                    def currentBranch = env.BRANCH_NAME ?: env.GIT_BRANCH?.replaceAll('origin/', '') ?: 'main'
                    
                    bat """
                        git config user.name "Jenkins"
                        git config user.email "jenkins@ci-cd"
                        git fetch origin main
                        git checkout main
                        git merge ${currentBranch} -m "Merge ${currentBranch} into main [Build #${env.BUILD_NUMBER}]"
                        git push origin main
                    """

                    echo "Деплой выполнен успешно - изменения отправлены в main"
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
