#!/usr/bin/env python3
"""
AI Self-Healing Framework Documentation Generator
Simplified version using built-in libraries to create DOCX-style content
"""
import os
import sys
from pathlib import Path
import html

def markdown_to_html(markdown_file, output_file):
    """Convert markdown to HTML with DOCX-like styling"""
    
    # Read markdown file
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # HTML template with Word-like styling
    html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AI Self-Healing Framework Overview</title>
    <style>
        body {
            font-family: 'Calibri', Arial, sans-serif;
            line-height: 1.6;
            max-width: 8.5in;
            margin: 0 auto;
            padding: 1in;
            background: white;
            color: #333;
        }
        
        h1 {
            color: #2E75B6;
            font-size: 24pt;
            text-align: center;
            margin-bottom: 20pt;
            border-bottom: 3px solid #2E75B6;
            padding-bottom: 10pt;
        }
        
        h2 {
            color: #2E75B6;
            font-size: 18pt;
            margin-top: 24pt;
            margin-bottom: 12pt;
            border-left: 4px solid #2E75B6;
            padding-left: 10pt;
        }
        
        h3 {
            color: #365F91;
            font-size: 16pt;
            margin-top: 18pt;
            margin-bottom: 9pt;
            font-weight: bold;
        }
        
        h4 {
            color: #365F91;
            font-size: 14pt;
            margin-top: 14pt;
            margin-bottom: 7pt;
            font-weight: bold;
        }
        
        p {
            margin-bottom: 12pt;
            text-align: justify;
        }
        
        code {
            font-family: 'Consolas', monospace;
            background-color: #f5f5f5;
            padding: 2px 4px;
            border-radius: 3px;
            font-size: 90%;
        }
        
        pre {
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15pt;
            margin: 12pt 0;
            font-family: 'Consolas', monospace;
            font-size: 10pt;
            overflow-x: auto;
            white-space: pre-wrap;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15pt 0;
            border: 1px solid #ddd;
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 8pt 12pt;
            text-align: left;
            vertical-align: top;
        }
        
        th {
            background-color: #2E75B6;
            color: white;
            font-weight: bold;
        }
        
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        ul, ol {
            margin: 12pt 0;
            padding-left: 30pt;
        }
        
        li {
            margin-bottom: 6pt;
        }
        
        .emoji {
            font-size: 1.2em;
        }
        
        .highlight {
            background-color: #fff2cc;
            padding: 2px 4px;
            border-radius: 3px;
        }
        
        .success {
            color: #28a745;
            font-weight: bold;
        }
        
        .fail {
            color: #dc3545;
            font-weight: bold;
        }
        
        .architecture-box {
            background-color: #f0f8ff;
            border: 1px solid #2E75B6;
            border-radius: 8px;
            padding: 15pt;
            margin: 15pt 0;
        }
        
        @media print {
            body { margin: 0; }
            .page-break { page-break-before: always; }
        }
    </style>
