# 🚀 Guide de démarrage rapide

## ⚡ Solution RAPIDE (Recommandée)

### 1️⃣ Télécharge le dépôt

**Option A - Avec Git:**
```bash
git clone https://github.com/nicolasrata/APSAD.git
cd APSAD
```

**Option B - Sans Git (plus simple):**
1. Va sur https://github.com/nicolasrata/APSAD
2. Clique sur le bouton vert **"Code"**
3. Clique sur **"Download ZIP"**
4. Décompresse le ZIP
5. Ouvre un terminal dans le dossier décompressé

### 2️⃣ Installe les dépendances

```bash
pip install beautifulsoup4
```

### 3️⃣ Génère le document

```bash
python reconstruct_local.py
```

⚠️ **Important:** Les fichiers HTML doivent être dans le même dossier que le script !

## 📄 Résultat

Le script crée `APSAD_D20_Document_Complet.html` dans le dossier courant.

**Pour le consulter:**
- Double-clique sur le fichier HTML
- Ou ouvre-le avec ton navigateur préféré

## 🔧 Solutions alternatives

### Si tu as des problèmes avec l'API GitHub

Utilise `reconstruct_local.py` qui fonctionne avec les fichiers locaux (pas besoin d'API).

### Si tu veux utiliser l'API GitHub

Tu peux aussi utiliser les autres scripts, mais ils nécessitent que le repo soit public ou que tu configures un token GitHub :

```bash
# Configuration du token (si nécessaire)
export GITHUB_TOKEN="ton_token_ici"

# Puis lance
python reconstruct_simple.py
```

## 🎯 Utilisation

Une fois le HTML généré :
- 🔍 **Recherche** : Utilise Ctrl+F dans ton navigateur
- 📱 **Mobile** : Le document s'adapte automatiquement
- 🖨️ **Impression** : Utilise Ctrl+P (la mise en page est optimisée)
- 🔖 **Table des matières** : Clique sur les liens pour naviguer

## 💡 Astuce

Pour une lecture confortable, utilise le mode lecture de ton navigateur :
- **Firefox** : F9 ou icône de livre
- **Chrome/Edge** : Extension "Reader View"
- **Safari** : Icône de paragraphe dans la barre d'adresse

## 🐛 Problèmes fréquents

### "No module named 'bs4'"
```bash
pip install beautifulsoup4
```

### "Aucun fichier HTML trouvé"
Assure-toi d'être dans le bon dossier (là où se trouvent les fichiers HTML du référentiel).

### Erreur 404 avec l'API GitHub
Utilise `reconstruct_local.py` à la place des autres scripts.

## 📱 Sur mobile (Android)

Tu peux même lancer les scripts depuis Termux :

```bash
# Installation de Termux depuis F-Droid ou Play Store
pkg install python git
git clone https://github.com/nicolasrata/APSAD.git
cd APSAD
pip install beautifulsoup4
python reconstruct_local.py
```

Puis ouvre le fichier HTML avec ton navigateur mobile.

## 📞 Besoin d'aide ?

- 📖 [Documentation complète](README.md)
- 🐛 [Signaler un problème](https://github.com/nicolasrata/APSAD/issues)

---

**Temps estimé:** 2-3 minutes ⏱️
