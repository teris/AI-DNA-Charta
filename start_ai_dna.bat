@echo off
setlocal EnableDelayedExpansion

REM ========================================
REM AI-DNA Charta System Starter (Windows)
REM ========================================

echo.
echo 🧬 AI-DNA Charta System Starter
echo ================================
echo.

REM Farben für bessere Ausgabe (Windows 10+)
for /F %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"
set "GREEN=%ESC%[32m"
set "RED=%ESC%[31m"
set "YELLOW=%ESC%[33m"
set "BLUE=%ESC%[34m"
set "RESET=%ESC%[0m"

REM Prüfe ob Python installiert ist
python --version >nul 2>&1
if errorlevel 1 (
    echo %RED%❌ Python ist nicht installiert oder nicht im PATH%RESET%
    echo Bitte Python von https://python.org installieren
    pause
    exit /b 1
)

echo %GREEN%✅ Python gefunden%RESET%

REM Prüfe aktuelle Position
if not exist "examples\app.py" (
    echo %RED%❌ Skript muss im Hauptverzeichnis des AI-DNA-Charta Repos ausgeführt werden%RESET%
    echo Aktueller Pfad: %CD%
    echo Erwartete Dateien: examples\app.py, examples\deepseek_local\
    pause
    exit /b 1
)

echo %GREEN%✅ Repository-Struktur gefunden%RESET%

REM Wähle Modus
echo.
echo Wähle Startmodus:
echo [1] Vollständiges System (Charta + DeepSeek)
echo [2] Nur Charta-System (Port 5000)
echo [3] Nur DeepSeek Local (Port 8000)
echo [4] Development Setup (beide + Dependencies installieren)
echo [5] Kollaborations-Tool öffnen
echo.
set /p choice="Deine Wahl (1-5): "

if "%choice%"=="1" goto :full_system
if "%choice%"=="2" goto :charta_only
if "%choice%"=="3" goto :deepseek_only
if "%choice%"=="4" goto :dev_setup
if "%choice%"=="5" goto :collab_tool
echo %RED%❌ Ungültige Auswahl%RESET%
pause
exit /b 1

:dev_setup
echo.
echo %BLUE%🔧 Development Setup wird gestartet...%RESET%
echo.

REM Prüfe/Installiere pip-packages für app.py
echo Installiere Abhängigkeiten für app.py...
pip install flask requests pyyaml

REM Prüfe/Installiere pip-packages für deepseek_local
echo Installiere Abhängigkeiten für deepseek_local...
cd examples\deepseek_local
pip install -r requirements.txt
cd ..\..

echo %GREEN%✅ Development Setup abgeschlossen%RESET%
echo.
goto :full_system

:full_system
echo.
echo %BLUE%🚀 Starte vollständiges AI-DNA System...%RESET%
echo.

REM Terminal 1: Charta-System
echo Starte Charta-System (Port 5000)...
start "AI-DNA Charta System" cmd /k "cd /d "%CD%\examples" && python app.py"

REM Warte kurz damit Charta-System startet
timeout /t 3 /nobreak >nul

REM Terminal 2: DeepSeek Local
echo Starte DeepSeek Local (Port 8000)...
start "DeepSeek Local" cmd /k "cd /d "%CD%\examples\deepseek_local" && python deepseek_local.py --config=config.yaml"

REM Terminal 3: Web-Interface
timeout /t 5 /nobreak >nul
echo %GREEN%✅ Öffne Web-Interfaces...%RESET%
start http://localhost:5000
start http://localhost:8000
start docs\ai_charta_collaboration_tool.html

goto :finish

:charta_only
echo.
echo %BLUE%🏛️ Starte nur Charta-System...%RESET%
echo.
cd examples
python app.py
goto :finish

:deepseek_only
echo.
echo %BLUE%🤖 Starte nur DeepSeek Local...%RESET%
echo.

REM Prüfe ob Config-Parameter gewünscht
set /p config_file="Config-Datei (Enter für Standard 'config.yaml'): "
if "%config_file%"=="" set config_file=config.yaml

cd examples\deepseek_local
python deepseek_local.py --config=%config_file%
goto :finish

:collab_tool
echo.
echo %BLUE%🛠️ Öffne Kollaborations-Tool...%RESET%
echo.
start docs\ai_charta_collaboration_tool.html
start docs\index.html
echo %GREEN%✅ Kollaborations-Tools geöffnet%RESET%
goto :finish

:finish
echo.
echo %GREEN%✅ System gestartet!%RESET%
echo.
echo %YELLOW%📋 Nützliche Links:%RESET%
echo • Charta-System: http://localhost:5000
echo • DeepSeek Local: http://localhost:8000
echo • Kollaborations-Tool: docs\ai_charta_collaboration_tool.html
echo • Dokumentation: docs\index.html
echo.
echo %YELLOW%🔧 API Tests:%RESET%
echo curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d "{\"question\":\"Hallo!\"}"
echo curl http://localhost:5000/status
echo.

REM Warte auf Eingabe vor dem Schließen
echo Drücke eine beliebige Taste zum Beenden...
pause >nul
