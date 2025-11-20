#!/usr/bin/env python3
"""
Script to remove sidebar from all converter pages
"""

import os
import re
from pathlib import Path

def remove_sidebar_from_file(filepath):
    """Remove sidebar and update styles in a converter HTML file"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if file has sidebar
    if '.sidebar' not in content:
        print(f"  ⏭️  No sidebar found in {filepath.name}")
        return False
    
    # Replace sidebar CSS and related styles
    # Remove sidebar definition
    content = re.sub(
        r'\.sidebar\s*\{[^}]+\}',
        '',
        content
    )
    
    # Remove logo styles
    content = re.sub(
        r'\.logo\s*\{[^}]+\}',
        '',
        content
    )
    
    content = re.sub(
        r'\.logo\s+h1\s*\{[^}]+\}',
        '',
        content
    )
    
    # Update main-content to remove margin-left
    content = re.sub(
        r'\.main-content\s*\{\s*margin-left:\s*250px;',
        '.main-content { margin-left: 0;',
        content
    )
    
    # Update body styles to remove display: flex
    content = re.sub(
        r'body\s*\{([^}]*?)display:\s*flex;',
        r'body { \1',
        content
    )
    
    # Remove sidebar HTML element
    content = re.sub(
        r'<div class="sidebar">.*?</div>\s*',
        '',
        content,
        flags=re.DOTALL
    )
    
    # Update media query to remove sidebar display:none
    content = re.sub(
        r'@media\s*\([^)]*\)\s*\{\s*\.sidebar\s*\{\s*display:\s*none;\s*\}',
        '@media (max-width: 768px) {',
        content
    )
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    # Get frontend directory
    frontend_dir = Path('/Users/perera/Downloads/Sigiri/frontend')
    
    # Get all HTML files
    html_files = list(frontend_dir.glob('*.html'))
    
    # Filter converter pages (exclude index, login, dashboard, etc.)
    exclude_files = {
        'index.html', 'login.html', 'dashboard.html', 'verify-email.html',
        'about.html', 'contact.html', 'privacy-policy.html', 'terms-of-service.html',
        'cookie-policy.html', 'features.html', 'pricing.html', 'brand.html',
        'projects.html', 'templates.html', 'converters.html', 
        'login-old-backup.html', 'login-new.html'
    }
    
    converter_files = [f for f in html_files if f.name not in exclude_files]
    
    print(f"\n🔧 Removing sidebar from {len(converter_files)} converter pages...\n")
    
    updated_count = 0
    for filepath in sorted(converter_files):
        if remove_sidebar_from_file(filepath):
            print(f"  ✅ Updated: {filepath.name}")
            updated_count += 1
    
    print(f"\n✨ Done! Updated {updated_count} converter pages.")
    print(f"   All converter pages now use full width without sidebar.\n")

if __name__ == '__main__':
    main()
