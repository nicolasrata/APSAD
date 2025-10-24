#!/usr/bin/env python3
"""
Script de reconstruction LOCAL - VERSION HYBRIDE
Préserve les positions mais force le texte visible
"""

import os
import glob
from bs4 import BeautifulSoup
import re
from collections import OrderedDict

def extract_chapter_number(filename):
    """Extrait le numéro de chapitre/annexe pour le tri"""
    basename = os.path.basename(filename)
    
    if "Pages liminaires" in basename:
        return (0, 0)
    if "Sommaire" in basename:
        return (0, 5)
    match = re.search(r'; (\d+)\. ', basename)
    if match:
        return (1, int(match.group(1)))
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

def extract_and_fix_text_layers(html_content):
    """
    Extrait les textLayer et force le texte visible
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    text_layers = soup.find_all('div', class_='textLayer')
    
    pages_html = []
    
    for layer in text_layers:
        # Parcourir tous les divs enfants
        for div in layer.find_all('div', recursive=False):
            # Ignorer les divs avec classe endOfContent
            if 'endOfContent' in div.get('class', []):
                continue
            
            # Modifier le style pour forcer le texte visible
            style = div.get('style', '')
            
            # Supprimer color: transparent
            style = re.sub(r'color:\s*transparent\s*;?', '', style)
            
            # Forcer la couleur noire
            if 'color:' not in style:
                style += '; color: #000;'
            else:
                style = re.sub(r'color:\s*[^;]+', 'color: #000', style)
            
            div['style'] = style
        
        # Récupérer le HTML modifié
        layer_html = str(layer)
        
        if layer_html and len(layer_html) > 100:
            pages_html.append(layer_html)
    
    return pages_html

def create_chapter_title(filename):
    """Crée un titre de section à partir du nom de fichier"""
    basename = os.path.basename(filename)
    match = re.search(r'; ([^-]+) -', basename)
    if match:
        title = match.group(1).strip()
        return title
    return 'Section'

def generate_html_hybrid(chapters_data):
    """Génère le HTML avec mise en page mais texte visible"""
    
    html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>APSAD D20 - Document complet</title>
    <style>
        /* Styles de base */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
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
            margin: 60px 0;
            page-break-before: always;
        }
        .chapter-title {
            background: linear-gradient(135deg, #003366 0%, #005599 100%);
            color: white;
            padding: 20px 30px;
            margin: 30px 0;
            font-size: 1.8em;
            font-weight: 600;
            border-left: 5px solid #FFD700;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        .page-container {
            position: relative;
            margin: 40px auto;
            background: white;
            border: 1px solid #ddd;
            padding: 40px 20px;
            min-height: 900px;
            max-width: 800px;
        }
        .page-number {
            position: absolute;
            top: 10px;
            right: 20px;
            color: #999;
            font-size: 0.9em;
            font-style: italic;
            background: #f9f9f9;
            padding: 5px 10px;
            border-radius: 3px;
        }
        
        /* Styles des textLayer - FORCER LE TEXTE VISIBLE */
        .textLayer {
            position: relative;
            left: 0;
            top: 0;
            right: 0;
            bottom: 0;
            overflow: visible !important;
            opacity: 1 !important;
            line-height: 1.2;
            min-height: 800px;
        }
        .textLayer > div {
            color: #000 !important;  /* FORCER NOIR */
            position: absolute;
            white-space: pre;
            cursor: text;
            transform-origin: 0% 0%;
            /* Supprimer toute transparence */
            opacity: 1 !important;
        }
        
        /* S'assurer que le texte est toujours visible */
        .textLayer * {
            color: #000 !important;
            opacity: 1 !important;
        }
        
        @media print {
            body {
                background: white;
                padding: 0;
            }
            .container {
                box-shadow: none;
            }
            .chapter {
                page-break-before: always;
            }
            .page-container {
                page-break-inside: avoid;
            }
        }
        
        .toc {
            background: #f9f9f9;
            padding: 30px;
            margin: 30px 0;
            border-left: 4px solid #003366;
        }
        .toc h2 {
            color: #003366;
            margin-bottom: 20px;
        }
        .toc ul {
            list-style: none;
            padding: 0;
        }
        .toc li {
            padding: 10px 0;
            border-bottom: 1px solid #e0e0e0;
        }
        .toc a {
            color: #005599;
            text-decoration: none;
            font-size: 1.1em;
            transition: color 0.3s;
        }
        .toc a:hover {
            color: #003366;
            text-decoration: underline;
        }
        .stats {
            background: #e8f4f8;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
            border-left: 4px solid #003366;
        }
        .stats strong {
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
                Document complet avec mise en page
            </p>
        </div>
        
        <div class="toc">
            <h2>📑 Table des matières</h2>
            <ul>
"""
    
    # Table des matières
    for filename in chapters_data.keys():
        title = create_chapter_title(filename)
        chapter_id = re.sub(r'[^a-z0-9]+', '-', title.lower())
        num_pages = len(chapters_data[filename])
        html += f'                <li><a href="#{chapter_id}">{title}</a> <span style="color:#999; font-size:0.9em;">({num_pages} pages)</span></li>\n'
    
    html += """            </ul>
        </div>
"""
    
    # Statistiques
    total_pages = sum(len(pages) for pages in chapters_data.values())
    html += f"""        <div class="stats">
            <strong>📊 Statistiques :</strong> {len(chapters_data)} sections • {total_pages} pages
        </div>
"""
    
    # Contenu des chapitres
    for filename, pages_html in chapters_data.items():
        title = create_chapter_title(filename)
        chapter_id = re.sub(r'[^a-z0-9]+', '-', title.lower())
        
        html += f"""
        <div class="chapter" id="{chapter_id}">
            <div class="chapter-title">{title}</div>
"""
        
        for i, page_html in enumerate(pages_html, 1):
            html += f"""
            <div class="page-container">
                <div class="page-number">Page {i}/{len(pages_html)}</div>
                {page_html}
            </div>
"""
        
        html += """        </div>
"""
    
    html += """    </div>
</body>
</html>"""
    
    return html

