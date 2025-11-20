#!/usr/bin/env python3
"""
Script to restore sidebar to all converter pages
"""

import os
import re

def restore_sidebar(filepath):
    """Restore sidebar CSS and HTML to a converter page"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Step 1: Update body CSS - add display: flex
    content = re.sub(
        r'body\s*\{\s*font-family:([^}]+?)min-height:\s*100vh;\s*\}',
        r'body { font-family:\1min-height: 100vh; display: flex; }',
        content,
        flags=re.DOTALL
    )
    
    # Step 2: Add sidebar CSS after body CSS
    # Find where to insert sidebar CSS (after body style)
    body_style_pattern = r'(body\s*\{[^}]+\})'
    sidebar_css = """
        .sidebar { width: 250px; background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); padding: 2rem 0; position: fixed; height: 100vh; left: 0; top: 0; border-right: 1px solid rgba(255, 255, 255, 0.2); }
        .logo { text-align: center; margin-bottom: 3rem; padding: 0 1rem; }
        .logo h1 { color: white; font-size: 2.5rem; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }"""
    
    if re.search(body_style_pattern, content) and '.sidebar' not in content:
        content = re.sub(
            body_style_pattern,
            r'\1' + sidebar_css,
            content,
            count=1
        )
    
    # Step 3: Update .main-content margin-left from 0 to 250px
    content = re.sub(
        r'\.main-content\s*\{\s*margin-left:\s*0;',
        r'.main-content { margin-left: 250px;',
        content
    )
    
    # Step 4: Update media query - add .sidebar { display: none; }
    content = re.sub(
        r'@media\s*\(\s*max-width:\s*768px\s*\)\s*\{\s*\.main-content',
        r'@media (max-width: 768px) { .sidebar { display: none; } .main-content',
        content
    )
    
    # Step 5: Add sidebar HTML div before main-content
    # Remove the stray </div> if it exists
    content = re.sub(
        r'</head>\s*<body>\s*</div>\s*<div class="main-content">',
        r'</head>\n<body>\n    <div class="sidebar"><div class="logo"><h1>S</h1></div></div>\n    <div class="main-content">',
        content
    )
    
    # If the stray </div> wasn't there, add sidebar HTML normally
    if '<div class="sidebar">' not in content:
        content = re.sub(
            r'</head>\s*<body>\s*<div class="main-content">',
            r'</head>\n<body>\n    <div class="sidebar"><div class="logo"><h1>S</h1></div></div>\n    <div class="main-content">',
            content
        )
    
    # Only write if changes were made
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    frontend_dir = 'frontend'
    
    # Files to exclude (non-converter pages)
    exclude_files = {
        'index.html', 'login.html', 'register.html', 'verify-email.html',
        'dashboard.html', 'about.html', 'contact.html', 'privacy.html',
        'terms.html', 'forgot-password.html', 'reset-password.html'
    }
    
    converter_files = []
    for filename in os.listdir(frontend_dir):
        if filename.endswith('.html') and filename not in exclude_files:
            converter_files.append(os.path.join(frontend_dir, filename))
    
    print(f"🔧 Restoring sidebar to {len(converter_files)} converter pages...\n")
    
    updated_count = 0
    for filepath in sorted(converter_files):
        if restore_sidebar(filepath):
            filename = os.path.basename(filepath)
            print(f"  ✅ Updated: {filename}")
            updated_count += 1
    
    print(f"\n✨ Done! Restored sidebar to {updated_count} converter pages.")

if __name__ == '__main__':
    main()
