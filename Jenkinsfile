pipeline {
    agent any

    environment {
        GIT_REPO = "https://github.com/Danil192/my-ci-cd-project.git"
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
                    @echo off
                    chcp 65001 >nul
                    
                    REM Попытка 1: python3
                    python3 --version >nul 2>&1
                    if %errorlevel% equ 0 (
                        echo Используется Python: python3
                        python3 -m pip install --upgrade pip
                        if %errorlevel% neq 0 exit /b 1
                        python3 -m pip install -r requirements.txt
                        if %errorlevel% neq 0 exit /b 1
                        exit /b 0
                    )
                    
                    REM Попытка 2: python (проверяем версию)
                    python --version >nul 2>&1
                    if %errorlevel% equ 0 (
                        python --version | findstr /R "^Python 3\\." >nul
                        if %errorlevel% equ 0 (
                            echo Используется Python: python
                            python -m pip install --upgrade pip
                            if %errorlevel% neq 0 exit /b 1
                            python -m pip install -r requirements.txt
                            if %errorlevel% neq 0 exit /b 1
                            exit /b 0
                        )
                    )
                    
                    echo Ошибка: Python 3 не найден! Установите Python 3 и добавьте его в PATH
                    exit /b 1
                """
            }
        }

        stage('Run tests') {
            steps {
                echo "запуск тестов идем жестко"
                bat """
                    @echo off
                    
                    REM Попытка 1: python3
                    python3 --version >nul 2>&1
                    if %errorlevel% equ 0 (
                        python3 -m pytest --maxfail=1 --disable-warnings -q
                        exit /b %errorlevel%
                    )
                    
                    REM Попытка 2: python (проверяем версию)
                    python --version >nul 2>&1
                    if %errorlevel% equ 0 (
                        python --version | findstr /R "^Python 3\\." >nul
                        if %errorlevel% equ 0 (
                            python -m pytest --maxfail=1 --disable-warnings -q
                            exit /b %errorlevel%
                        )
                    )
                    
                    echo Ошибка: Python 3 не найден для запуска тестов
                    exit /b 1
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
                    def currentBranch = env.BRANCH_NAME ?: env.GIT_BRANCH?.replaceAll('origin/', '') ?: 'unknown'
                    echo "Текущая ветка: ${currentBranch}"
                    echo "Выполняется merge в ветку main"
                    
                    bat """
                        git config user.name "Jenkins"
                        git config user.email "jenkins@ci-cd"
                        git fetch origin main
                        git checkout main
                        git merge ${currentBranch} -m "Merge ${currentBranch} into main [Build #${env.BUILD_NUMBER}]"
                        git push origin main
                    """
                    
                    echo "Merge в main завершен"
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

