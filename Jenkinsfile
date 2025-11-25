pipeline {
    agent any

    environment {
        DEPLOY_DIR = "C:/deploy/my_app"
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
                    
                    REM Попытка использовать py -3 (Python 3 через Launcher)
                    py -3 --version >nul 2>&1
                    if %errorlevel% == 0 (
                        set PYTHON_CMD=py -3
                        goto :found
                    )
                    
                    REM Попытка использовать python3 из PATH
                    python3 --version >nul 2>&1
                    if %errorlevel% == 0 (
                        set PYTHON_CMD=python3
                        goto :found
                    )
                    
                    REM Попытка использовать py (Python Launcher для Windows)
                    py --version >nul 2>&1
                    if %errorlevel% == 0 (
                        REM Проверяем версию Python
                        for /f "tokens=2" %%i in ('py --version 2^>nul') do (
                            echo %%i | findstr /R "^3\\." >nul
                            if %errorlevel% == 0 (
                                set PYTHON_CMD=py
                                goto :found
                            )
                        )
                    )
                    
                    REM Попытка использовать python из PATH (только если версия 3.x)
                    python --version >nul 2>&1
                    if %errorlevel% == 0 (
                        for /f "tokens=2" %%i in ('python --version 2^>nul') do (
                            echo %%i | findstr /R "^3\\." >nul
                            if %errorlevel% == 0 (
                                set PYTHON_CMD=python
                                goto :found
                            )
                        )
                    )
                    
                    echo Ошибка: Python 3 не найден! Установите Python 3 и добавьте его в PATH
                    exit /b 1
                    
                    :found
                    echo Используется Python команда: %PYTHON_CMD%
                    %PYTHON_CMD% -m pip install --upgrade pip
                    if errorlevel 1 exit /b 1
                    %PYTHON_CMD% -m pip install -r requirements.txt
                    if errorlevel 1 exit /b 1
                """
            }
        }

        stage('Run tests') {
            steps {
                echo "запуск тестов идем жестко"
                bat """
                    @echo off
                    REM Попытка использовать py -3 (Python 3 через Launcher)
                    py -3 --version >nul 2>&1
                    if %errorlevel% == 0 (
                        py -3 -m pytest --maxfail=1 --disable-warnings -q
                        exit /b %errorlevel%
                    )
                    
                    REM Попытка использовать python3 из PATH
                    python3 --version >nul 2>&1
                    if %errorlevel% == 0 (
                        python3 -m pytest --maxfail=1 --disable-warnings -q
                        exit /b %errorlevel%
                    )
                    
                    REM Попытка использовать py (проверяем версию)
                    py --version >nul 2>&1
                    if %errorlevel% == 0 (
                        for /f "tokens=2" %%i in ('py --version 2^>nul') do (
                            echo %%i | findstr /R "^3\\." >nul
                            if %errorlevel% == 0 (
                                py -m pytest --maxfail=1 --disable-warnings -q
                                exit /b %errorlevel%
                            )
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
            steps {
                script {
                    // Определяем имя ветки из переменных окружения Jenkins
                    def branchName = env.BRANCH_NAME ?: env.GIT_BRANCH ?: 'unknown'
                    // Убираем префикс origin/ если есть
                    branchName = branchName.replaceAll('origin/', '')
                    
                    echo "Текущая ветка: ${branchName}"
                    
                    // Выполняем деплой только для веток dev и main
                    if (branchName == 'dev' || branchName == 'main') {
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
                    } else {
                        echo "Деплой пропущен для ветки: ${branchName} (выполняется только для dev и main)"
                    }
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

