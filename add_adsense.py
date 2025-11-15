#!/usr/bin/env python3
"""
Script to add Google AdSense code to converter pages that don't have it yet.
"""

import os
import re

# AdSense header script to add after Font Awesome link
ADSENSE_HEADER = '''    
    <!-- Google AdSense - Replace with your actual Publisher ID -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX"
     crossorigin="anonymous"></script>
'''

# AdSense ad unit templates
ADSENSE_AD_DISPLAY = '''
                    <!-- AdSense Display Ad -->
                    <ins class="adsbygoogle"
                         style="display:block"
                         data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
                         data-ad-slot="XXXXXXXXXX"
                         data-ad-format="auto"
                         data-full-width-responsive="true"></ins>
                    <script>
                         (adsbygoogle = window.adsbygoogle || []).push({});
                    </script>
'''

def add_adsense_to_file(filepath):
    """Add AdSense code to a single file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if AdSense is already present
        if 'adsbygoogle' in content:
            print(f"✓ {os.path.basename(filepath)} - Already has AdSense")
            return False
        
        # Add AdSense header script after Font Awesome link
        if 'font-awesome' in content and '<link rel="stylesheet"' in content:
            # Find the Font Awesome link and add AdSense after it
            content = re.sub(
                r'(<link rel="stylesheet".*?font-awesome.*?>\s*)',
                r'\1' + ADSENSE_HEADER,
                content,
                count=1
            )
        else:
            # If no Font Awesome, add after viewport meta tag
            content = re.sub(
                r'(<meta name="viewport".*?>\s*)',
                r'\1' + ADSENSE_HEADER,
                content,
                count=1
            )
        
        # Add ad unit before closing body tag
        if '</body>' in content:
            # Add ad before </body>
            content = content.replace('</body>', ADSENSE_AD_DISPLAY + '\n</body>')
        
        # Write back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {os.path.basename(filepath)} - AdSense added successfully")
        return True
        
    except Exception as e:
        print(f"❌ {os.path.basename(filepath)} - Error: {str(e)}")
        return False

def main():
    """Main function to process all files."""
    frontend_dir = '/Users/perera/Downloads/Sigiri/frontend'
    
    # Read list of files that need AdSense
    files_list = '/tmp/files_need_adsense.txt'
    
    if not os.path.exists(files_list):
        print("❌ File list not found. Please run the grep command first.")
        return
    
    with open(files_list, 'r') as f:
        files = [line.strip() for line in f if line.strip()]
    
    print(f"📋 Found {len(files)} files that need AdSense code\n")
    print("=" * 60)
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for filename in files:
        filepath = os.path.join(frontend_dir, filename)
        if os.path.exists(filepath):
            result = add_adsense_to_file(filepath)
            if result:
                success_count += 1
            elif result is False and 'Already has AdSense' in str(result):
                skip_count += 1
            else:
                error_count += 1
        else:
            print(f"⚠️  {filename} - File not found")
            error_count += 1
    
    print("\n" + "=" * 60)
    print(f"\n📊 Summary:")
    print(f"   ✅ Successfully added: {success_count}")
    print(f"   ⏭️  Skipped (already has): {skip_count}")
    print(f"   ❌ Errors: {error_count}")
    print(f"\n✨ Done! AdSense code has been added to all converter pages.")

if __name__ == '__main__':
    main()
