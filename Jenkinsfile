pipeline {
    agent any

    environment {
        DEPLOY_DIR = "C:/deploy/my_app"
        PYTHON = "C:/Users/danil/AppData/Local/Programs/Python/Python312/python.exe"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "ветка идет такая извлекаем код: ${env.BRANCH_NAME}"
                echo "код взят Jenkins автоматически"
            }
        }

        stage('Install dependencies') {
            steps {
                bat """
                    chcp 65001 >nul
                    "${PYTHON}" -m pip install --upgrade pip
                    "${PYTHON}" -m pip install -r requirements.txt
                    if errorlevel 1 exit /b 1
                """
            }
        }

        stage('Run tests') {
            steps {
                echo "запуск тестов идем жестко"
                bat """
                    "${PYTHON}" -m pytest --maxfail=1 --disable-warnings -q
                """
            }
        }

        stage('Branch logic') {
            steps {
                script {
                    if (env.BRANCH_NAME == 'dev') {
                        echo "ветка dev идет работа"
                    } else if (env.BRANCH_NAME == 'feature/add-tests') {
                        echo "ветка feature идет разработка"
                    } else if (env.BRANCH_NAME == 'main') {
                        echo "ветка main готовим релиз"
                    } else {
                        echo "ветка неизвестна идет стандартная проверка"
                    }
                }
            }
        }

        stage('Deploy') {
            when {
                anyOf {
                    branch "dev"
                    branch "main"
                }
            }
            steps {
                script {
                    echo "деплой отключен но код оставляем на месте"

                    bat """
                        if not exist "${DEPLOY_DIR}" (
                            mkdir "${DEPLOY_DIR}"
                        )
                        if not exist "${DEPLOY_DIR}" (
                            echo Ошибка: не удалось создать папку "${DEPLOY_DIR}"
                            exit /b 1
                        )
                        xcopy /E /I /Y * "${DEPLOY_DIR}\\"
                        if errorlevel 1 (
                            echo Ошибка при копировании файлов
                            exit /b 1
                        )
                        echo Файлы успешно скопированы в "${DEPLOY_DIR}"
                    """

                    echo "деплой завершен"
                }
            }
        }

        stage('Build complete') {
            steps {
                echo "проект собран пайплайн завершен"
            }
        }
    }

    post {
        success {
            echo "сборка успешная саланга красавчик"
        }
        failure {
            echo "сборка упала надо чинить"
        }
    }
}
