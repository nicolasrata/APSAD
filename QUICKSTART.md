# 🚀 Guide de démarrage rapide

## ⚡ Deux versions disponibles

### Version 1 : Texte simple et lisible (recommandée) 📖

```bash
python3 reconstruct_local.py
```

**Résultat :** Document moderne et épuré avec le texte extrait  
**Fichier généré :** `APSAD_D20_Document_Complet.html`

**Avantages :**
- ✅ Très lisible à l'écran
- ✅ Texte facilement sélectionnable
- ✅ Recherche efficace (Cmd+F)
- ✅ Léger et rapide

### Version 2 : Avec mise en page originale 🎨

```bash
python3 reconstruct_with_layout.py
```

**Résultat :** Document avec positions CSS et mise en page préservée  
**Fichier généré :** `APSAD_D20_Document_Avec_Mise_En_Page.html`

**Avantages :**
- ✅ Fidèle au PDF original
- ✅ Positions et alignements préservés
- ✅ Aspect visuel identique
- ✅ Bon pour l'impression

---

## 📥 Installation rapide

### 1️⃣ Télécharge le dépôt

**Option A - Avec Git:**
```bash
git clone https://github.com/nicolasrata/APSAD.git
cd APSAD
```

**Option B - Sans Git (ZIP):**
1. Va sur https://github.com/nicolasrata/APSAD
2. Clique sur **"Code"** > **"Download ZIP"**
3. Décompresse le ZIP
4. Ouvre un terminal dans le dossier

### 2️⃣ Installe la dépendance

```bash
pip3 install beautifulsoup4
```

### 3️⃣ Génère le document

**Pour un document lisible :**
```bash
python3 reconstruct_local.py
```

**Pour conserver la mise en page :**
```bash
python3 reconstruct_with_layout.py
```

---

## 🍎 Sur macOS - Méthode automatique

```bash
chmod +x generer_document.sh
./generer_document.sh
```

Le script fait tout automatiquement (utilise la version texte simple).

---

## 📊 Comparaison des versions

| Caractéristique | Version texte simple | Version avec mise en page |
|----------------|---------------------|--------------------------|
| Lisibilité | 🟢 Excellente | 🟡 Comme le PDF |
| Fidélité visuelle | 🟡 Structure | 🟢 Identique |
| Recherche texte | 🟢 Parfaite | 🟢 Bonne |
| Poids fichier | 🟢 Léger | 🟡 Moyen |
| Sélection texte | 🟢 Facile | 🟢 Bonne |
| Impression | 🟢 Bonne | 🟢 Excellente |
| **Recommandé pour** | Lecture | Archive/impression |

---

## 📄 Ouvrir le document généré

```bash
# Ouvrir automatiquement
open APSAD_D20_Document_Complet.html

# ou
open APSAD_D20_Document_Avec_Mise_En_Page.html
```

Ou double-clique sur le fichier dans le Finder ! 🖱️

---

## 🐛 Problèmes fréquents

### "No module named 'bs4'"
```bash
pip3 install beautifulsoup4
```

Si ça ne fonctionne pas :
```bash
python3 -m pip install beautifulsoup4
```

### "Aucun fichier HTML trouvé"
Vérifie que tu es dans le bon dossier :
```bash
ls *.html
```

Tu dois voir les fichiers du référentiel APSAD.

### Le texte n'apparaît pas
Utilise la **nouvelle version** :
```bash
python3 reconstruct_with_layout.py
```

---

## 🎯 Quelle version choisir ?

**Utilise `reconstruct_local.py` si :**
- Tu veux **lire** le document à l'écran
- Tu vas faire des **recherches** dans le texte
- Tu veux quelque chose de **moderne et épuré**

**Utilise `reconstruct_with_layout.py` si :**
- Tu veux l'**apparence exacte** du PDF
- Tu vas **imprimer** le document
- Tu as besoin des **positions précises**

---

## ⏱️ Temps estimé

- Installation des dépendances : **1 minute**
- Génération du document : **30 secondes**
- **Total : ~2 minutes** ⚡

---

## 📞 Besoin d'aide ?

- 📖 [Documentation complète](README.md)
- 📂 [Liste des fichiers](FILES.md)
- 🐛 [Signaler un problème](https://github.com/nicolasrata/APSAD/issues)

---

**Bonne lecture ! 📚✨**
