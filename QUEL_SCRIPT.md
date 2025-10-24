# 📋 Quel script utiliser ?

## 🎯 Choix rapide

### Tu veux LIRE le document ? 📖
```bash
python3 reconstruct_local.py
```
→ Génère `APSAD_D20_Document_Complet.html`

### Tu veux la MISE EN PAGE originale ? 🎨
```bash
python3 reconstruct_with_layout.py
```
→ Génère `APSAD_D20_Document_Avec_Mise_En_Page.html`

---

## 📊 Différences en détail

### `reconstruct_local.py` - Version texte simple
**Ce qu'il fait :**
- Extrait le texte de chaque page
- Regroupe les mots par ligne
- Présente le texte de manière linéaire
- Ajoute des séparateurs entre les pages

**Résultat :**
```
Chapitre 1 : Généralités
-------------------------
Ligne 1 de texte
Ligne 2 de texte
...
• • • (séparateur de page)
...
```

**Idéal pour :**
- ✅ Lire confortablement à l'écran
- ✅ Chercher du texte (Cmd+F)
- ✅ Copier-coller du contenu
- ✅ Navigation fluide

---

### `reconstruct_with_layout.py` - Version avec mise en page
**Ce qu'il fait :**
- Conserve les positions CSS originales
- Préserve les `div` avec `left`, `top`, etc.
- Garde la structure visuelle exacte
- Reproduit l'apparence du PDF

**Résultat :**
```html
<div style="left:108px; top:966px;">Texte</div>
<div style="left:143px; top:966px;">positionné</div>
```

**Idéal pour :**
- ✅ Avoir l'aspect exact du PDF
- ✅ Imprimer avec la mise en page originale
- ✅ Vérifier les positions des éléments
- ✅ Archivage fidèle

---

## 🚀 Installation et lancement

### Prérequis (une seule fois)
```bash
pip3 install beautifulsoup4
```

### Lancer le script choisi
```bash
# Version texte simple
python3 reconstruct_local.py

# Version avec mise en page
python3 reconstruct_with_layout.py
```

### Ouvrir le résultat
```bash
# Ouvrir automatiquement
open APSAD_D20_Document_Complet.html
# ou
open APSAD_D20_Document_Avec_Mise_En_Page.html
```

---

## 💡 Recommandations

| Situation | Script recommandé |
|-----------|------------------|
| Lire le document | `reconstruct_local.py` |
| Chercher une info | `reconstruct_local.py` |
| Imprimer | `reconstruct_with_layout.py` |
| Vérifier la mise en page | `reconstruct_with_layout.py` |
| Consultation quotidienne | `reconstruct_local.py` |
| Archive | `reconstruct_with_layout.py` |

---

## 🔍 Exemples de rendu

### Version texte simple
```
Référentiel APSAD D20
Installations photovoltaïques
. Édition septembre 2025

Type d'évaluation du système d'intégration
□ ATec
□ ATEx
□ ETN
```

### Version avec mise en page
Le texte apparaît exactement comme dans le PDF, avec les mêmes positions, espacements et alignements.

---

## ⚙️ Scripts automatiques

### macOS / Linux
```bash
chmod +x generer_document.sh
./generer_document.sh
```
→ Utilise `reconstruct_local.py` automatiquement

### Windows
```batch
generer_document.bat
```
→ Utilise `reconstruct_local.py` automatiquement

---

## 🆘 Problèmes ?

### Le texte n'apparaît pas
→ Utilise `reconstruct_with_layout.py`

### La mise en page est cassée
→ Utilise `reconstruct_local.py` pour une version plus simple

### Erreur "No module named 'bs4'"
```bash
pip3 install beautifulsoup4
```

---

## 📚 Documentation complète

- [Guide rapide](QUICKSTART.md)
- [README complet](README.md)
- [Liste des fichiers](FILES.md)

---

**Tu peux aussi générer les DEUX versions pour comparer ! 🎉**
