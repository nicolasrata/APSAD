#!/usr/bin/env python3
"""
Script de reconstruction LOCAL - VERSION FINALE OPTIMALE
Image de fond + texte transparent sélectionnable par-dessus
Reproduit exactement la structure PDF + Filtre les pages vides
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

def has_text_content(text_layer):
    """
    Vérifie si un textLayer contient du texte réel (pas juste endOfContent)
    """
    if not text_layer:
        return False
    
    # Trouver tous les div enfants
    divs = text_layer.find_all('div', recursive=False)
    
    # Compter les divs avec du contenu réel
    content_divs = 0
    for div in divs:
        # Ignorer les divs endOfContent
        if 'endOfContent' in div.get('class', []):
            continue
        
        # Vérifier si le div a du texte
        text = div.get_text(strip=True)
        if text:
            content_divs += 1
    
    # La page a du contenu si au moins un div contient du texte
    return content_divs > 0

def extract_page_structure(html_content):
    """
    Extrait la structure complète : canvas (image) + textLayer (texte transparent)
    Garde le texte transparent pour qu'il soit sélectionnable mais invisible
    Filtre les pages vides
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Chercher les structures de page
    pages = soup.find_all('div', class_='page')
    
    if not pages:
        # Chercher d'autres structures possibles
        pages = soup.find_all('div', id=re.compile(r'page\d+'))
    
    if not pages:
        # Essayer de reconstruire manuellement
        return extract_manual_structure(soup)
    
    pages_html = []
    skipped_pages = 0
    
    for page in pages:
        # Vérifier si la page contient du texte
        text_layer = page.find('div', class_='textLayer')
        
        if not has_text_content(text_layer):
            skipped_pages += 1
            continue  # Sauter cette page vide
        
        # Garder la page telle quelle, mais s'assurer que le textLayer est transparent
        page_copy = BeautifulSoup(str(page), 'html.parser')
        
        # Trouver le textLayer
        text_layer = page_copy.find('div', class_='textLayer')
        
        if text_layer:
            # Garder le texte transparent mais sélectionnable
            for div in text_layer.find_all('div', recursive=False):
                if 'endOfContent' in div.get('class', []):
                    continue
                
                style = div.get('style', '')
                
                # S'assurer que le texte est transparent
                if 'color:' not in style:
                    style += '; color: transparent;'
                elif 'transparent' not in style:
                    style = re.sub(r'color:\s*[^;]+', 'color: transparent', style)
                
                div['style'] = style
        
        page_html = str(page_copy)
        
        if len(page_html) > 100:
            pages_html.append(page_html)
    
    if skipped_pages > 0:
        print(f"      → {skipped_pages} pages vides ignorées")
    
    return pages_html

def extract_manual_structure(soup):
    """
    Si pas de structure de page, reconstruire manuellement
    Filtre les pages vides
    """
    canvas_wrappers = soup.find_all('div', class_='canvasWrapper')
    text_layers = soup.find_all('div', class_='textLayer')
    
    pages_html = []
    skipped_pages = 0
    max_len = max(len(canvas_wrappers), len(text_layers))
    
    for i in range(max_len):
        # Vérifier si le textLayer de cette page contient du texte
        if i < len(text_layers):
            text_layer_soup = BeautifulSoup(str(text_layers[i]), 'html.parser')
            text_layer = text_layer_soup.find('div', class_='textLayer')
            
            if not has_text_content(text_layer):
                skipped_pages += 1
                continue  # Sauter cette page vide
        else:
            # Pas de textLayer du tout
            skipped_pages += 1
            continue
        
        page_html = '<div class="page">\n'
        
        # Ajouter le canvas (image de fond)
        if i < len(canvas_wrappers):
            page_html += str(canvas_wrappers[i]) + '\n'
        
        # Ajouter le textLayer (texte transparent)
        if i < len(text_layers):
            text_layer = BeautifulSoup(str(text_layers[i]), 'html.parser').find('div', class_='textLayer')
            
            if text_layer:
                # Garder le texte transparent
                for div in text_layer.find_all('div', recursive=False):
                    if 'endOfContent' in div.get('class', []):
                        continue
                    
                    style = div.get('style', '')
                    
                    if 'color:' not in style:
                        style += '; color: transparent;'
                    elif 'transparent' not in style:
                        style = re.sub(r'color:\s*[^;]+', 'color: transparent', style)
                    
                    div['style'] = style
                
                page_html += str(text_layer) + '\n'
        
        page_html += '</div>'
        
        if len(page_html) > 100:
            pages_html.append(page_html)
    
    if skipped_pages > 0:
        print(f"      → {skipped_pages} pages vides ignorées")
    
    return pages_html

