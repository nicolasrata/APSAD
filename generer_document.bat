@echo off
REM Script Windows pour reconstruire le document APSAD D20
echo.
echo ========================================
echo  Reconstruction Document APSAD D20
echo  Version corrigee - Extraction amelioree
echo ========================================
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe!
    echo.
    echo Telecharge Python sur https://www.python.org/downloads/
    echo Coche "Add Python to PATH" lors de l'installation
    echo.
    pause
    exit /b 1
)

echo [OK] Python detecte
echo.

REM Installer beautifulsoup4 si nécessaire
echo Installation des dependances...
pip install beautifulsoup4 --quiet
if errorlevel 1 (
    echo [ATTENTION] Probleme lors de l'installation
    echo Essai de continuer...
)
echo.

REM Lancer le script
echo Generation du document...
echo.
python reconstruct_local.py

if errorlevel 1 (
    echo.
    echo [ERREUR] Le script a rencontre un probleme
    echo.
    echo Solutions:
    echo 1. Verifie que tu es dans le bon dossier
    echo 2. Verifie que les fichiers HTML sont presents
    echo 3. Essaie: python reconstruct_local.py
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Document cree avec succes!
echo ========================================
echo.
echo Le fichier APSAD_D20_Document_Complet.html a ete cree.
echo Double-clique dessus pour l'ouvrir dans ton navigateur.
echo.
pause
