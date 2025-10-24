# 🚀 Guide de démarrage rapide

## ⚡ Solution ULTRA-RAPIDE (1 clic)

### Windows 🪟
1. Télécharge le ZIP du dépôt
2. Décompresse-le
3. **Double-clique sur `generer_document.bat`**

### Linux/Mac 🐧🍎
1. Télécharge le ZIP du dépôt
2. Décompresse-le
3. Ouvre un terminal dans le dossier
4. Lance :
```bash
chmod +x generer_document.sh
./generer_document.sh
```

**C'est tout !** Le document HTML sera créé automatiquement. 🎉

---

## 📥 Solution standard (ligne de commande)

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
- **Windows:** Double-clique sur le fichier HTML
- **Linux:** `xdg-open APSAD_D20_Document_Complet.html`
- **Mac:** `open APSAD_D20_Document_Complet.html`

## 🔧 Solutions alternatives

### Si tu veux télécharger depuis GitHub automatiquement

```bash
python reconstruct_simple.py
```

⚠️ Nécessite que le repo soit public ou un token GitHub configuré.

## 🎯 Utilisation du document

Une fois le HTML généré :
- 🔍 **Recherche** : Utilise Ctrl+F (Cmd+F sur Mac)
- 📱 **Mobile** : Le document s'adapte automatiquement
- 🖨️ **Impression** : Utilise Ctrl+P (la mise en page est optimisée)
- 🔖 **Navigation** : Clique sur la table des matières pour sauter entre chapitres

## 💡 Astuces

### Mode lecture
Pour une lecture confortable, utilise le mode lecture de ton navigateur :
- **Firefox** : F9 ou icône de livre
- **Chrome/Edge** : Extension "Reader View"
- **Safari** : Icône de paragraphe dans la barre d'adresse

### Recherche avancée
Pour chercher dans tout le document : Ctrl+F puis coche "Surligner tout" dans Firefox.

### Impression en PDF
Pour sauvegarder en PDF : Ctrl+P > Choisir "Imprimer vers PDF"

## 🐛 Problèmes fréquents

### Windows : "python n'est pas reconnu"
1. Installe Python depuis https://www.python.org/downloads/
2. ⚠️ Coche "Add Python to PATH" pendant l'installation
3. Redémarre ton terminal

### "No module named 'bs4'"
```bash
pip install beautifulsoup4
```

Si ça ne fonctionne pas :
```bash
python -m pip install beautifulsoup4
```

### "Aucun fichier HTML trouvé"
Assure-toi d'être dans le bon dossier (là où se trouvent les fichiers HTML du référentiel).

Vérifie avec :
- **Windows:** `dir *.html`
- **Linux/Mac:** `ls *.html`

### Erreur 404 avec l'API GitHub
Utilise `reconstruct_local.py` ou le script batch/shell à la place.

### Le fichier .sh n'est pas exécutable (Linux/Mac)
```bash
chmod +x generer_document.sh
```

## 📱 Sur mobile (Android)

Avec Termux (application gratuite) :

```bash
# Installation de Termux depuis F-Droid ou Play Store
pkg install python git
git clone https://github.com/nicolasrata/APSAD.git
cd APSAD
pip install beautifulsoup4
python reconstruct_local.py
```

Puis ouvre le fichier HTML avec ton navigateur mobile.

## ⏱️ Temps estimé

- **Avec script automatique** : 30 secondes
- **En ligne de commande** : 2-3 minutes
- **Première fois (installation Python)** : 5-10 minutes

## 📞 Besoin d'aide ?

- 📖 [Documentation complète](README.md)
- 🐛 [Signaler un problème](https://github.com/nicolasrata/APSAD/issues)
- 💬 Pose une question dans les Issues GitHub

---

**Tu as réussi ? Génial ! 🎉**

Ouvre maintenant `APSAD_D20_Document_Complet.html` dans ton navigateur et bonne lecture ! 📖
