@echo off
cd /d "%~dp0"
title MB Bank Alert - Ultimate Build Tool
setlocal enabledelayedexpansion

echo =========================================
echo   MB Bank Alert -- Ultimate Build Tool
echo =========================================

:: BUOC 0: KIEM TRA PYTHON 
python --version >nul 2>&1
if not errorlevel 1 goto :PYTHON_FOUND

echo [!] Python khong tim thay. Dang chuan bi tai...

set "PY_URL=https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe"
set "PY_INST=%temp%\python_312_installer.exe"

curl -L -o "%PY_INST%" "%PY_URL%"

if not exist "%PY_INST%" (
    echo [FAIL] Khong tai duoc bo cai Python.
    pause
    exit /b 1
)

echo [+] Dang cai dat Python (Silent Mode)...
start /wait "" "%PY_INST%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
del /f /q "%PY_INST%"
echo [OK] Cai dat hoan tat. Vui long chay lai file .bat nay.
pause
exit /b 0

:PYTHON_FOUND
echo [OK] Da tim thay Python.

:: BUOC 1: KHOI TAO VENV
set VENV_DIR=venv
echo.
echo [1/5] Tao virtual environment (venv)...
if not exist %VENV_DIR% (
    python -m venv %VENV_DIR%
)

set VENV_PYTHON=%VENV_DIR%\Scripts\python.exe
set VENV_PIP=%VENV_DIR%\Scripts\pip.exe
set VENV_PYINSTALLER=%VENV_DIR%\Scripts\pyinstaller.exe

:: BUOC 2: CAI THU VIEN
echo.
echo [2/4] Cai dat thu vien...
%VENV_PYTHON% -m pip install --upgrade pip --quiet
%VENV_PIP% install -r requirements.txt --quiet
if errorlevel 1 (
    echo [FAIL] Cai dat thu vien that bai.
    pause
    exit /b 1
)

:: BUOC 3: BUILD EXE
echo.
echo [3/4] Dang dong goi EXE Standalone...
if exist dist rmdir /s /q dist

%VENV_PYINSTALLER% --onedir --contents-directory _internal ^
    --console --name "MB_Bank_Alert" ^
    --add-data "sounds;sounds" ^
    --hidden-import=pygame ^
    --hidden-import=paho.mqtt.client ^
    --hidden-import=dotenv ^
    --collect-all paho ^
    --collect-all pygame ^
    --noconfirm mb_bank_alert.py

if errorlevel 1 (
    echo [FAIL] Build EXE that bai.
    pause
    exit /b 1
)

:: BUOC 4: COPY FILE
echo.
echo [4/5] Hoan thien thu muc san pham...
set "DIST_APP_FOLDER=dist\MB_Bank_Alert"

:: Luon uu tien dung file .env.example de copy sang dist\.env (Bao mat)
if exist .env.example (
    copy /y .env.example "%DIST_APP_FOLDER%\.env" > nul
) else if exist .env (
    :: Neu khong co file mau thi moi copy file hien tai
    copy /y .env "%DIST_APP_FOLDER%\.env" > nul
)
if exist HUONG_DAN.md copy /y HUONG_DAN.md "%DIST_APP_FOLDER%\HUONG_DAN.md" > nul

:: BUOC 5: NEN ZIP
echo.
echo [5/5] Dang nen Zip toan bo thu muc san pham vao dist...
set "ZIP_NAME=dist\MB_Bank_Alert_Full_Package.zip"
if exist "%ZIP_NAME%" del /f /q "%ZIP_NAME%"

:: Dung lenh tar co san tren Windows de nen vao trong thu muc dist
tar -a -c -f "%ZIP_NAME%" -C dist MB_Bank_Alert

echo.
echo =========================================
echo   HOAN TAT! MOI THU DA DUOC DONG GOI.
echo =========================================
echo   [+] Vi tri san pham: %cd%\dist\MB_Bank_Alert\
echo   [+] File Nen: %cd%\%ZIP_NAME%
echo =========================================
pause
