#!/usr/bin/env python3
"""
Script de reconstruction LOCAL - VERSION AVEC MISE EN PAGE
Préserve la mise en forme originale avec positions CSS
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

def extract_text_layers_with_style(html_content):
    """
    Extrait les textLayer en conservant les styles et positions
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    text_layers = soup.find_all('div', class_='textLayer')
    
    pages_html = []
    
    for layer in text_layers:
        # Récupérer le HTML complet du textLayer
        layer_html = str(layer)
        
        # Nettoyer un peu (enlever les divs vides)
        if layer_html and len(layer_html) > 100:  # Au moins 100 caractères
            pages_html.append(layer_html)
    
    return pages_html

def extract_css_from_html(html_content):
    """Extrait les styles CSS du document"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    css_styles = []
    
    # Récupérer toutes les balises <style>
    for style_tag in soup.find_all('style'):
        if style_tag.string:
            css_styles.append(style_tag.string)
    
    return '\n'.join(css_styles)

def create_chapter_title(filename):
    """Crée un titre de section à partir du nom de fichier"""
    basename = os.path.basename(filename)
    match = re.search(r'; ([^-]+) -', basename)
    if match:
        title = match.group(1).strip()
        return title
    return 'Section'

def generate_html_with_layout(chapters_data, all_css):
    """Génère le HTML final avec mise en page préservée"""
    
    html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>APSAD D20 - Document complet avec mise en page</title>
    <style>
        /* Styles de base */
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f0f0f0;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 30px;
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
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            padding: 20px;
            min-height: 800px;
        }
        .page-number {
            position: absolute;
            top: 10px;
            right: 20px;
            color: #999;
            font-size: 0.9em;
            font-style: italic;
        }
        
        /* Styles des textLayer */
        .textLayer {
            position: relative;
            left: 0;
            top: 0;
            right: 0;
            bottom: 0;
            overflow: hidden;
            opacity: 1;
            line-height: 1.0;
        }
        .textLayer > div {
            color: #000;
            position: absolute;
            white-space: pre;
            cursor: text;
            transform-origin: 0% 0%;
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
"""
    
    # Ajouter les styles CSS extraits
    if all_css:
        html += "\n        /* Styles extraits des documents originaux */\n"
        html += all_css
    
    html += """
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Référentiel APSAD D20</h1>
            <p>Installations photovoltaïques</p>
            <p style="font-size: 0.9em; color: #999; margin-top: 10px;">
                Document complet reconstruit avec mise en page originale
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
            <strong>📊 Statistiques du document :</strong><br>
            • {len(chapters_data)} sections<br>
            • {total_pages} pages extraites<br>
            • Mise en page originale préservée
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
    print("🔧 RECONSTRUCTION DOCUMENT APSAD D20 - AVEC MISE EN PAGE")
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
    print("📖 Extraction du contenu avec mise en page...\n")
    chapters_data = OrderedDict()
    all_css = set()
    total_pages = 0
    
    for filepath in sorted_files:
        try:
            html_content = read_html_file(filepath)
            
            # Extraire les pages avec leur HTML
            pages_html = extract_text_layers_with_style(html_content)
            
            # Extraire les CSS
            css = extract_css_from_html(html_content)
            if css:
                all_css.add(css)
            
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
    
    # Fusionner tous les CSS
    combined_css = '\n'.join(all_css)
    
    # Génération
    print(f"\n📝 Génération du HTML final ({total_pages} pages)...")
    final_html = generate_html_with_layout(chapters_data, combined_css)
    
    # Sauvegarde
    output_file = "APSAD_D20_Document_Avec_Mise_En_Page.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"\n✅ Document créé : {output_file}")
    print(f"   📊 Taille : {len(final_html):,} caractères")
    print(f"   📄 Sections : {len(chapters_data)}")
    print(f"   📑 Pages : {total_pages}")
    print(f"   🎨 Mise en page préservée")
    print(f"\n🌐 Ouvre le fichier dans ton navigateur :")
    print(f"   open {output_file}")
    print("\n" + "="*70)
    print("✨ Terminé avec succès !")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
