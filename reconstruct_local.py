#!/usr/bin/env python3
"""
Script de reconstruction LOCAL du document APSAD D20
Fonctionne avec les fichiers HTML déjà téléchargés localement
"""

import os
import glob
from bs4 import BeautifulSoup
import re
from collections import OrderedDict

def extract_chapter_number(filename):
    """Extrait le numéro de chapitre/annexe pour le tri"""
    basename = os.path.basename(filename)
    
    # Pages liminaires = 0
    if "Pages liminaires" in basename:
        return (0, 0)
    # Sommaire = 0.5
    if "Sommaire" in basename:
        return (0, 5)
    # Chapitres 1-8
    match = re.search(r'; (\d+)\. ', basename)
    if match:
        return (1, int(match.group(1)))
    # Annexes
    match = re.search(r'Annexe (\d+)', basename)
    if match:
        annexe_num = match.group(1)
        if '-' in annexe_num:
            parts = annexe_num.split('-')
            return (2, int(parts[0]), int(parts[1]))
        return (2, int(annexe_num), 0)
    return (999, 0)

def read_html_file(filepath):
    """Lit un fichier HTML local"""
    print(f"📖 Lecture: {os.path.basename(filepath)[:60]}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def extract_text_only(html_content):
    """Extrait uniquement le texte, sans les styles de position"""
    soup = BeautifulSoup(html_content, 'html.parser')
    text_layers = soup.find_all('div', class_='textLayer')
    
    all_text = []
    for layer in text_layers:
        # Extraire le texte de tous les spans
        text_parts = []
        for span in layer.find_all('span'):
            text = span.get_text(strip=True)
            if text:
                text_parts.append(text)
        if text_parts:
            all_text.append(' '.join(text_parts))
    
    return all_text

def create_chapter_title(filename):
    """Crée un titre de section à partir du nom de fichier"""
    basename = os.path.basename(filename)
    match = re.search(r'; ([^-]+) -', basename)
    if match:
        title = match.group(1).strip()
        return title
    return 'Section'

def generate_simple_html(chapters_data):
    """Génère un HTML épuré et lisible"""
    
    html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>APSAD D20 - Document complet</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f4f4f4;
            padding: 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            border-bottom: 3px solid #003366;
            padding-bottom: 30px;
            margin-bottom: 40px;
        }
        .header h1 {
            color: #003366;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .header p {
            color: #666;
            font-size: 1.1em;
        }
        .chapter {
            margin: 50px 0;
            page-break-before: always;
        }
        .chapter-title {
            background: linear-gradient(135deg, #003366 0%, #005599 100%);
            color: white;
            padding: 20px 30px;
            margin: 30px -40px 30px -40px;
            font-size: 1.8em;
            font-weight: 600;
            border-left: 5px solid #FFD700;
        }
        .chapter-content {
            padding: 20px 0;
        }
        .page-break {
            border-top: 1px dashed #ccc;
            margin: 30px 0;
            padding-top: 20px;
        }
        .page-text {
            text-align: justify;
            margin-bottom: 20px;
            color: #444;
        }
        @media print {
            body {
                background: white;
                padding: 0;
            }
            .container {
                box-shadow: none;
                padding: 20px;
            }
            .chapter {
                page-break-before: always;
            }
        }
        .toc {
            background: #f9f9f9;
            padding: 30px;
            margin: 30px -40px;
            border-left: 4px solid #003366;
        }
        .toc h2 {
            color: #003366;
            margin-bottom: 20px;
        }
        .toc ul {
            list-style: none;
        }
        .toc li {
            padding: 8px 0;
            border-bottom: 1px solid #e0e0e0;
        }
        .toc a {
            color: #005599;
            text-decoration: none;
            transition: color 0.3s;
        }
        .toc a:hover {
            color: #003366;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Référentiel APSAD D20</h1>
            <p>Installations photovoltaïques</p>
            <p style="font-size: 0.9em; color: #999; margin-top: 10px;">
                Document complet reconstruit
            </p>
        </div>
        
        <div class="toc">
            <h2>📑 Table des matières</h2>
            <ul>
"""
    
    # Générer la table des matières
    for filename in chapters_data.keys():
        title = create_chapter_title(filename)
        chapter_id = re.sub(r'[^a-z0-9]+', '-', title.lower())
        html += f'                <li><a href="#{chapter_id}">{title}</a></li>\n'
    
    html += """            </ul>
        </div>
"""
    
    # Ajouter le contenu de chaque chapitre
    for filename, text_pages in chapters_data.items():
        title = create_chapter_title(filename)
        chapter_id = re.sub(r'[^a-z0-9]+', '-', title.lower())
        
        html += f"""
        <div class="chapter" id="{chapter_id}">
            <div class="chapter-title">{title}</div>
            <div class="chapter-content">
"""
        
        for i, text in enumerate(text_pages):
            if i > 0:
                html += '                <div class="page-break"></div>\n'
            html += f'                <div class="page-text">{text}</div>\n'
        
        html += """            </div>
        </div>
"""
    
    html += """    </div>
</body>
</html>"""
    
    return html

def main():
    print("\n" + "="*70)
    print("🔧 RECONSTRUCTION DOCUMENT APSAD D20 (Version locale)")
    print("="*70 + "\n")
    
    # 1. Chercher les fichiers HTML localement
    print("📂 Recherche des fichiers HTML dans le dossier courant...")
    html_files = glob.glob("*.html")
    
    # Exclure les fichiers générés
    html_files = [f for f in html_files if not f.startswith('APSAD_D20_')]
    
    if not html_files:
        print("\n❌ Aucun fichier HTML trouvé!")
        print("\n💡 Astuce: Assure-toi que les fichiers HTML sont dans le même")
        print("   dossier que ce script Python.\n")
        print("📥 Pour télécharger les fichiers:")
        print("   1. Va sur https://github.com/nicolasrata/APSAD")
        print("   2. Clique sur 'Code' > 'Download ZIP'")
        print("   3. Décompresse et lance ce script\n")
        return
    
    print(f"   ✓ {len(html_files)} fichiers trouvés\n")
    
    # 2. Trier les fichiers
    print("📊 Tri des fichiers par ordre logique...")
    sorted_files = sorted(html_files, key=extract_chapter_number)
    print("   ✓ Ordre établi\n")
    
    # 3. Extraction
    print("📖 Extraction du contenu...\n")
    chapters_data = OrderedDict()
    
    for filepath in sorted_files:
        try:
            html_content = read_html_file(filepath)
            text_pages = extract_text_only(html_content)
            
            if text_pages:  # Seulement si du contenu a été extrait
                chapters_data[filepath] = text_pages
                print(f"   ✓ {len(text_pages)} pages extraites")
            else:
                print(f"   ⚠️  Aucun contenu extrait (probablement pas un chapitre)")
                
        except Exception as e:
            print(f"   ✗ Erreur: {e}")
    
    if not chapters_data:
        print("\n❌ Aucun contenu n'a pu être extrait!")
        print("   Vérifie que les fichiers HTML contiennent des <div class='textLayer'>\n")
        return
    
    # 4. Génération
    print("\n📝 Génération du HTML final...")
    final_html = generate_simple_html(chapters_data)
    
    # 5. Sauvegarde
    output_file = "APSAD_D20_Document_Complet.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"\n✅ Document créé : {output_file}")
    print(f"   📊 Taille : {len(final_html):,} caractères")
    print(f"   📄 Chapitres : {len(chapters_data)}")
    print(f"\n🌐 Ouvre le fichier dans ton navigateur pour le consulter!")
    print("\n" + "="*70)
    print("✨ Terminé avec succès !")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
