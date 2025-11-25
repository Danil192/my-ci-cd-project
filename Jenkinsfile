pipeline {
    agent any

    environment {
        DEPLOY_DIR = "C:/deploy/my_app"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "код скачан Jenkins автоматически"
            }
        }

        stage('Fix checkout') {
            steps {
                bat "git checkout dev"
            }
        }

        stage('Detect branch') {
            steps {
                script {

                    def raw = bat(
                        script: 'git symbolic-ref --short HEAD || git rev-parse --abbrev-ref HEAD',
                        returnStdout: true
                    ).trim()

                    def lines = raw.readLines()
                    def ref = lines[-1].trim()

                    if (ref == 'HEAD') {

                        def commit = bat(
                            script: 'git rev-parse HEAD',
                            returnStdout: true
                        ).trim()

                        def rawBranches = bat(
                            script: "git branch -r --contains ${commit}",
                            returnStdout: true
                        ).trim()

                        def branchLines = rawBranches.readLines()
                        def realBranch = branchLines[-1].trim().replace("origin/", "")

                        env.BRANCH_NAME = realBranch.trim()

                    } else {
                        env.BRANCH_NAME = ref.trim()
                    }

                    echo "определенная ветка: ${env.BRANCH_NAME}"
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

                    echo "запуск CD деплоя, выполняем merge dev в main c авторазруливанием"

                    def currentBranch = env.BRANCH_NAME

                    bat """
                        git config user.name "Jenkins"
                        git config user.email "jenkins@ci-cd"
                        git fetch origin main
                        git checkout main
                        git merge ${currentBranch} -X theirs -m "auto merge ${currentBranch} into main, build ${env.BUILD_NUMBER}"
                        git push origin main
                    """

                    echo "деплой завершен успешно"
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