</head>
<body>
"""
    
    # Process markdown content
    html_content = process_markdown_content(content)
    
    # Complete HTML
    full_html = html_template + html_content + "\n</body>\n</html>"
    
    # Write HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"Successfully converted to HTML: {output_file}")

def process_markdown_content(content):
    """Process markdown content and convert to HTML"""
    lines = content.split('\n')
    html_lines = []
    in_code_block = False
    in_table = False
    table_headers = []
    
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        
        # Code block detection
        if line.startswith('```'):
            if in_code_block:
                html_lines.append('</pre>')
                in_code_block = False
            else:
                language = line[3:].strip()
                html_lines.append(f'<pre>')
                in_code_block = True
            i += 1
            continue
        
        if in_code_block:
            html_lines.append(html.escape(line))
            i += 1
            continue
        
        # Headers
        if line.startswith('# '):
            html_lines.append(f'<h1>{html.escape(line[2:])}</h1>')
        elif line.startswith('## '):
            html_lines.append(f'<h2>{html.escape(line[3:])}</h2>')
        elif line.startswith('### '):
            html_lines.append(f'<h3>{html.escape(line[4:])}</h3>')
        elif line.startswith('#### '):
            html_lines.append(f'<h4>{html.escape(line[5:])}</h4>')
        
        # Tables
        elif '|' in line and line.count('|') >= 2:
            if not in_table:
                html_lines.append('<table>')
                in_table = True
                
                # Process header row
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                table_headers = cells
                html_lines.append('<thead><tr>')
                for cell in cells:
                    html_lines.append(f'<th>{html.escape(cell.strip("*"))}</th>')
                html_lines.append('</tr></thead><tbody>')
                
                # Skip separator line
                i += 1
                if i < len(lines) and '---' in lines[i]:
                    i += 1
                continue
            else:
                # Data row
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                html_lines.append('<tr>')
                for cell in cells:
                    processed_cell = process_inline_formatting(cell.strip('*'))
                    html_lines.append(f'<td>{processed_cell}</td>')
                html_lines.append('</tr>')
        
        # End table if not a table line
        elif in_table and '|' not in line:
            html_lines.append('</tbody></table>')
            in_table = False
            # Process this line normally
            continue
        
        # Lists
        elif line.startswith('- ') or line.startswith('* '):
            text = process_inline_formatting(line[2:].strip())
            html_lines.append(f'<ul><li>{text}</li></ul>')
        elif line.startswith('├─ ') or line.startswith('└─ '):
            text = process_inline_formatting(line[3:].strip())
            html_lines.append(f'<ul style="margin-left: 20pt;"><li>{text}</li></ul>')
        
        # Regular paragraphs
        elif line.strip():
            processed_line = process_inline_formatting(line.strip())
            html_lines.append(f'<p>{processed_line}</p>')
        else:
            html_lines.append('<br>')
        
        i += 1
    
    # Close any open table
    if in_table:
        html_lines.append('</tbody></table>')
    
    return '\n'.join(html_lines)

def process_inline_formatting(text):
    """Process inline formatting like bold, code, etc."""
    # Bold text
    text = text.replace('**', '<strong>', 1)
    if '<strong>' in text:
        text = text.replace('**', '</strong>', 1)
    
    # Inline code
    import re
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    
    # Emojis (simple replacement)
    emoji_map = {
        '🎯': '<span class="emoji">🎯</span>',
        '🏗️': '<span class="emoji">🏗️</span>',
        '📚': '<span class="emoji">📚</span>',
        '🔧': '<span class="emoji">🔧</span>',
        '🛒': '<span class="emoji">🛒</span>',
        '🤖': '<span class="emoji">🤖</span>',
        '📊': '<span class="emoji">📊</span>',
        '🔄': '<span class="emoji">🔄</span>',
        '🎓': '<span class="emoji">🎓</span>',
        '⚙️': '<span class="emoji">⚙️</span>',
        '🚀': '<span class="emoji">🚀</span>',
        '📈': '<span class="emoji">📈</span>',
        '🎉': '<span class="emoji">🎉</span>',
        '✅': '<span class="emoji success">✅</span>',
        '❌': '<span class="emoji fail">❌</span>',
    }
    
    for emoji, replacement in emoji_map.items():
        text = text.replace(emoji, replacement)
    
    return html.escape(text, quote=False)

def main():
    """Main function to handle the conversion"""
    
    # File paths
    current_dir = Path(__file__).parent
    ai_folder = current_dir
    
    markdown_file = ai_folder / "AI_Self_Healing_Framework_Overview.md"
    html_file = ai_folder / "AI_Self_Healing_Framework_Overview.html"
    
    # Check if markdown file exists
    if not markdown_file.exists():
        print(f"Error: Markdown file not found at {markdown_file}")
        return 1
    
    # Convert to HTML (Word-compatible)
    try:
        markdown_to_html(markdown_file, html_file)
        
        print("\n" + "="*60)
        print("AI SELF-HEALING FRAMEWORK DOCUMENTATION GENERATED")
        print("="*60)
        print(f"📁 Location: {ai_folder}")
        print(f"📄 HTML File: {html_file.name}")
        print(f"📊 Size: {html_file.stat().st_size / 1024:.1f} KB")
        print("\n💡 Instructions:")
        print("1. Open the HTML file in any web browser")
        print("2. Use browser's 'Print' or 'Save as PDF' function")
        print("3. Or open in Microsoft Word and save as DOCX")
        print("\n✅ Document ready for stakeholder distribution!")
        print("="*60)
        
        return 0
        
    except Exception as e:
        print(f"Error during conversion: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())