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
pip install -r requirements.txt
```

ou

```bash
pip install requests beautifulsoup4
```

### 🎯 Deux versions disponibles

#### Option 1 : Version complète (avec mise en page)

```bash
python reconstruct_document.py
```

**Résultat** : `APSAD_D20_Document_Complet.html`
- ✅ Préserve la mise en page originale (positions, styles CSS)
- ✅ Fidèle au PDF d'origine
- ⚠️ Fichier plus volumineux
- 👁️ Idéal pour impression ou consultation identique à l'original

#### Option 2 : Version simplifiée (texte seul) - **RECOMMANDÉE** 

```bash
python reconstruct_simple.py
```

**Résultat** : `APSAD_D20_Document_Simplifie.html`
- ✅ Mise en page moderne et épurée
- ✅ Table des matières interactive
- ✅ Plus léger et rapide à charger
- ✅ Meilleure lisibilité à l'écran
- 📱 Responsive (adapté mobile/tablette)
- 🔍 Texte facilement sélectionnable et recherchable

## 🎯 Fonctionnement des scripts

### Script complet (`reconstruct_document.py`)

1. **Récupération** : Télécharge tous les fichiers HTML depuis GitHub
2. **Extraction** : Extrait les `<div class="textLayer">` avec leurs styles
3. **Tri** : Ordonne les chapitres (Pages liminaires → Chapitres → Annexes)
4. **Fusion** : Assemble tout dans un HTML avec styles inline
5. **Génération** : Crée un document fidèle à la mise en page originale

### Script simplifié (`reconstruct_simple.py`)

1. **Récupération** : Télécharge tous les fichiers HTML depuis GitHub
2. **Extraction** : Extrait uniquement le texte des `textLayer`
3. **Nettoyage** : Supprime les styles de positionnement
4. **Organisation** : Structure en chapitres avec table des matières
5. **Génération** : Crée un document moderne et lisible

## 📊 Comparaison des versions

| Caractéristique | Version complète | Version simplifiée |
|----------------|------------------|-------------------|
| Taille fichier | 🔴 Volumineux (~5-10 MB) | 🟢 Léger (~1-2 MB) |
| Fidélité originale | 🟢 Identique au PDF | 🟡 Structure préservée |
| Lisibilité | 🟡 Comme le PDF | 🟢 Optimisée |
| Recherche texte | 🟡 Moyenne | 🟢 Excellente |
| Impression | 🟢 Parfaite | 🟢 Bonne |
| Mobile | 🟡 Moyen | 🟢 Excellent |
| Table des matières | ❌ Non | 🟢 Interactive |
| **Recommandation** | Archive/impression | **Consultation** ⭐ |

## 📝 Recommandations d'utilisation

**Utilise la version complète si :**
- Tu veux une reproduction exacte du PDF
- Tu as besoin de l'aspect visuel original
- Tu vas imprimer le document

**Utilise la version simplifiée si :**
- Tu veux consulter le document à l'écran
- Tu as besoin de rechercher du texte rapidement
- Tu veux un chargement rapide
- Tu consultes sur mobile/tablette

## 🔍 Personnalisation

Les scripts sont modulables. Tu peux modifier :

**Dans `reconstruct_document.py` :**
- Les styles CSS dans `generate_complete_html()`
- Les couleurs de chapitres
- La mise en page des pages

**Dans `reconstruct_simple.py` :**
- Les styles CSS (couleurs, typographie)
- La structure de la table des matières
- Les séparateurs de pages

## 🛠️ Exemples d'usage avancé

### Extraire seulement certains chapitres

```python
# Dans main(), filtre les fichiers
sorted_files = [f for f in sorted_files if 'Chapitre 2' in f['name']]
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
# Utilise wkhtmltopdf ou similar
wkhtmltopdf APSAD_D20_Document_Simplifie.html APSAD_D20.pdf
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
1. Vérifie que tu as installé les dépendances (`pip install -r requirements.txt`)
2. Vérifie ta connexion internet (les scripts téléchargent depuis GitHub)
3. Consulte les messages d'erreur détaillés dans la console
4. Ouvre une issue sur GitHub si le problème persiste

## 📜 License

Les scripts Python sont fournis "tels quels" sous licence MIT. Le contenu du référentiel APSAD D20 reste propriété du CNPP.

---

<div align="center">

**Scripts de reconstruction créés pour faciliter la consultation du référentiel APSAD D20**

[📖 Guide rapide](QUICKSTART.md) • [🐛 Signaler un bug](https://github.com/nicolasrata/APSAD/issues) • [💡 Demander une fonctionnalité](https://github.com/nicolasrata/APSAD/issues)

</div>
