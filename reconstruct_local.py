#!/usr/bin/env python3
"""
Script de reconstruction LOCAL du document APSAD D20 - VERSION CORRIGÉE
Extraction améliorée du texte des textLayer
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

def extract_text_improved(html_content):
    """
    Extraction améliorée du texte des textLayer
    Combine tous les div enfants pour former des paragraphes
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    text_layers = soup.find_all('div', class_='textLayer')
    
    all_pages = []
    
    for layer in text_layers:
        # Extraire tous les div qui contiennent du texte
        divs = layer.find_all('div', recursive=False)
        
        if not divs:
            continue
            
        # Regrouper le texte par position verticale (top)
        lines = {}
        for div in divs:
            # Ignorer les div vides et ceux avec la classe endOfContent
            if 'endOfContent' in div.get('class', []):
                continue
                
            text = div.get_text(strip=True)
            if not text:
                continue
            
            # Extraire la position top du style
            style = div.get('style', '')
            top_match = re.search(r'top:([\d.]+)px', style)
            
            if top_match:
                top = float(top_match.group(1))
                # Arrondir à 5px près pour regrouper les éléments sur la même ligne
                top_rounded = round(top / 5) * 5
                
                if top_rounded not in lines:
                    lines[top_rounded] = []
                lines[top_rounded].append(text)
        
        if lines:
            # Trier les lignes par position verticale
            sorted_lines = sorted(lines.items())
            
            # Construire le texte de la page
            page_text = []
            for _, texts in sorted_lines:
                # Joindre les textes d'une même ligne
                line_text = ' '.join(texts)
                page_text.append(line_text)
            
            # Joindre toutes les lignes
            full_text = '\n'.join(page_text)
            
            if full_text.strip():
                all_pages.append(full_text)
    
    return all_pages

def create_chapter_title(filename):
    """Crée un titre de section à partir du nom de fichier"""
    basename = os.path.basename(filename)
    match = re.search(r'; ([^-]+) -', basename)
    if match:
        title = match.group(1).strip()
        return title
    return 'Section'

def generate_html(chapters_data):
    """Génère le HTML final"""
    
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
            max-width: 1000px;
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
        .page-separator {
            border-top: 2px dashed #ccc;
            margin: 40px 0;
            position: relative;
        }
        .page-separator::after {
            content: "• • •";
            position: absolute;
            top: -12px;
            left: 50%;
            transform: translateX(-50%);
            background: white;
            padding: 0 20px;
            color: #999;
        }
        .page-text {
            margin-bottom: 30px;
            color: #444;
            line-height: 1.8;
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
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
            text-decoration: underline;
        }
        .stats {
            background: #e8f4f8;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            font-size: 0.9em;
            color: #666;
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
    
    # Table des matières
    for filename in chapters_data.keys():
        title = create_chapter_title(filename)
        chapter_id = re.sub(r'[^a-z0-9]+', '-', title.lower())
        num_pages = len(chapters_data[filename])
        html += f'                <li><a href="#{chapter_id}">{title}</a> <span style="color:#999">({num_pages} pages)</span></li>\n'
    
    html += """            </ul>
        </div>
"""
    
    # Statistiques
    total_pages = sum(len(pages) for pages in chapters_data.values())
    html += f"""        <div class="stats">
            📊 <strong>Statistiques:</strong> {len(chapters_data)} sections • {total_pages} pages extraites
        </div>
"""
    
    # Contenu des chapitres
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
                html += '                <div class="page-separator"></div>\n'
            # Échapper les caractères HTML
            text_escaped = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            html += f'                <div class="page-text">{text_escaped}</div>\n'
        
        html += """            </div>
        </div>
"""
    
    html += """    </div>
</body>
</html>"""
    
    return html

def main():
    print("\n" + "="*70)
    print("🔧 RECONSTRUCTION DOCUMENT APSAD D20 - VERSION CORRIGÉE")
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
    print("📖 Extraction du contenu (méthode améliorée)...\n")
    chapters_data = OrderedDict()
    total_pages = 0
    
    for filepath in sorted_files:
        try:
            html_content = read_html_file(filepath)
            text_pages = extract_text_improved(html_content)
            
            if text_pages:
                chapters_data[filepath] = text_pages
                total_pages += len(text_pages)
                print(f"   ✓ {len(text_pages)} pages extraites")
            else:
                print(f"   ⚠️  Aucun contenu extrait")
                
        except Exception as e:
            print(f"   ✗ Erreur: {e}")
    
    if not chapters_data:
        print("\n❌ Aucun contenu n'a pu être extrait!\n")
        return
    
    # Génération
    print(f"\n📝 Génération du HTML final ({total_pages} pages totales)...")
    final_html = generate_html(chapters_data)
    
    # Sauvegarde
    output_file = "APSAD_D20_Document_Complet.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"\n✅ Document créé : {output_file}")
    print(f"   📊 Taille : {len(final_html):,} caractères")
    print(f"   📄 Sections : {len(chapters_data)}")
    print(f"   📑 Pages : {total_pages}")
    print(f"\n🌐 Ouvre le fichier dans ton navigateur pour le consulter!")
    print("\n" + "="*70)
    print("✨ Terminé avec succès !")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
