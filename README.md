# Référentiel APSAD D20 - Reconstruction de document

Ce dépôt contient les fichiers HTML individuels du **Référentiel APSAD D20 sur les installations photovoltaïques**, ainsi que des scripts pour reconstruire le document complet.

> 🚀 **Nouveau ?** Commence avec le [Guide de démarrage rapide](QUICKSTART.md) !

## 📁 Structure du dépôt

- **Pages liminaires** : Page de garde, mentions légales
- **Sommaire** : Table des matières
- **Chapitres 1-8** : Corps principal du document
  - Chapitre 1 : Généralités
  - Chapitre 2 : Dispositions constructives
  - Chapitre 3 : Dispositions électriques
  - Chapitre 4 : Exploitation et intervention
  - Chapitre 5 : Entretien et maintenance
  - Chapitre 6 : Contrôle des installations
  - Chapitre 7 : Documents à fournir
  - Chapitre 8 : Obligations des entreprises
- **Annexes 1-12** : Documents complémentaires et modèles

## 🔧 Reconstruction du document complet

### Prérequis

```bash
pip install beautifulsoup4
```

(ou `pip install -r requirements.txt` pour installer toutes les dépendances)

### 🎯 Trois versions disponibles

#### ⭐ Option 1 : Version locale (RECOMMANDÉE)

```bash
python reconstruct_local.py
```

**Avantages :**
- ✅ Fonctionne sans connexion internet (après téléchargement)
- ✅ Pas besoin de l'API GitHub
- ✅ Plus rapide
- ✅ Lit directement les fichiers HTML locaux

**Résultat** : `APSAD_D20_Document_Complet.html`

#### Option 2 : Version simplifiée (avec API GitHub)

```bash
python reconstruct_simple.py
```

**Résultat** : `APSAD_D20_Document_Simplifie.html`
- ✅ Télécharge depuis GitHub automatiquement
- ✅ Mise en page moderne et épurée
- ✅ Table des matières interactive
- ⚠️ Nécessite connexion internet et repo public

#### Option 3 : Version complète (avec API GitHub)

```bash
python reconstruct_document.py
```

**Résultat** : `APSAD_D20_Document_Complet.html`
- ✅ Préserve la mise en page originale
- ✅ Télécharge depuis GitHub automatiquement
- ⚠️ Nécessite connexion internet et repo public
- ⚠️ Fichier plus volumineux

### 🔑 Configuration pour l'API GitHub (si nécessaire)

Si tu obtiens une erreur 404 avec les scripts qui utilisent l'API GitHub, tu as deux options :

**Option A - Utilise le script local (recommandé) :**
```bash
python reconstruct_local.py
```

**Option B - Configure un token GitHub :**
```bash
# 1. Crée un token sur https://github.com/settings/tokens
# 2. Configure-le dans ton environnement
export GITHUB_TOKEN="ton_token_ici"  # Linux/Mac
set GITHUB_TOKEN=ton_token_ici       # Windows CMD
$env:GITHUB_TOKEN="ton_token_ici"    # Windows PowerShell
```

## 🎯 Fonctionnement des scripts

### Script local (`reconstruct_local.py`) - ⭐ RECOMMANDÉ

1. **Recherche** : Cherche les fichiers HTML dans le dossier courant
2. **Extraction** : Extrait le texte des `textLayer`
3. **Tri** : Ordonne les chapitres automatiquement
4. **Génération** : Crée un document HTML moderne

### Script simplifié (`reconstruct_simple.py`)

1. **Téléchargement** : Utilise l'API GitHub pour récupérer les fichiers
2. **Extraction** : Extrait uniquement le texte
3. **Organisation** : Structure avec table des matières
4. **Génération** : Document moderne et lisible

### Script complet (`reconstruct_document.py`)

1. **Téléchargement** : Utilise l'API GitHub
2. **Extraction** : Préserve tous les styles CSS
3. **Fusion** : Assemble avec mise en page originale
4. **Génération** : Document fidèle au PDF

## 📊 Comparaison des versions

