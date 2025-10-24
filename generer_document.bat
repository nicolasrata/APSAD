@echo off
REM Script Windows pour reconstruire le document APSAD D20
echo.
echo ========================================
echo  Reconstruction Document APSAD D20
echo ========================================
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installé!
    echo.
    echo Télécharge Python sur https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [OK] Python détecté
echo.

REM Installer beautifulsoup4 si nécessaire
echo Installation des dépendances...
pip install beautifulsoup4 --quiet
if errorlevel 1 (
    echo [ATTENTION] Problème lors de l'installation
    echo Essai de continuer...
)
echo.

REM Lancer le script
echo Génération du document...
echo.
python reconstruct_local.py

if errorlevel 1 (
    echo.
    echo [ERREUR] Le script a rencontré un problème
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Document créé avec succès!
echo ========================================
echo.
echo Le fichier APSAD_D20_Document_Complet.html a été créé.
echo Double-clique dessus pour l'ouvrir dans ton navigateur.
echo.
pause
