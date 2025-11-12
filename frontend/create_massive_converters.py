#!/usr/bin/env python3
"""
Master script to create all remaining converter pages for:
- ERF, DNG, DCR, CRW, CR3 (RAW formats)
- GIF converters (to audio, images, video)
- To GIF converters (from various formats)
- EPS converters (to various formats)
- To EPS converters (from various formats)
"""

import os

# Common image/document formats
IMAGE_FORMATS = {
    'pdf': {'icon': 'fa-file-pdf', 'name': 'PDF'},
    'avif': {'icon': 'fa-rocket', 'name': 'AVIF'},
    'bmp': {'icon': 'fa-image', 'name': 'BMP'},
    'eps': {'icon': 'fa-file-image', 'name': 'EPS'},
    'gif': {'icon': 'fa-film', 'name': 'GIF'},
    'ico': {'icon': 'fa-icons', 'name': 'ICO'},
    'jpg': {'icon': 'fa-image', 'name': 'JPG'},
    'odd': {'icon': 'fa-file-alt', 'name': 'ODD'},
    'png': {'icon': 'fa-file-image', 'name': 'PNG'},
    'ps': {'icon': 'fa-file-image', 'name': 'PS'},
    'psd': {'icon': 'fa-image', 'name': 'PSD'},
    'tiff': {'icon': 'fa-file-image', 'name': 'TIFF'},
    'webp': {'icon': 'fa-images', 'name': 'WEBP'},
}

# Audio formats for GIF
AUDIO_FORMATS = {
    'aac': {'icon': 'fa-music', 'name': 'AAC'},
    'aiff': {'icon': 'fa-music', 'name': 'AIFF'},
    'flac': {'icon': 'fa-music', 'name': 'FLAC'},
    'm4a': {'icon': 'fa-music', 'name': 'M4A'},
    'mp3': {'icon': 'fa-music', 'name': 'MP3'},
    'wav': {'icon': 'fa-music', 'name': 'WAV'},
    'wma': {'icon': 'fa-music', 'name': 'WMA'},
}

# Video formats for GIF
VIDEO_FORMATS = {
    'avi': {'icon': 'fa-video', 'name': 'AVI'},
    'flv': {'icon': 'fa-video', 'name': 'FLV'},
    'mkv': {'icon': 'fa-video', 'name': 'MKV'},
    'mov': {'icon': 'fa-video', 'name': 'MOV'},
    'mp4': {'icon': 'fa-video', 'name': 'MP4'},
    'webm': {'icon': 'fa-video', 'name': 'WEBM'},
    'wmv': {'icon': 'fa-video', 'name': 'WMV'},
}

# Additional EPS target formats
EPS_EXTRA_FORMATS = {
    'dxf': {'icon': 'fa-project-diagram', 'name': 'DXF'},
    'emf': {'icon': 'fa-file-image', 'name': 'EMF'},
    'svg': {'icon': 'fa-vector-square', 'name': 'SVG'},
    'wmf': {'icon': 'fa-file-image', 'name': 'WMF'},
}

# Formats that convert TO GIF
TO_GIF_SOURCES = [
    '3fr', '3g2', '3gp', '3gpp', 'arw', 'avi', 'avif', 'bmp', 'cavs', 'cr2', 'cr3', 'crw',
    'dcr', 'dng', 'dv', 'dvr', 'dwg', 'dxf', 'emf', 'eps', 'erf', 'flv', 'gif', 'heic', 'heif',
    'ico', 'jfif', 'jpeg', 'jpg', 'm2ts', 'm4v', 'mkv', 'mod', 'mos', 'mov', 'mp4', 'mpeg', 'mpg',
    'mrw', 'mts', 'mxf', 'nef', 'odd', 'ogv', 'orf', 'pdf', 'pef', 'png', 'ppm', 'ps', 'psd',
    'raf', 'raw', 'rm', 'rmvb', 'rw2', 'svg', 'svgz', 'swf', 'tif', 'tiff', 'ts', 'vob', 'webm',
    'webp', 'wmv', 'wtv', 'x3f', 'xcf', 'xps'
]