| Caractéristique | Script local | Version simplifiée | Version complète |
|----------------|--------------|-------------------|------------------|
| Connexion internet | ❌ Non | ✅ Oui | ✅ Oui |
| API GitHub | ❌ Non | ✅ Oui | ✅ Oui |
| Vitesse | 🟢 Rapide | 🟡 Moyenne | 🔴 Lente |
| Taille fichier | 🟢 Léger | 🟢 Léger | 🔴 Lourd |
| Table des matières | ✅ Oui | ✅ Oui | ❌ Non |
| Fidélité originale | 🟡 Bonne | 🟡 Bonne | 🟢 Parfaite |
| **Recommandation** | ⭐ **Par défaut** | Usage avancé | Impression |

## 📝 Recommandations d'utilisation

**Utilise `reconstruct_local.py` si :**
- Tu as téléchargé le repo en ZIP (la plupart des cas)
- Tu veux la solution la plus simple et rapide
- Tu n'as pas besoin de connexion internet

**Utilise `reconstruct_simple.py` si :**
- Tu veux télécharger automatiquement depuis GitHub
- Le repo est public
- Tu as une connexion internet stable

**Utilise `reconstruct_document.py` si :**
- Tu veux une reproduction exacte du PDF
- Tu vas imprimer le document
- La fidélité visuelle est importante

## 🔍 Personnalisation

Les scripts sont modulables. Tu peux modifier :

**Dans `reconstruct_local.py` :**
- Les styles CSS (ligne ~70)
- Les couleurs de chapitres
- La structure de la table des matières

**Dans les autres scripts :**
- Filtrer certains chapitres
- Changer la mise en page
- Exporter en d'autres formats

## 🛠️ Exemples d'usage avancé

### Extraire seulement certains chapitres

```python
# Dans reconstruct_local.py, après la ligne "html_files = glob.glob("*.html")"
html_files = [f for f in html_files if 'Chapitre 2' in f or 'Chapitre 3' in f]
```

### Générer un fichier Markdown

```python
def extract_to_markdown(chapters_data):
    md = "# APSAD D20\n\n"
    for filename, pages in chapters_data.items():
        title = create_chapter_title(filename)
        md += f"## {title}\n\n"
        for page in pages:
            md += f"{page}\n\n"
    return md
```

### Exporter en PDF

```bash
# Utilise wkhtmltopdf
wkhtmltopdf APSAD_D20_Document_Complet.html APSAD_D20.pdf

# Ou avec weasyprint
weasyprint APSAD_D20_Document_Complet.html APSAD_D20.pdf
```

## ⚠️ Note légale

Ce référentiel appartient au **CNPP (Centre National de Prévention et de Protection)**. L'utilisation de ces fichiers doit respecter les droits d'auteur et conditions d'utilisation du CNPP/APSAD.

Ces scripts sont fournis pour faciliter la consultation personnelle du document. Toute utilisation commerciale ou redistribution doit être autorisée par le CNPP.

## 🤝 Contribution

Pour améliorer les scripts :
1. Fork le dépôt
2. Crée une branche (`git checkout -b feature/amelioration`)
3. Commit tes changements (`git commit -m 'Amélioration XYZ'`)
4. Push (`git push origin feature/amelioration`)
5. Ouvre une Pull Request

## 📞 Support

Si tu rencontres des problèmes :

### Erreur "No module named 'bs4'"
```bash
pip install beautifulsoup4
```

### Erreur 404 avec l'API GitHub
Utilise `reconstruct_local.py` à la place.

### "Aucun fichier HTML trouvé"
Assure-toi d'être dans le dossier contenant les fichiers HTML.

### Autres problèmes
1. Vérifie ta version de Python (3.7+)
2. Consulte les messages d'erreur détaillés
3. Ouvre une [issue sur GitHub](https://github.com/nicolasrata/APSAD/issues)

## 📜 License

Les scripts Python sont fournis "tels quels" sous licence MIT. Le contenu du référentiel APSAD D20 reste propriété du CNPP.

---

<div align="center">

**Scripts de reconstruction créés pour faciliter la consultation du référentiel APSAD D20**

[📖 Guide rapide](QUICKSTART.md) • [🐛 Signaler un bug](https://github.com/nicolasrata/APSAD/issues) • [💡 Demander une fonctionnalité](https://github.com/nicolasrata/APSAD/issues)

</div>
