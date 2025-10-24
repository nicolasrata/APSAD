#!/usr/bin/env python3
"""
Script de reconstruction LOCAL - VERSION FINALE AVEC IMAGES
Préserve les positions, force le texte visible ET inclut les images
"""

import os
import glob
from bs4 import BeautifulSoup
import re
from collections import OrderedDict
import base64

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

def extract_images_from_canvas(html_content):
    """
    Extrait les images des balises canvas (si présentes)
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    canvases = soup.find_all('canvas')
    
    images_html = []
    for canvas in canvases:
        # Récupérer les attributs du canvas
        canvas_html = str(canvas)
        images_html.append(canvas_html)
    
    return images_html

def extract_images_from_img_tags(html_content):
    """
    Extrait les balises <img> présentes dans le HTML
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    images = soup.find_all('img')
    
    images_html = []
    for img in images:
        images_html.append(str(img))
    
    return images_html

def extract_page_content(html_content):
    """
    Extrait le contenu complet d'une page : textLayer + images + canvas
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Chercher les div qui contiennent le contenu d'une page
    # Généralement dans des div avec classe 'page'
    pages = soup.find_all('div', class_='page')
    
    if not pages:
        # Si pas de div.page, chercher d'autres structures communes
        pages = soup.find_all('div', id=re.compile(r'page\d+'))
    
    pages_content = []
    
    for page in pages:
        # Créer une copie de la page
        page_copy = BeautifulSoup(str(page), 'html.parser')
        
        # Trouver le textLayer dans cette page
        text_layer = page_copy.find('div', class_='textLayer')
        
        if text_layer:
            # Forcer le texte visible dans le textLayer
            for div in text_layer.find_all('div', recursive=False):
                if 'endOfContent' in div.get('class', []):
                    continue
                
                style = div.get('style', '')
                style = re.sub(r'color:\s*transparent\s*;?', '', style)
                
                if 'color:' not in style:
                    style += '; color: #000;'
                else:
                    style = re.sub(r'color:\s*[^;]+', 'color: #000', style)
                
                div['style'] = style
        
        # Récupérer tout le contenu de la page (textLayer + canvasWrapper + images)
        page_html = str(page_copy)
        
        if len(page_html) > 100:
            pages_content.append(page_html)
    
    return pages_content

def extract_text_and_images(html_content):
    """
    Nouvelle méthode : extrait textLayer ET cherche les images/canvas
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Méthode 1: Chercher les pages complètes
    pages_content = extract_page_content(html_content)
    if pages_content:
        return pages_content
    
    # Méthode 2: Si pas de structure de page, extraire séparément
    text_layers = soup.find_all('div', class_='textLayer')
    canvas_wrappers = soup.find_all('div', class_='canvasWrapper')
    
    pages_html = []
    
    # Combiner textLayer et canvasWrapper par paires
    max_len = max(len(text_layers), len(canvas_wrappers))
    
    for i in range(max_len):
        page_parts = []
        
        # Ajouter le canvas si présent
        if i < len(canvas_wrappers):
            canvas_html = str(canvas_wrappers[i])
            page_parts.append(canvas_html)
        
        # Ajouter le textLayer si présent
        if i < len(text_layers):
            text_layer = text_layers[i]
            
            # Forcer le texte visible
            for div in text_layer.find_all('div', recursive=False):
                if 'endOfContent' in div.get('class', []):
                    continue
                
                style = div.get('style', '')
                style = re.sub(r'color:\s*transparent\s*;?', '', style)
                
                if 'color:' not in style:
                    style += '; color: #000;'
                else:
                    style = re.sub(r'color:\s*[^;]+', 'color: #000', style)
                
                div['style'] = style
            
            text_html = str(text_layer)
            page_parts.append(text_html)
        
        if page_parts:
            combined_html = '<div class="page-content">\n' + '\n'.join(page_parts) + '\n</div>'
            pages_html.append(combined_html)
    
    return pages_html

def create_chapter_title(filename):
    """Crée un titre de section à partir du nom de fichier"""
    basename = os.path.basename(filename)
    match = re.search(r'; ([^-]+) -', basename)
    if match:
        title = match.group(1).strip()
        return title
    return 'Section'

def generate_html_with_images(chapters_data):
    """Génère le HTML avec mise en page, texte visible ET images"""
    
    html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>APSAD D20 - Document complet avec images</title>
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
            max-width: 900px;
        }
        .page-content {
            position: relative;
            width: 100%;
            min-height: 800px;
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
            z-index: 10;
        }
        
        /* Styles pour les canvas (images de fond) */
        .canvasWrapper {
            position: relative;
            width: 100%;
        }
        .canvasWrapper canvas {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: auto;
        }
        
        /* Images */
        img {
            max-width: 100%;
            height: auto;
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
            z-index: 2; /* Au-dessus des canvas */
        }
        .textLayer > div {
            color: #000 !important;
            position: absolute;
            white-space: pre;
            cursor: text;
            transform-origin: 0% 0%;
            opacity: 1 !important;
        }
        
        /* S'assurer que le texte est toujours visible */
        .textLayer * {
            color: #000 !important;
            opacity: 1 !important;
        }
        
        /* Styles pour la structure de page complète */
        .page {
            position: relative;
            width: 100%;
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
                Document complet avec texte, mise en page et images
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
            <strong>📊 Statistiques :</strong> {len(chapters_data)} sections • {total_pages} pages • Images incluses
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
    print("🔧 RECONSTRUCTION APSAD D20 - VERSION FINALE AVEC IMAGES")
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
    print("📖 Extraction : texte + images + mise en page...\n")
    chapters_data = OrderedDict()
    total_pages = 0
    
    for filepath in sorted_files:
        try:
            html_content = read_html_file(filepath)
            pages_html = extract_text_and_images(html_content)
            
            if pages_html:
                chapters_data[filepath] = pages_html
                total_pages += len(pages_html)
                print(f"   ✓ {len(pages_html)} pages extraites (texte + images)")
            else:
                print(f"   ⚠️  Aucun contenu extrait")
                
        except Exception as e:
            print(f"   ✗ Erreur: {e}")
    
    if not chapters_data:
        print("\n❌ Aucun contenu n'a pu être extrait!\n")
        return
    
    # Génération
    print(f"\n📝 Génération du HTML final ({total_pages} pages)...")
    final_html = generate_html_with_images(chapters_data)
    
    # Sauvegarde
    output_file = "APSAD_D20_Document_Final.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"\n✅ Document créé : {output_file}")
    print(f"   📊 Taille : {len(final_html):,} caractères")
    print(f"   📄 Sections : {len(chapters_data)}")
    print(f"   📑 Pages : {total_pages}")
    print(f"   🎨 Texte visible + Mise en page + Images")
    print(f"\n🌐 Ouvre le fichier :")
    print(f"   open {output_file}")
    print("\n" + "="*70)
    print("✨ Terminé avec succès !")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
