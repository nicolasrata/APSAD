# Référentiel APSAD D20 - Reconstruction de document

Ce dépôt contient les fichiers HTML individuels du **Référentiel APSAD D20 sur les installations photovoltaïques**, ainsi qu'un script pour reconstruire le document complet.

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
pip install requests beautifulsoup4
```

### Utilisation

```bash
python reconstruct_document.py
```

### Résultat

Le script génère un fichier **`APSAD_D20_Document_Complet.html`** qui contient :
- ✅ Tous les chapitres dans l'ordre
- ✅ Toutes les annexes
- ✅ Styles CSS préservés
- ✅ Mise en page identique à l'original
- ✅ Navigation par chapitres

## 🎯 Fonctionnement du script

1. **Récupération** : Télécharge tous les fichiers HTML depuis GitHub
2. **Extraction** : Extrait les `<div class="textLayer">` contenant le texte
3. **Tri** : Ordonne les chapitres (Pages liminaires → Chapitres → Annexes)
4. **Fusion** : Assemble tout dans un HTML unique
5. **Styles** : Préserve la mise en page avec les CSS d'origine

## 📄 Format du document reconstruit

Le document final inclut :
- Une en-tête centrée avec le titre
- Des séparateurs visuels entre chapitres
- Chaque page du PDF original comme section
- Styles CSS inline pour une mise en page fidèle

## 🔍 Personnalisation

Vous pouvez modifier le script pour :
- Changer les styles CSS (variables dans `generate_complete_html()`)
- Filtrer certains chapitres
- Extraire seulement le texte brut
- Générer d'autres formats (Markdown, PDF...)

## ⚠️ Note légale

Ce référentiel appartient au CNPP. L'utilisation de ces fichiers doit respecter les droits d'auteur et conditions d'utilisation du CNPP/APSAD.

## 🤝 Contribution

Pour toute amélioration du script de reconstruction, n'hésite pas à :
1. Fork le dépôt
2. Créer une branche
3. Proposer une pull request

---

*Document technique généré pour faciliter la consultation du référentiel APSAD D20*
