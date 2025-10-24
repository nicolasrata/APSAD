#!/usr/bin/env python3
"""
Version simplifiée du script de reconstruction
Génère un document HTML épuré et plus léger
"""

import requests
from bs4 import BeautifulSoup
import re
from collections import OrderedDict

GITHUB_API = "https://api.github.com/repos/nicolasrata/APSAD/contents"
GITHUB_RAW = "https://raw.githubusercontent.com/nicolasrata/APSAD/main/"

def get_files_list():
    response = requests.get(GITHUB_API)
    response.raise_for_status()
    return response.json()

def extract_chapter_number(filename):
    if "Pages liminaires" in filename:
        return (0, 0)
    if "Sommaire" in filename:
        return (0, 5)
    match = re.search(r'; (\d+)\. ', filename)
    if match:
        return (1, int(match.group(1)))
    match = re.search(r'Annexe (\d+)', filename)
    if match:
        annexe_num = match.group(1)
        if '-' in annexe_num:
            parts = annexe_num.split('-')
            return (2, int(parts[0]), int(parts[1]))
        return (2, int(annexe_num), 0)
    return (999, 0)

def download_html(filename):
    url = GITHUB_RAW + requests.utils.quote(filename)
    print(f"📥 {filename[:60]}...")
    response = requests.get(url)
    response.raise_for_status()
    return response.text

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
    match = re.search(r'; ([^-]+) -', filename)
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
    <title>APSAD D20 - Document complet (version texte)</title>
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
                Document complet reconstruit - Version texte
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
    print("\n" + "="*60)
    print("🔧 RECONSTRUCTION DOCUMENT APSAD D20 (Version simplifiée)")
    print("="*60 + "\n")
    
    # 1. Récupérer les fichiers
    print("📂 Récupération de la liste des fichiers...")
    files = get_files_list()
    html_files = [f for f in files if f['name'].endswith('.html')]
    print(f"   ✓ {len(html_files)} fichiers trouvés\n")
    
    # 2. Trier
    print("📊 Tri des fichiers...")
    sorted_files = sorted(html_files, key=lambda x: extract_chapter_number(x['name']))
    print("   ✓ Ordre établi\n")
    
    # 3. Extraction
    print("📖 Extraction du contenu...\n")
    chapters_data = OrderedDict()
    
    for file_info in sorted_files:
        filename = file_info['name']
        try:
            html_content = download_html(filename)
            text_pages = extract_text_only(html_content)
            chapters_data[filename] = text_pages
            print(f"   ✓ {len(text_pages)} pages extraites")
        except Exception as e:
            print(f"   ✗ Erreur: {e}")
    
    # 4. Génération
    print("\n📝 Génération du HTML final...")
    final_html = generate_simple_html(chapters_data)
    
    # 5. Sauvegarde
    output_file = "APSAD_D20_Document_Simplifie.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"\n✅ Document créé : {output_file}")
    print(f"   📊 Taille : {len(final_html):,} caractères")
    print(f"   📄 Chapitres : {len(chapters_data)}")
    print("\n" + "="*60)
    print("✨ Terminé avec succès !")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