def main():
    print("\n" + "="*70)
    print("🔧 RECONSTRUCTION DOCUMENT APSAD D20 - VERSION FINALE")
    print("="*70 + "\n")
    
    # Chercher les fichiers HTML
    print("📂 Recherche des fichiers HTML...")
    html_files = glob.glob("*.html")
    html_files = [f for f in html_files if not f.startswith('APSAD_D20_')]
    
    if not html_files:
        print("\n❌ Aucun fichier HTML trouvé!")
        print("\n💡 Assure-toi que les fichiers HTML sont dans le même dossier.\n")
        return
    
    print(f"   ✓ {len(html_files)} fichiers trouvés\n")
    
    # Trier
    print("📊 Tri des fichiers...")
    sorted_files = sorted(html_files, key=extract_chapter_number)
    print("   ✓ Ordre établi\n")
    
    # Extraction
    print("📖 Extraction avec texte visible forcé...\n")
    chapters_data = OrderedDict()
    total_pages = 0
    
    for filepath in sorted_files:
        try:
            html_content = read_html_file(filepath)
            pages_html = extract_and_fix_text_layers(html_content)
            
            if pages_html:
                chapters_data[filepath] = pages_html
                total_pages += len(pages_html)
                print(f"   ✓ {len(pages_html)} pages extraites")
            else:
                print(f"   ⚠️  Aucun contenu extrait")
                
        except Exception as e:
            print(f"   ✗ Erreur: {e}")
    
    if not chapters_data:
        print("\n❌ Aucun contenu n'a pu être extrait!\n")
        return
    
    # Génération
    print(f"\n📝 Génération du HTML final ({total_pages} pages)...")
    final_html = generate_html_hybrid(chapters_data)
    
    # Sauvegarde
    output_file = "APSAD_D20_Document_Final.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"\n✅ Document créé : {output_file}")
    print(f"   📊 Taille : {len(final_html):,} caractères")
    print(f"   📄 Sections : {len(chapters_data)}")
    print(f"   📑 Pages : {total_pages}")
    print(f"   🎨 Mise en page préservée + texte visible")
    print(f"\n🌐 Ouvre le fichier :")
    print(f"   open {output_file}")
    print("\n" + "="*70)
    print("✨ Terminé avec succès !")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
