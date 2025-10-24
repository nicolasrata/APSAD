# 🚀 Guide de démarrage rapide

## Installation en 3 étapes

### 1️⃣ Clone le dépôt

```bash
git clone https://github.com/nicolasrata/APSAD.git
cd APSAD
```

### 2️⃣ Installe les dépendances

```bash
pip install -r requirements.txt
```

### 3️⃣ Génère le document

**Pour une version moderne et lisible :**
```bash
python reconstruct_simple.py
```

**Pour une version fidèle à l'original :**
```bash
python reconstruct_document.py
```

## 📄 Résultat

Les scripts créent des fichiers HTML que tu peux ouvrir avec n'importe quel navigateur :

- `APSAD_D20_Document_Simplifie.html` - Version optimisée pour lecture
- `APSAD_D20_Document_Complet.html` - Version avec mise en page originale

## 🎯 Utilisation

Double-clique simplement sur le fichier HTML généré pour l'ouvrir dans ton navigateur !

## 💡 Astuce

Pour une lecture confortable, utilise le mode lecture de ton navigateur (F9 dans Firefox, ou icône de livre dans la barre d'adresse).

## ❓ Besoin d'aide ?

Consulte le [README.md](README.md) complet pour plus de détails et d'options avancées.

## 📱 Sur mobile

Tu peux même lancer les scripts depuis Termux (Android) :

```bash
pkg install python git
git clone https://github.com/nicolasrata/APSAD.git
cd APSAD
pip install -r requirements.txt
python reconstruct_simple.py
```

Puis ouvre le fichier HTML avec ton navigateur mobile.