def create_chapter_title(filename):
    """Crée un titre de section à partir du nom de fichier"""
    basename = os.path.basename(filename)
    match = re.search(r'; ([^-]+) -', basename)
    if match:
        title = match.group(1).strip()
        return title
    return 'Section'

def generate_html_pdf_style(chapters_data):
    """Génère le HTML avec structure PDF : image + texte transparent"""
    
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
            padding: 20px;
            max-width: 900px;
        }
        .page-number {
            position: absolute;
            top: 10px;
            right: 20px;
            color: #999;
            font-size: 0.9em;
            font-style: italic;
            background: rgba(249, 249, 249, 0.9);
            padding: 5px 10px;
            border-radius: 3px;
            z-index: 100;
        }
        
        /* Structure de page : image + texte superposé */
        .page {
            position: relative;
            width: 100%;
            margin: 0 auto;
        }
        
        /* Canvas (image de fond) */
        .canvasWrapper {
            position: relative;
            width: 100%;
            display: block;
        }
        .canvasWrapper canvas {
            display: block;
            width: 100%;
            height: auto;
        }
        
        /* TextLayer (texte transparent par-dessus) */
        .textLayer {
            position: absolute;
            left: 0;
            top: 0;
            right: 0;
            bottom: 0;
            overflow: hidden;
            opacity: 1;
            line-height: 1.0;
            pointer-events: auto; /* Permettre la sélection */
        }
        
        .textLayer > div {
            color: transparent; /* Texte invisible */
            position: absolute;
            white-space: pre;
            cursor: text;
            transform-origin: 0% 0%;
        }
        
        /* Quand on sélectionne le texte, le montrer */
        .textLayer > div::selection {
            background: rgba(0, 100, 255, 0.3);
            color: #000; /* Montrer le texte sélectionné */
        }
        
        .textLayer > div::-moz-selection {
            background: rgba(0, 100, 255, 0.3);
            color: #000;
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
        .info-box {
            background: #fff8dc;
            border-left: 4px solid #ffa500;
            padding: 15px;
            margin: 20px 0;
            border-radius: 3px;
        }
        .info-box p {
            margin: 5px 0;
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
        
        <div class="info-box">
            <strong>ℹ️ Comment utiliser ce document :</strong>
            <p>• Le texte est <strong>sélectionnable</strong> (mais invisible, il est par-dessus l'image)</p>
            <p>• Utilisez <strong>Cmd+F</strong> pour rechercher du texte</p>
            <p>• Quand vous sélectionnez, le texte devient visible (en bleu)</p>
            <p>• Structure identique au PDF original : image + texte transparent</p>
            <p>• Les pages vides ont été automatiquement supprimées</p>
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
            <strong>📊 Statistiques :</strong> {len(chapters_data)} sections • {total_pages} pages avec contenu
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
    print("🔧 RECONSTRUCTION APSAD D20 - VERSION FINALE OPTIMALE")
    print("   Structure PDF : Image de fond + Texte transparent sélectionnable")
    print("   Filtrage automatique des pages vides")
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
    print("📖 Extraction structure PDF (filtrage des pages vides)...\n")
    chapters_data = OrderedDict()
    total_pages = 0
    total_skipped = 0
    
    for filepath in sorted_files:
        try:
            html_content = read_html_file(filepath)
            pages_html = extract_page_structure(html_content)
            
            if pages_html:
                chapters_data[filepath] = pages_html
                total_pages += len(pages_html)
                print(f"   ✓ {len(pages_html)} pages avec contenu extraites")
            else:
                print(f"   ⚠️  Aucun contenu (toutes les pages étaient vides)")
                
        except Exception as e:
            print(f"   ✗ Erreur: {e}")
    
    if not chapters_data:
        print("\n❌ Aucun contenu n'a pu être extrait!\n")
        return
    
    # Génération
    print(f"\n📝 Génération du HTML ({total_pages} pages avec contenu)...")
    final_html = generate_html_pdf_style(chapters_data)
    
    # Sauvegarde
    output_file = "APSAD_D20_Document_Final.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"\n✅ Document créé : {output_file}")
    print(f"   📊 Taille : {len(final_html):,} caractères")
    print(f"   📄 Sections : {len(chapters_data)}")
    print(f"   📑 Pages avec contenu : {total_pages}")
    print(f"   🗑️  Pages vides supprimées automatiquement")
    print(f"   🎨 Structure PDF : Image + Texte transparent sélectionnable")
    print(f"\n🌐 Ouvre le fichier :")
    print(f"   open {output_file}")
    print(f"\n💡 Le texte est invisible mais sélectionnable !")
    print(f"   Essaie de sélectionner du texte avec ta souris 🖱️")
    print("\n" + "="*70)
    print("✨ Terminé avec succès !")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
