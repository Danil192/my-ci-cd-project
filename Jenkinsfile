pipeline {
    agent any

    environment {
        DEPLOY_DIR = "C:/deploy/my_app"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Код скачан Jenkins автоматически"
            }
        }

        stage('Detect branch') {
            steps {
                script {
                    // получаем имя remote ветки
                    def ref = bat(
                        script: 'git symbolic-ref --short HEAD || git rev-parse --abbrev-ref HEAD',
                        returnStdout: true
                    ).trim()

                    // если Jenkins дал detached HEAD
                    if (ref == 'HEAD') {
                        def commit = bat(
                            script: 'git rev-parse HEAD',
                            returnStdout: true
                        ).trim()

                        // ищем имя ветки по хэшу
                        def branches = bat(
                            script: 'git branch -r --contains ' + commit,
                            returnStdout: true
                        ).trim()

                        // первые 1–2 строки обычно origin/dev или origin/main
                        def realBranch = branches.split("\n")[0].trim()
                        realBranch = realBranch.replace("origin/", "")

                        env.BRANCH_NAME = realBranch
                    } else {
                        env.BRANCH_NAME = ref
                    }

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
                    switch(env.BRANCH_NAME) {
                        case 'dev':
                            echo "dev ветка, тестируем новый код"
                            break
                        case 'feature/add-tests':
                            echo "feature ветка, идёт разработка"
                            break
                        case 'main':
                            echo "main ветка, готовим деплой"
                            break
                        default:
                            echo "неизвестная ветка, просто тестируем"
                    }
                }
            }
        }

        stage('Deploy') {
            when {
                expression { env.BRANCH_NAME == 'dev' }
            }
            steps {
                script {
                    echo "Запуск CD деплоя, слияние dev → main"

                    def currentBranch = env.BRANCH_NAME

                    bat """
                        git config user.name "Jenkins"
                        git config user.email "jenkins@ci-cd"
                        git fetch origin main
                        git checkout main
                        git merge ${currentBranch} -m "Auto-merge ${currentBranch} into main [Build #${env.BUILD_NUMBER}]"
                        git push origin main
                    """

                    echo "Деплой выполнен успешно"
                }
            }
        }

        stage('Build complete') {
            steps {
                echo "CI CD процесс завершён"
            }
        }
    }
}
