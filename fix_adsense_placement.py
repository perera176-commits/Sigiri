#!/usr/bin/env python3
"""
Script to fix AdSense ad placement in simple converter pages.
Moves the ad from after closing divs to inside the converter-container.
"""

import os
import re

def fix_adsense_placement(filepath):
    """Fix AdSense placement in a simple converter file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if it's a simple converter page (short file < 100 lines) with misplaced ad
        line_count = content.count('\n')
        if line_count > 100:
            return False  # Skip complex pages
        
        # Check if ad is misplaced (after </div></div> and before </body>)
        if '</div>\n    </div>\n    <script>' in content and '<!-- AdSense Display Ad -->' in content:
            # Pattern: ad is placed after closing script tag but before </body>
            pattern = r'(    </script>\n\n)(                    <!-- AdSense Display Ad -->.*?</script>\n\n)(</body>)'
            
            if re.search(pattern, content, re.DOTALL):
                # Move the ad inside the converter-container
                # Find the convert button and place ad after it
                new_ad_html = '''
            
            <!-- AdSense Display Ad -->
            <div style="margin-top: 2rem; padding: 1rem; background: rgba(255,255,255,0.5); border-radius: 10px; text-align: center;">
                <div style="color: #999; font-size: 0.75rem; margin-bottom: 0.5rem;">Advertisement</div>
                <ins class="adsbygoogle"
                     style="display:block"
                     data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
                     data-ad-slot="XXXXXXXXXX"
                     data-ad-format="auto"
                     data-full-width-responsive="true"></ins>
                <script>
                     (adsbygoogle = window.adsbygoogle || []).push({});
                </script>
            </div>'''
                
                # Replace pattern: add ad after convert button, before closing </div></div>
                content = re.sub(
                    r'(            <button class="convert-btn".*?</button>\n)(        </div>\n    </div>)',
                    r'\1' + new_ad_html + r'\n\2',
                    content,
                    count=1
                )
                
                # Remove the old ad placement
                content = re.sub(
                    r'\n\n                    <!-- AdSense Display Ad -->.*?</script>\n',
                    r'\n',
                    content,
                    flags=re.DOTALL,
                    count=1
                )
                
                # Write back
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"✅ {os.path.basename(filepath)} - Fixed AdSense placement")
                return True
        
        return False
        
    except Exception as e:
        print(f"❌ {os.path.basename(filepath)} - Error: {str(e)}")
        return False

def main():
    """Main function."""
    frontend_dir = '/Users/perera/Downloads/Sigiri/frontend'
    
    # Get all converter files
    import glob
    converter_files = glob.glob(os.path.join(frontend_dir, '*-to-*.html'))
    
    print(f"📋 Found {len(converter_files)} converter files\n")
    print("=" * 60)
    
    fixed_count = 0
    skipped_count = 0
    
    for filepath in converter_files:
        result = fix_adsense_placement(filepath)
        if result:
            fixed_count += 1
        else:
            skipped_count += 1
    
    print("\n" + "=" * 60)
    print(f"\n📊 Summary:")
    print(f"   ✅ Fixed: {fixed_count}")
    print(f"   ⏭️  Skipped: {skipped_count}")
    print(f"\n✨ Done! AdSense placement has been fixed.")

if __name__ == '__main__':
    main()
