#!/usr/bin/env python3
"""
Simple HTML to DOCX Converter
Uses basic text processing to create a Word-compatible document
"""
import os
import sys
from pathlib import Path
import re

def html_to_docx_content(html_file):
    """Extract text content from HTML and format for Word"""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove HTML tags and convert to plain text with formatting markers
    content = re.sub(r'<style>.*?</style>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script>.*?</script>', '', content, flags=re.DOTALL)
    
    # Convert headers
    content = re.sub(r'<h1>(.*?)</h1>', r'\n\n# \1\n\n', content)
    content = re.sub(r'<h2>(.*?)</h2>', r'\n\n## \1\n\n', content)
    content = re.sub(r'<h3>(.*?)</h3>', r'\n\n### \1\n\n', content)
    content = re.sub(r'<h4>(.*?)</h4>', r'\n\n#### \1\n\n', content)
    
    # Convert formatting
    content = re.sub(r'<strong>(.*?)</strong>', r'**\1**', content)
    content = re.sub(r'<b>(.*?)</b>', r'**\1**', content)
    content = re.sub(r'<em>(.*?)</em>', r'*\1*', content)
    content = re.sub(r'<i>(.*?)</i>', r'*\1*', content)
    content = re.sub(r'<code>(.*?)</code>', r'`\1`', content)
    
    # Convert lists
    content = re.sub(r'<ul[^>]*>', '\n', content)
    content = re.sub(r'</ul>', '\n', content)
    content = re.sub(r'<ol[^>]*>', '\n', content)
    content = re.sub(r'</ol>', '\n', content)
    content = re.sub(r'<li>(.*?)</li>', r'- \1\n', content)
    
    # Convert paragraphs
    content = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', content)
    
    # Convert code blocks
    content = re.sub(r'<pre[^>]*>(.*?)</pre>', r'\n```\n\1\n```\n', content, flags=re.DOTALL)
    
    # Convert tables (basic)
    content = re.sub(r'<table[^>]*>', '\n', content)
    content = re.sub(r'</table>', '\n', content)
    content = re.sub(r'<thead[^>]*>', '', content)
    content = re.sub(r'</thead>', '', content)
    content = re.sub(r'<tbody[^>]*>', '', content)
    content = re.sub(r'</tbody>', '', content)
    content = re.sub(r'<tr[^>]*>', '', content)
    content = re.sub(r'</tr>', '\n', content)
    content = re.sub(r'<th[^>]*>(.*?)</th>', r'| **\1** ', content)
    content = re.sub(r'<td[^>]*>(.*?)</td>', r'| \1 ', content)
    
    # Clean up remaining HTML tags
    content = re.sub(r'<[^>]+>', '', content)
    
    # Decode HTML entities
    content = content.replace('&lt;', '<')
    content = content.replace('&gt;', '>')
    content = content.replace('&amp;', '&')
    content = content.replace('&quot;', '"')
    content = content.replace('&#39;', "'")
    
    # Clean up whitespace
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    content = re.sub(r'^\s*\n', '', content)
    
    return content.strip()

def create_docx_from_text(text_content, output_file):
    """Create a simple text file that can be opened in Word"""
    
    # Add RTF headers for better Word compatibility
    rtf_content = r"""{\rtf1\ansi\deff0 {\fonttbl {\f0 Times New Roman;}}
{\colortbl;\red0\green0\blue0;\red0\green0\blue255;}
\f0\fs24 
""" + text_content.replace('\n', r'\par ') + "}"
    
    # Save as RTF for Word compatibility
    rtf_file = output_file.with_suffix('.rtf')
    with open(rtf_file, 'w', encoding='utf-8') as f:
        f.write(rtf_content)
    
    print(f"Created RTF file: {rtf_file}")
    
    # Also save as plain text that can be imported to Word
    txt_file = output_file.with_suffix('.txt')
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(text_content)
    
    print(f"Created text file: {txt_file}")

def main():
    """Main conversion function"""
    
    current_dir = Path(__file__).parent
    html_file = current_dir / "AI_Self_Healing_Framework_Overview.html"
    output_file = current_dir / "AI_Self_Healing_Framework_Overview.docx"
    
    if not html_file.exists():
        print(f"Error: HTML file not found at {html_file}")
        return 1
    
    try:
        # Extract text content from HTML
        text_content = html_to_docx_content(html_file)
        
        # Create Word-compatible files
        create_docx_from_text(text_content, output_file)
        
        print("\n" + "="*70)
        print("AI SELF-HEALING FRAMEWORK - WORD-COMPATIBLE FILES CREATED")
        print("="*70)
        print(f"📁 Location: {current_dir}")
        print(f"📄 RTF File: AI_Self_Healing_Framework_Overview.rtf")
        print(f"📄 Text File: AI_Self_Healing_Framework_Overview.txt")
        print("\n💡 How to create DOCX:")
        print("Option 1: Open RTF file in Microsoft Word and save as DOCX")
        print("Option 2: Open HTML file in Word and save as DOCX")
        print("Option 3: Copy content from text file into new Word document")
        print("\n✅ Files ready for conversion to DOCX format!")
        print("="*70)
        
        return 0
        
    except Exception as e:
        print(f"Error during conversion: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())