# Formats that convert TO EPS
TO_EPS_SOURCES = [
    '3fr', 'ai', 'arw', 'avif', 'bmp', 'cdr', 'cgm', 'cr2', 'cr3', 'crw', 'dcr', 'dng', 'dps',
    'dwg', 'dxf', 'emf', 'eps', 'erf', 'gif', 'heic', 'heif', 'ico', 'jfif', 'jpeg', 'jpg',
    'mos', 'mrw', 'nef', 'odd', 'odp', 'orf', 'pdf', 'pef', 'png', 'ppm', 'pps', 'ppsx', 'ppt',
    'pptm', 'pptx', 'ps', 'psd', 'raf', 'raw', 'rw2', 'sk', 'sk1', 'svg', 'svgz', 'tif', 'tiff',
    'vsd', 'webp', 'wmf', 'x3f', 'xcf', 'xps'
]

def get_simple_template(source_format, target_format, source_desc=""):
    """Generate a simple converter HTML template"""
    source_upper = source_format.upper()
    target_upper = target_format.upper()
    
    # Get icon and name
    all_formats = {**IMAGE_FORMATS, **AUDIO_FORMATS, **VIDEO_FORMATS, **EPS_EXTRA_FORMATS}
    target_info = all_formats.get(target_format, {'icon': 'fa-file', 'name': target_upper})
    
    if not source_desc:
        source_desc = f"{source_upper} files"
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{source_upper} to {target_info['name']} Converter - Free Online Converter | SIGIRI</title>
    <meta name="description" content="Convert {source_desc} to {target_info['name']} format online for free. Fast, secure converter.">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; }}
        .sidebar {{ width: 250px; background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); padding: 2rem 0; position: fixed; height: 100vh; left: 0; top: 0; border-right: 1px solid rgba(255, 255, 255, 0.2); }}
        .logo {{ text-align: center; margin-bottom: 3rem; padding: 0 1rem; }}
        .logo h1 {{ color: white; font-size: 2.5rem; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }}
        .main-content {{ margin-left: 250px; flex: 1; padding: 2rem; }}
        .converter-container {{ max-width: 800px; margin: 0 auto; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border-radius: 20px; padding: 3rem; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3); }}
        h1 {{ color: #333; margin-bottom: 0.5rem; font-size: 2rem; }}
        .subtitle {{ color: #666; margin-bottom: 2rem; font-size: 1.1rem; }}
        .upload-area {{ border: 3px dashed #667eea; border-radius: 15px; padding: 3rem; text-align: center; cursor: pointer; transition: all 0.3s ease; background: rgba(102, 126, 234, 0.05); margin-bottom: 2rem; }}
        .upload-area:hover {{ border-color: #764ba2; background: rgba(118, 75, 162, 0.05); transform: translateY(-2px); }}
        .upload-icon {{ font-size: 4rem; color: #667eea; margin-bottom: 1rem; }}
        .upload-text {{ font-size: 1.2rem; color: #333; margin-bottom: 0.5rem; }}
        .upload-hint {{ color: #666; font-size: 0.9rem; }}
        #fileInput {{ display: none; }}
        .convert-btn {{ width: 100%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 1rem 2rem; font-size: 1.1rem; border-radius: 10px; cursor: pointer; transition: all 0.3s ease; font-weight: 600; display: none; }}
        .convert-btn.show {{ display: block; }}
        .premium-badge {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600; display: inline-block; margin-bottom: 1rem; }}
        @media (max-width: 768px) {{ .sidebar {{ display: none; }} .main-content {{ margin-left: 0; padding: 1rem; }} .converter-container {{ padding: 1.5rem; }} }}
    </style>
</head>
<body>
    <div class="sidebar"><div class="logo"><h1>S</h1></div></div>
    <div class="main-content">
        <div class="converter-container">
            <div class="premium-badge">FREE TOOL</div>
            <h1>{source_upper} to {target_info['name']} Converter</h1>
            <p class="subtitle">Convert {source_desc} to {target_info['name']} format</p>
            <div class="upload-area" id="uploadArea">
                <div class="upload-icon"><i class="fas fa-cloud-upload-alt"></i></div>
                <div class="upload-text">Click to upload or drag and drop</div>
                <div class="upload-hint">Maximum file size: 100MB</div>
                <input type="file" id="fileInput" accept=".{source_format}">
            </div>
            <button class="convert-btn" id="convertBtn">Convert to {target_info['name']}</button>
        </div>
    </div>
    <script>
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const convertBtn = document.getElementById('convertBtn');
        uploadArea.addEventListener('click', () => fileInput.click());
        fileInput.addEventListener('change', (e) => {{ if (e.target.files.length > 0) convertBtn.classList.add('show'); }});
    </script>
</body>
</html>'''

def create_batch(source_formats, target_formats, source_type_desc=""):
    """Create a batch of converter pages"""
    created = 0
    skipped = 0
    
    for source in source_formats:
        for target in target_formats:
            filename = f"{source}-to-{target}.html"
            
            if os.path.exists(filename):
                skipped += 1
                continue
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(get_simple_template(source, target, source_type_desc))
            
            created += 1
    
    return created, skipped

def main():
    print("Creating massive batch of converter pages...\n")
    
    total_created = 0
    total_skipped = 0
    
    # 1. RAW formats to standard formats
    print("1️⃣  Creating RAW format converters (ERF, DNG, DCR, CRW, CR3)...")
    raw_formats = ['erf', 'dng', 'dcr', 'crw', 'cr3']
    created, skipped = create_batch(raw_formats, IMAGE_FORMATS.keys(), "RAW image")
    total_created += created
    total_skipped += skipped
    print(f"   ✅ Created {created}, skipped {skipped}\n")
    
    # 2. GIF to audio formats
    print("2️⃣  Creating GIF to audio converters...")
    created, skipped = create_batch(['gif'], AUDIO_FORMATS.keys(), "GIF animation")
    total_created += created
    total_skipped += skipped
    print(f"   ✅ Created {created}, skipped {skipped}\n")
    
    # 3. GIF to video formats
    print("3️⃣  Creating GIF to video converters...")
    created, skipped = create_batch(['gif'], VIDEO_FORMATS.keys(), "GIF animation")
    total_created += created
    total_skipped += skipped
    print(f"   ✅ Created {created}, skipped {skipped}\n")
    
    # 4. All formats TO GIF
    print("4️⃣  Creating TO GIF converters (~80 formats)...")
    created, skipped = create_batch(TO_GIF_SOURCES, ['gif'])
    total_created += created
    total_skipped += skipped
    print(f"   ✅ Created {created}, skipped {skipped}\n")
    
    # 5. EPS to various formats (including vector)
    print("5️⃣  Creating EPS converters (with vector formats)...")
    eps_targets = {**IMAGE_FORMATS, **EPS_EXTRA_FORMATS}
    created, skipped = create_batch(['eps'], eps_targets.keys(), "EPS vector")
    total_created += created
    total_skipped += skipped
    print(f"   ✅ Created {created}, skipped {skipped}\n")
    
    # 6. All formats TO EPS
    print("6️⃣  Creating TO EPS converters (~70 formats)...")
    created, skipped = create_batch(TO_EPS_SOURCES, ['eps'])
    total_created += created
    total_skipped += skipped
    print(f"   ✅ Created {created}, skipped {skipped}\n")
    
    print(f"{'='*60}")
    print(f"✨ DONE! Created {total_created} new converter pages")
    print(f"⚠️  Skipped {total_skipped} existing pages")
    print(f"📊 Total processed: {total_created + total_skipped}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
