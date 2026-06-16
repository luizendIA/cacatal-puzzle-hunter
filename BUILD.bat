@echo off
chcp 65001 >nul 2>&1
echo.
echo ====================================================
echo   CACATAL PUZZLE HUNTER - Build para .exe
echo ====================================================
echo.

REM Verificar se Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado!
    echo Instale o Python em: https://www.python.org/downloads/
    echo Marque "Add Python to PATH" durante a instalacao!
    pause
    exit /b 1
)

echo [1/3] Instalando PyInstaller...
python -m pip install pyinstaller --quiet

echo [2/3] Compilando puzzle_hunter.py para .exe...
echo Isso pode levar 1-2 minutos...
echo.

python -m PyInstaller --onefile --windowed --name "CacatalPuzzleHunter" --clean puzzle_hunter.py

echo.
if exist "dist\CacatalPuzzleHunter.exe" (
    echo ====================================================
    echo   SUCESSO! O .exe foi criado em:
    echo   dist\CacatalPuzzleHunter.exe
    echo ====================================================
    echo.
    echo Copie o arquivo .exe e distribua para a comunidade!
) else (
    echo [ERRO] Falha ao compilar. Verifique os erros acima.
)

echo.
pause
