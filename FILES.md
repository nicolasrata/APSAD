# 📦 Fichiers du projet APSAD D20

## 📝 Scripts de reconstruction

### Scripts principaux
- **`reconstruct_local.py`** ⭐ - Script recommandé, fonctionne hors ligne avec fichiers locaux
- **`reconstruct_simple.py`** - Télécharge depuis GitHub et crée un document moderne
- **`reconstruct_document.py`** - Version complète qui préserve la mise en page originale

### Scripts automatiques (1 clic)
- **`generer_document.bat`** 🪟 - Pour Windows (double-clic)
- **`generer_document.sh`** 🐧🍎 - Pour Linux/Mac (chmod +x puis ./script)

## 📚 Documentation

- **`README.md`** - Documentation complète du projet
- **`QUICKSTART.md`** - Guide de démarrage rapide
- **`FILES.md`** - Ce fichier (index des fichiers)

## 🔧 Configuration

- **`requirements.txt`** - Dépendances Python (beautifulsoup4, requests)
- **`.gitignore`** - Fichiers à ignorer dans Git

## 📄 Fichiers HTML sources

Tous les fichiers HTML du référentiel APSAD D20 :
- Pages liminaires
- Sommaire
- Chapitres 1-8
- Annexes 1-12

## 🎯 Fichiers générés (ignorés par Git)

Ces fichiers sont créés par les scripts et ne sont pas versionnés :
- `APSAD_D20_Document_Complet.html` - Document HTML complet
- `APSAD_D20_Document_Simplifie.html` - Version simplifiée

## 🚀 Utilisation rapide

### Windows
```batch
generer_document.bat
```

### Linux/Mac
```bash
chmod +x generer_document.sh
./generer_document.sh
```

### Ligne de commande universelle
```bash
pip install beautifulsoup4
python reconstruct_local.py
```

## 📊 Arborescence du projet

```
APSAD/
├── 📝 Scripts Python
│   ├── reconstruct_local.py          ⭐ Recommandé
│   ├── reconstruct_simple.py
│   └── reconstruct_document.py
│
├── 🔧 Scripts automatiques
│   ├── generer_document.bat          (Windows)
│   └── generer_document.sh           (Linux/Mac)
│
├── 📚 Documentation
│   ├── README.md                     Documentation principale
│   ├── QUICKSTART.md                 Guide rapide
│   └── FILES.md                      Ce fichier
│
├── ⚙️ Configuration
│   ├── requirements.txt              Dépendances
│   └── .gitignore                    Exclusions Git
│
└── 📄 Sources HTML
    ├── [Pages liminaires].html
    ├── [Sommaire].html
    ├── [Chapitre 1-8].html
    └── [Annexe 1-12].html
```

## ❓ Quel script utiliser ?

| Situation | Script recommandé |
|-----------|------------------|
| 🆕 Première utilisation | `generer_document.bat/.sh` |
| 💻 Ligne de commande | `reconstruct_local.py` |
| 🌐 Depuis GitHub direct | `reconstruct_simple.py` |
| 📄 Fidélité au PDF | `reconstruct_document.py` |

## 🔗 Liens utiles

- [Guide de démarrage](QUICKSTART.md)
- [Documentation complète](README.md)
- [Dépôt GitHub](https://github.com/nicolasrata/APSAD)
- [Signaler un bug](https://github.com/nicolasrata/APSAD/issues)

---

*Dernière mise à jour : Octobre 2024*
