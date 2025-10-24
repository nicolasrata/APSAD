# 📄 Export PDF - Guide d'installation

Le script `reconstruct_final.py` peut maintenant générer automatiquement un fichier PDF avec **texte sélectionnable** !

## 🚀 Installation rapide

### Sur macOS 🍎

```bash
# 1. Installer les dépendances système (Homebrew)
brew install python3 pango cairo gdk-pixbuf libffi

# 2. Installer WeasyPrint
pip3 install weasyprint

# 3. Vérifier l'installation
python3 -c "import weasyprint; print('✅ WeasyPrint installé!')"
```

### Sur Linux (Ubuntu/Debian) 🐧

```bash
# 1. Installer les dépendances système
sudo apt-get install python3-pip python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0

# 2. Installer WeasyPrint
pip3 install weasyprint

# 3. Vérifier l'installation
python3 -c "import weasyprint; print('✅ WeasyPrint installé!')"
```

### Sur Windows 🪟

```bash
# 1. Télécharger GTK3 Runtime
# Va sur : https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
# Télécharge et installe gtk3-runtime-x.x.x-x-x-x-ts-win64.exe

# 2. Installer WeasyPrint
pip install weasyprint

# 3. Vérifier l'installation
python -c "import weasyprint; print('✅ WeasyPrint installé!')"
```

---

## 📝 Utilisation

Une fois WeasyPrint installé :

```bash
python3 reconstruct_final.py
```

Le script va générer **automatiquement** :
1. ✅ `APSAD_D20_Document_Final.html` - Version HTML
2. ✅ `APSAD_D20_Document_Final.pdf` - Version PDF avec texte sélectionnable

---

## ⚠️ Si WeasyPrint n'est pas installé

Pas de problème ! Le script fonctionne quand même :
- ✅ Le fichier HTML sera créé normalement
- ⚠️ Un message t'informera que WeasyPrint n'est pas installé
- 💡 Tu peux installer WeasyPrint plus tard et relancer le script

**Message affiché :**
```
⚠️  WeasyPrint n'est pas installé.
   Pour générer le PDF, installe WeasyPrint :
   pip3 install weasyprint

   Le fichier HTML a quand même été créé.
```

---

## 🎯 Avantages du PDF généré

### ✅ Texte sélectionnable
Le texte transparent du HTML est préservé dans le PDF :
- Tu peux **sélectionner** le texte
- Tu peux **copier-coller**
- Tu peux **rechercher** avec Cmd+F

### ✅ Structure identique
- Images de fond préservées
- Mise en page originale
- Navigation par chapitres

### ✅ Qualité professionnelle
- Résolution optimale des images
- Polices embarquées
- Table des matières avec liens

---

## 🐛 Problèmes fréquents

### "cairo >= 1.15.4 is required"
**Sur macOS :**
```bash
brew install cairo pango
pip3 install --upgrade weasyprint
```

**Sur Linux :**
```bash
sudo apt-get install libcairo2-dev libpango1.0-dev
pip3 install --upgrade weasyprint
```

### "ModuleNotFoundError: No module named 'cffi'"
```bash
pip3 install cffi
pip3 install weasyprint
```

### Erreur de compilation sur macOS M1/M2
```bash
# Installer les outils de développement
xcode-select --install

# Puis réessayer
pip3 install weasyprint
```

### Le PDF est trop lourd
C'est normal ! Le PDF contient toutes les images en haute qualité.
- HTML : ~2-5 MB
- PDF : ~50-150 MB (selon le nombre de pages)

---

## 💡 Alternative sans WeasyPrint

Si tu ne peux pas installer WeasyPrint, tu peux convertir le HTML en PDF avec ton navigateur :

1. Ouvre `APSAD_D20_Document_Final.html` dans Chrome/Safari/Firefox
2. Appuie sur **Cmd+P** (ou Ctrl+P sur Windows)
3. Choisis **"Enregistrer au format PDF"**
4. Configure :
   - Marges : Minimales
   - Échelle : 100%
   - En-têtes/pieds de page : Désactivés
5. Clique sur **Enregistrer**

⚠️ **Attention :** Le texte transparent pourrait ne pas être sélectionnable avec cette méthode.

---

## 📊 Comparaison des méthodes

| Méthode | Texte sélectionnable | Qualité | Taille fichier |
|---------|---------------------|---------|----------------|
| WeasyPrint | ✅ Oui | 🟢 Excellente | 🟡 Moyenne (~100 MB) |
| Navigateur (Cmd+P) | ⚠️ Variable | 🟢 Bonne | 🟢 Légère (~20 MB) |
| HTML uniquement | ✅ Oui | 🟢 Excellente | 🟢 Très légère (~5 MB) |

---

## 🆘 Besoin d'aide ?

Si tu rencontres des problèmes :
1. Vérifie que Python 3.7+ est installé : `python3 --version`
2. Essaie de réinstaller : `pip3 install --upgrade weasyprint`
3. Consulte la doc officielle : https://doc.courtbouillon.org/weasyprint/
4. Ouvre une issue sur GitHub

---

**Bonne génération de PDF ! 📄✨**
