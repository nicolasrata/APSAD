#!/usr/bin/env python3
"""
Script de reconstruction du document APSAD D20 complet
À partir des fichiers HTML individuels sur GitHub
"""

import requests
from bs4 import BeautifulSoup
import re
from collections import OrderedDict

# Configuration
GITHUB_API = "https://api.github.com/repos/nicolasrata/APSAD/contents"
GITHUB_RAW = "https://raw.githubusercontent.com/nicolasrata/APSAD/main/"

def get_files_list():
    """Récupère la liste des fichiers du dépôt"""
    response = requests.get(GITHUB_API)
    response.raise_for_status()
    return response.json()

def extract_chapter_number(filename):
    """Extrait le numéro de chapitre/annexe pour le tri"""
    # Pages liminaires = 0
    if "Pages liminaires" in filename:
        return (0, 0)
    # Sommaire = 0.5
    if "Sommaire" in filename:
        return (0, 5)
    # Chapitres 1-8
    match = re.search(r'; (\d+)\. ', filename)
    if match:
        return (1, int(match.group(1)))
    # Annexes
    match = re.search(r'Annexe (\d+)', filename)
    if match:
        annexe_num = match.group(1)
        if '-' in annexe_num:
            parts = annexe_num.split('-')
            return (2, int(parts[0]), int(parts[1]))
        return (2, int(annexe_num), 0)
    return (999, 0)  # Fichiers non reconnus à la fin

def download_html(filename):
    """Télécharge un fichier HTML"""
    url = GITHUB_RAW + requests.utils.quote(filename)
    print(f"Téléchargement: {filename[:60]}...")
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def extract_text_layers(html_content):
    """Extrait les textLayer d'un fichier HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')
    text_layers = soup.find_all('div', class_='textLayer')
    
    pages_content = []
    for layer in text_layers:
        # Récupère tout le contenu de la textLayer
        pages_content.append(str(layer))
    
    return pages_content

def extract_styles(html_content):
    """Extrait les styles CSS nécessaires"""
    soup = BeautifulSoup(html_content, 'html.parser')
    styles = []
    
    # Récupère les balises <style>
    for style_tag in soup.find_all('style'):
        styles.append(style_tag.string)
    
    return '\n'.join(styles) if styles else ''

def create_chapter_title(filename):
    """Crée un titre de section à partir du nom de fichier"""
    # Extraire le titre entre les points-virgules
    match = re.search(r'; ([^-]+) -', filename)
    if match:
        title = match.group(1).strip()
        return f'<div class="chapter-title"><h1>{title}</h1></div>'
    return ''

def generate_complete_html(chapters_data):
    """Génère le HTML complet"""
    
    html_parts = [
        '<!DOCTYPE html>',
        '<html lang="fr">',
        '<head>',
        '    <meta charset="UTF-8">',
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '    <title>Référentiel APSAD D20 - Installation photovoltaïques - Document complet</title>',
        '    <style>',
        '        body {',
        '            font-family: Arial, sans-serif;',
        '            margin: 0;',
        '            padding: 20px;',
        '            background-color: #f5f5f5;',
        '        }',
        '        .container {',
        '            max-width: 1200px;',
        '            margin: 0 auto;',
        '            background: white;',
        '            padding: 40px;',
        '            box-shadow: 0 0 10px rgba(0,0,0,0.1);',
        '        }',
        '        .chapter-title {',
        '            margin: 60px 0 30px 0;',
        '            padding: 20px;',
        '            background: #003366;',
        '            color: white;',
        '            page-break-before: always;',
        '        }',
        '        .chapter-title h1 {',
        '            margin: 0;',
        '            font-size: 24px;',
        '        }',
        '        .page-content {',
        '            margin: 20px 0;',
        '            position: relative;',
        '            min-height: 800px;',
        '        }',
        '        .textLayer {',
        '            position: relative;',
        '            left: 0;',
        '            top: 0;',
        '            right: 0;',
        '            bottom: 0;',
        '            overflow: hidden;',
        '            opacity: 1;',
        '            line-height: 1.0;',
        '        }',
        '        .textLayer > span {',
        '            color: transparent;',
        '            position: absolute;',
        '            white-space: pre;',
        '            cursor: text;',
        '            transform-origin: 0% 0%;',
        '        }',
    ]
    
    # Ajouter les styles extraits
    for filename, data in chapters_data.items():
        if data['styles']:
            html_parts.append(f'        /* Styles de {filename[:40]}... */')
            html_parts.append(data['styles'])
    
    html_parts.extend([
        '    </style>',
        '</head>',
        '<body>',
        '    <div class="container">',
        '        <div class="document-header">',
        '            <h1 style="text-align: center; color: #003366; font-size: 32px; margin-bottom: 40px;">',
        '                Référentiel APSAD D20<br>',
        '                Installations photovoltaïques<br>',
        '                <small style="font-size: 18px; font-weight: normal;">Document complet reconstruit</small>',
        '            </h1>',
        '        </div>',
    ])
    
    # Ajouter chaque chapitre
    for filename, data in chapters_data.items():
        html_parts.append(data['title'])
        for i, page in enumerate(data['pages']):
            html_parts.append(f'        <!-- Page {i+1} de {filename[:50]}... -->')
            html_parts.append(f'        <div class="page-content">')
            html_parts.append(page)
            html_parts.append('        </div>')
    
    html_parts.extend([
        '    </div>',
        '</body>',
        '</html>'
    ])
    
    return '\n'.join(html_parts)

def main():
    """Fonction principale"""
    print("=== Reconstruction du document APSAD D20 ===\n")
    
    # 1. Récupérer la liste des fichiers
    print("1. Récupération de la liste des fichiers...")
    files = get_files_list()
    html_files = [f for f in files if f['name'].endswith('.html')]
    print(f"   Trouvés: {len(html_files)} fichiers HTML\n")
    
    # 2. Trier les fichiers
    print("2. Tri des fichiers par ordre logique...")
    sorted_files = sorted(html_files, key=lambda x: extract_chapter_number(x['name']))
    
    # 3. Télécharger et extraire le contenu
    print("3. Téléchargement et extraction du contenu...\n")
    chapters_data = OrderedDict()
    
    for file_info in sorted_files:
        filename = file_info['name']
        try:
            # Télécharger
            html_content = download_html(filename)
            
            # Extraire
            pages = extract_text_layers(html_content)
            styles = extract_styles(html_content)
            title = create_chapter_title(filename)
            
            chapters_data[filename] = {
                'pages': pages,
                'styles': styles,
                'title': title
            }
            
            print(f"   ✓ {len(pages)} pages extraites")
            
        except Exception as e:
            print(f"   ✗ Erreur: {e}")
    
    # 4. Générer le HTML final
    print("\n4. Génération du document HTML complet...")
    final_html = generate_complete_html(chapters_data)
    
    # 5. Sauvegarder
    output_file = "APSAD_D20_Document_Complet.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"\n✓ Document créé: {output_file}")
    print(f"   Taille: {len(final_html):,} caractères")
    print("\n=== Terminé ===")

if __name__ == "__main__":
    main()
