#!/bin/bash

# Script Linux/Mac pour reconstruire le document APSAD D20

echo ""
echo "========================================"
echo " Reconstruction Document APSAD D20"
echo "========================================"
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null
then
    echo "[ERREUR] Python n'est pas installé!"
    echo ""
    echo "Installation:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    echo "  macOS: brew install python3"
    echo ""
    exit 1
fi

# Utiliser python3 si disponible, sinon python
if command -v python3 &> /dev/null; then
    PYTHON=python3
    PIP=pip3
else
    PYTHON=python
    PIP=pip
fi

echo "[OK] Python détecté ($($PYTHON --version))"
echo ""

# Installer beautifulsoup4 si nécessaire
echo "Installation des dépendances..."
$PIP install beautifulsoup4 --quiet 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[ATTENTION] Problème lors de l'installation"
    echo "Essai de continuer..."
fi
echo ""

# Lancer le script
echo "Génération du document..."
echo ""
$PYTHON reconstruct_local.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERREUR] Le script a rencontré un problème"
    exit 1
fi

echo ""
echo "========================================"
echo " Document créé avec succès!"
echo "========================================"
echo ""
echo "Le fichier APSAD_D20_Document_Complet.html a été créé."
echo ""
echo "Pour l'ouvrir:"
echo "  Linux: xdg-open APSAD_D20_Document_Complet.html"
echo "  macOS: open APSAD_D20_Document_Complet.html"
echo ""
