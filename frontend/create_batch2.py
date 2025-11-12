import os

# Base HTML template
def create_converter_html(config):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{config["title"]} - SIGIRI</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX" crossorigin="anonymous"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif; background: linear-gradient(135deg, {config["bg_gradient"]}); backdrop-filter: blur(100px); min-height: 100vh; display: flex; position: relative; overflow-x: hidden; }}
        body::before {{ content: ''; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: {config["bg_radial"]}; z-index: 0; pointer-events: none; }}
        @keyframes float {{ 0%, 100% {{ transform: translate(0, 0) scale(1); }} 33% {{ transform: translate(30px, -50px) scale(1.1); }} 66% {{ transform: translate(-20px, 20px) scale(0.9); }} }}
        @keyframes pulse {{ 0%, 100% {{ opacity: 0.3; }} 50% {{ opacity: 0.6; }} }}
        .floating-shape {{ position: fixed; border-radius: 50%; filter: blur(100px); opacity: 0.3; z-index: 0; animation: float 25s ease-in-out infinite, pulse 10s ease-in-out infinite; pointer-events: none; }}
        .shape1 {{ width: 500px; height: 500px; background: {config["shape1_bg"]}; top: 50%; right: 10%; animation-delay: 3s; }}
        .shape2 {{ width: 450px; height: 450px; background: {config["shape2_bg"]}; bottom: 20%; left: 15%; animation-delay: 10s; }}
        .left-sidebar {{ width: 70px; background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(30px); border-right: 1px solid rgba(255, 255, 255, 0.5); display: flex; flex-direction: column; align-items: center; padding: 20px 0; position: fixed; height: 100vh; z-index: 1000; box-shadow: 4px 0 20px rgba(0, 0, 0, 0.05); }}
        .sidebar-logo {{ font-size: 1.5rem; font-weight: 800; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 40px; }}
        .sidebar-item {{ width: 50px; height: 50px; border-radius: 10px; display: flex; flex-direction: column; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s; text-decoration: none; color: #666; font-size: 0.7rem; gap: 2px; margin-bottom: 10px; }}
        .sidebar-item i {{ font-size: 1.3rem; }}
        .sidebar-item:hover {{ background: rgba(245, 245, 255, 0.6); }}
        .main-container {{ margin-left: 70px; flex: 1; display: flex; justify-content: center; padding: 30px 20px; position: relative; z-index: 1; }}
        .content {{ width: 100%; max-width: 900px; }}
        .converter-header {{ text-align: center; margin-bottom: 40px; }}
        .converter-header h1 {{ font-size: 2.5rem; margin-bottom: 12px; background: {config["header_gradient"]}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
        .converter-header p {{ color: #666; font-size: 1.1rem; }}
        .upload-area {{ background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(25px); border: 3px dashed {config["border_color"]}; border-radius: 16px; padding: 60px 40px; text-align: center; cursor: pointer; transition: all 0.3s; margin-bottom: 30px; }}
        .upload-area:hover {{ border-color: {config["hover_border"]}; transform: translateY(-5px); box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1); }}
        .upload-area i {{ font-size: 4rem; color: {config["icon_color"]}; margin-bottom: 20px; }}
        .upload-area h3 {{ font-size: 1.5rem; color: #333; margin-bottom: 10px; }}
        .upload-area p {{ color: #666; font-size: 1rem; }}
        .file-input {{ display: none; }}
        .convert-btn {{ background: {config["button_gradient"]}; color: white; border: none; padding: 16px 48px; border-radius: 12px; font-size: 1.1rem; font-weight: 600; cursor: pointer; width: 100%; transition: all 0.3s; box-shadow: 0 8px 25px {config["button_shadow"]}; }}
        .convert-btn:hover {{ transform: translateY(-2px); box-shadow: 0 12px 35px {config["button_shadow"]}; }}
        .convert-btn:disabled {{ opacity: 0.5; cursor: not-allowed; }}
        .features {{ margin-top: 60px; display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 24px; }}
        .feature-card {{ background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(25px); padding: 30px; border-radius: 12px; text-align: center; border: 1px solid rgba(255, 255, 255, 0.5); }}
        .feature-card i {{ font-size: 2.5rem; color: {config["icon_color"]}; margin-bottom: 16px; }}
        .feature-card h4 {{ font-size: 1.1rem; color: #333; margin-bottom: 8px; }}
        .feature-card p {{ color: #666; font-size: 0.9rem; }}
        .ad-container {{ background: rgba(248, 249, 250, 0.5); backdrop-filter: blur(10px); border: 1px dashed rgba(102, 126, 234, 0.2); border-radius: 12px; padding: 15px; margin: 25px 0; text-align: center; min-height: 100px; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
        .ad-label {{ font-size: 0.75rem; color: #999; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }}
        .ad-header {{ margin-bottom: 25px; }}
        .ad-header .ad-container {{ max-width: 970px; margin: 0 auto 25px; }}
        .ad-in-content {{ margin: 35px 0; }}
        .ad-footer {{ margin-top: 35px; }}
        body.premium-user .ad-container {{ display: none; }}
    </style>
</head>
<body>
    <div class="floating-shape shape1"></div>
    <div class="floating-shape shape2"></div>
    <div class="left-sidebar">
        <div class="sidebar-logo">S</div>
        <a href="dashboard.html" class="sidebar-item"><i class="fas fa-home"></i><span>Home</span></a>
        <a href="converters.html" class="sidebar-item"><i class="fas fa-exchange-alt"></i><span>Converts</span></a>
    </div>
    <div class="main-container">
        <div class="content">
            <div class="ad-header"><div class="ad-container"><div class="ad-label">Advertisement</div><ins class="adsbygoogle" style="display:inline-block;width:728px;height:90px" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="1234567890"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script></div></div>
            <div class="converter-header"><h1>{config["heading"]}</h1><p>{config["description"]}</p></div>
            <div class="upload-area" onclick="document.getElementById('fileInput').click()"><i class="{config["icon"]}"></i><h3>Drop your {config["from_format"]} files here</h3><p>or click to browse</p><input type="file" id="fileInput" class="file-input" accept="{config["accept"]}" multiple></div>
            <button class="convert-btn" disabled><i class="fas fa-sync-alt"></i> Convert to {config["to_format"]}</button>
            <div class="ad-in-content"><div class="ad-container"><div class="ad-label">Advertisement</div><ins class="adsbygoogle" style="display:inline-block;width:336px;height:280px" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="0987654321"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script></div></div>
            <div class="features">
                <div class="feature-card"><i class="fas fa-bolt"></i><h4>Fast Conversion</h4><p>Lightning-fast {config["from_format"]} to {config["to_format"]} conversion</p></div>
                <div class="feature-card"><i class="fas fa-shield-alt"></i><h4>100% Secure</h4><p>Your files are processed securely and deleted after conversion</p></div>
                <div class="feature-card"><i class="fas fa-star"></i><h4>High Quality</h4><p>Maintain maximum quality during conversion</p></div>
            </div>
            <div class="ad-footer"><div class="ad-container"><div class="ad-label">Advertisement</div><ins class="adsbygoogle" style="display:inline-block;width:728px;height:90px" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="1122334455"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script></div></div>
        </div>
    </div>
    <script>
        function checkPremiumStatus() {{ const isPremium = localStorage.getItem('isPremiumUser') === 'true'; if (isPremium) {{ document.body.classList.add('premium-user'); }} }}
        checkPremiumStatus();
        const fileInput = document.getElementById('fileInput'); const convertBtn = document.querySelector('.convert-btn'); const uploadArea = document.querySelector('.upload-area');
        fileInput.addEventListener('change', function() {{ if (this.files.length > 0) {{ convertBtn.disabled = false; uploadArea.querySelector('h3').textContent = `${{this.files.length}} file(s) selected`; }} }});
        convertBtn.addEventListener('click', function() {{ if (fileInput.files.length > 0) {{ alert('Conversion functionality will be implemented with backend integration'); }} }});
    </script>
</body>
</html>'''

# Batch 2: 10 more converters
converters = [
    {
        "filename": "bmp-to-png.html",
        "title": "BMP to PNG Converter",
        "heading": "BMP to PNG Converter",
        "description": "Convert Windows BMP images to PNG format",
        "from_format": "BMP",
        "to_format": "PNG",
        "accept": ".bmp",
        "icon": "fas fa-image",
        "bg_gradient": "rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%",
        "bg_radial": "radial-gradient(circle at 20% 30%, rgba(102, 126, 234, 0.15) 0%, transparent 50%)",
        "shape1_bg": "linear-gradient(135deg, rgba(102, 126, 234, 0.25) 0%, rgba(118, 75, 162, 0.25) 100%)",
        "shape2_bg": "linear-gradient(135deg, rgba(67, 233, 123, 0.25) 0%, rgba(56, 249, 215, 0.25) 100%)",
        "header_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "border_color": "rgba(102, 126, 234, 0.3)",
        "hover_border": "#667eea",
        "icon_color": "#667eea",
        "button_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "button_shadow": "rgba(102, 126, 234, 0.3)"
    },
    {
        "filename": "ico-to-png.html",
        "title": "ICO to PNG Converter",
        "heading": "ICO to PNG Converter",
        "description": "Convert Windows icon files to PNG format",
        "from_format": "ICO",
        "to_format": "PNG",
        "accept": ".ico",
        "icon": "fas fa-icons",
        "bg_gradient": "rgba(240, 147, 251, 0.1) 0%, rgba(245, 87, 108, 0.1) 100%",
        "bg_radial": "radial-gradient(circle at 20% 30%, rgba(240, 147, 251, 0.15) 0%, transparent 50%)",
        "shape1_bg": "linear-gradient(135deg, rgba(240, 147, 251, 0.25) 0%, rgba(245, 87, 108, 0.25) 100%)",
        "shape2_bg": "linear-gradient(135deg, rgba(250, 112, 154, 0.25) 0%, rgba(254, 225, 64, 0.25) 100%)",
        "header_gradient": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
        "border_color": "rgba(240, 147, 251, 0.3)",
        "hover_border": "#f093fb",
        "icon_color": "#f093fb",
        "button_gradient": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
        "button_shadow": "rgba(240, 147, 251, 0.3)"
    },
    {
        "filename": "svg-to-png.html",
        "title": "SVG to PNG Converter",
        "heading": "SVG to PNG Converter",
        "description": "Convert vector SVG graphics to PNG images",
        "from_format": "SVG",
        "to_format": "PNG",
        "accept": ".svg",
        "icon": "fas fa-vector-square",
        "bg_gradient": "rgba(79, 172, 254, 0.1) 0%, rgba(0, 242, 254, 0.1) 100%",
        "bg_radial": "radial-gradient(circle at 20% 30%, rgba(79, 172, 254, 0.15) 0%, transparent 50%)",
        "shape1_bg": "linear-gradient(135deg, rgba(79, 172, 254, 0.25) 0%, rgba(0, 242, 254, 0.25) 100%)",
        "shape2_bg": "linear-gradient(135deg, rgba(67, 233, 123, 0.25) 0%, rgba(56, 249, 215, 0.25) 100%)",
        "header_gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
        "border_color": "rgba(79, 172, 254, 0.3)",
        "hover_border": "#4facfe",
        "icon_color": "#4facfe",
        "button_gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
        "button_shadow": "rgba(79, 172, 254, 0.3)"
    },
    {
        "filename": "png-to-webp.html",
        "title": "PNG to WEBP Converter",
        "heading": "PNG to WEBP Converter",
        "description": "Convert PNG images to modern WEBP format",
        "from_format": "PNG",
        "to_format": "WEBP",
        "accept": ".png",
        "icon": "fas fa-images",
        "bg_gradient": "rgba(67, 233, 123, 0.1) 0%, rgba(56, 249, 215, 0.1) 100%",
        "bg_radial": "radial-gradient(circle at 20% 30%, rgba(67, 233, 123, 0.15) 0%, transparent 50%)",
        "shape1_bg": "linear-gradient(135deg, rgba(67, 233, 123, 0.25) 0%, rgba(56, 249, 215, 0.25) 100%)",
        "shape2_bg": "linear-gradient(135deg, rgba(79, 172, 254, 0.25) 0%, rgba(0, 242, 254, 0.25) 100%)",
        "header_gradient": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
        "border_color": "rgba(67, 233, 123, 0.3)",
        "hover_border": "#43e97b",
        "icon_color": "#43e97b",
        "button_gradient": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
        "button_shadow": "rgba(67, 233, 123, 0.3)"
    },
    {
        "filename": "jpg-to-webp.html",
        "title": "JPG to WEBP Converter",
        "heading": "JPG to WEBP Converter",
        "description": "Convert JPG images to modern WEBP format",
        "from_format": "JPG",
        "to_format": "WEBP",
        "accept": ".jpg,.jpeg",
        "icon": "fas fa-images",
        "bg_gradient": "rgba(250, 112, 154, 0.1) 0%, rgba(254, 225, 64, 0.1) 100%",
        "bg_radial": "radial-gradient(circle at 20% 30%, rgba(250, 112, 154, 0.15) 0%, transparent 50%)",
        "shape1_bg": "linear-gradient(135deg, rgba(250, 112, 154, 0.25) 0%, rgba(254, 225, 64, 0.25) 100%)",
        "shape2_bg": "linear-gradient(135deg, rgba(240, 147, 251, 0.25) 0%, rgba(245, 87, 108, 0.25) 100%)",
        "header_gradient": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
        "border_color": "rgba(250, 112, 154, 0.3)",
        "hover_border": "#fa709a",
        "icon_color": "#fa709a",
        "button_gradient": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
        "button_shadow": "rgba(250, 112, 154, 0.3)"
    },
    {
        "filename": "png-to-svg.html",
        "title": "PNG to SVG Converter",
        "heading": "PNG to SVG Converter",
        "description": "Convert PNG raster images to scalable SVG vectors",
        "from_format": "PNG",
        "to_format": "SVG",
        "accept": ".png",
        "icon": "fas fa-file-image",
        "bg_gradient": "rgba(48, 207, 208, 0.1) 0%, rgba(51, 8, 103, 0.1) 100%",
        "bg_radial": "radial-gradient(circle at 20% 30%, rgba(48, 207, 208, 0.15) 0%, transparent 50%)",
        "shape1_bg": "linear-gradient(135deg, rgba(48, 207, 208, 0.25) 0%, rgba(51, 8, 103, 0.25) 100%)",
        "shape2_bg": "linear-gradient(135deg, rgba(102, 126, 234, 0.25) 0%, rgba(118, 75, 162, 0.25) 100%)",
        "header_gradient": "linear-gradient(135deg, #30cfd0 0%, #330867 100%)",
        "border_color": "rgba(48, 207, 208, 0.3)",
        "hover_border": "#30cfd0",
        "icon_color": "#30cfd0",
        "button_gradient": "linear-gradient(135deg, #30cfd0 0%, #330867 100%)",
        "button_shadow": "rgba(48, 207, 208, 0.3)"
    },
    {
        "filename": "heic-to-jpg.html",
        "title": "HEIC to JPG Converter",
        "heading": "HEIC to JPG Converter",
        "description": "Convert iPhone/Apple HEIC photos to JPG format",
        "from_format": "HEIC",
        "to_format": "JPG",
        "accept": ".heic,.heif",
        "icon": "fas fa-mobile-alt",
        "bg_gradient": "rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%",
        "bg_radial": "radial-gradient(circle at 20% 30%, rgba(102, 126, 234, 0.15) 0%, transparent 50%)",
        "shape1_bg": "linear-gradient(135deg, rgba(102, 126, 234, 0.25) 0%, rgba(118, 75, 162, 0.25) 100%)",
        "shape2_bg": "linear-gradient(135deg, rgba(67, 233, 123, 0.25) 0%, rgba(56, 249, 215, 0.25) 100%)",
        "header_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "border_color": "rgba(102, 126, 234, 0.3)",
        "hover_border": "#667eea",
        "icon_color": "#667eea",
        "button_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "button_shadow": "rgba(102, 126, 234, 0.3)"
    },
    {
        "filename": "tiff-to-jpg.html",
        "title": "TIFF to JPG Converter",
        "heading": "TIFF to JPG Converter",
        "description": "Convert TIFF images to standard JPG format",
        "from_format": "TIFF",
        "to_format": "JPG",
        "accept": ".tif,.tiff",
        "icon": "fas fa-file-image",
        "bg_gradient": "rgba(240, 147, 251, 0.1) 0%, rgba(245, 87, 108, 0.1) 100%",
        "bg_radial": "radial-gradient(circle at 20% 30%, rgba(240, 147, 251, 0.15) 0%, transparent 50%)",
        "shape1_bg": "linear-gradient(135deg, rgba(240, 147, 251, 0.25) 0%, rgba(245, 87, 108, 0.25) 100%)",
        "shape2_bg": "linear-gradient(135deg, rgba(250, 112, 154, 0.25) 0%, rgba(254, 225, 64, 0.25) 100%)",
        "header_gradient": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
        "border_color": "rgba(240, 147, 251, 0.3)",
        "hover_border": "#f093fb",
        "icon_color": "#f093fb",
        "button_gradient": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
        "button_shadow": "rgba(240, 147, 251, 0.3)"
    },
    {
        "filename": "psd-to-png.html",
        "title": "PSD to PNG Converter",
        "heading": "PSD to PNG Converter",
        "description": "Convert Photoshop PSD files to PNG format",
        "from_format": "PSD",
        "to_format": "PNG",
        "accept": ".psd",
        "icon": "fas fa-image",
        "bg_gradient": "rgba(79, 172, 254, 0.1) 0%, rgba(0, 242, 254, 0.1) 100%",
        "bg_radial": "radial-gradient(circle at 20% 30%, rgba(79, 172, 254, 0.15) 0%, transparent 50%)",
        "shape1_bg": "linear-gradient(135deg, rgba(79, 172, 254, 0.25) 0%, rgba(0, 242, 254, 0.25) 100%)",
        "shape2_bg": "linear-gradient(135deg, rgba(67, 233, 123, 0.25) 0%, rgba(56, 249, 215, 0.25) 100%)",
        "header_gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
        "border_color": "rgba(79, 172, 254, 0.3)",
        "hover_border": "#4facfe",
        "icon_color": "#4facfe",
        "button_gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
        "button_shadow": "rgba(79, 172, 254, 0.3)"
    },
    {
        "filename": "gif-to-mp4.html",
        "title": "GIF to MP4 Converter",
        "heading": "GIF to MP4 Converter",
        "description": "Convert animated GIF to MP4 video format",
        "from_format": "GIF",
        "to_format": "MP4",
        "accept": ".gif",
        "icon": "fas fa-film",
        "bg_gradient": "rgba(67, 233, 123, 0.1) 0%, rgba(56, 249, 215, 0.1) 100%",
        "bg_radial": "radial-gradient(circle at 20% 30%, rgba(67, 233, 123, 0.15) 0%, transparent 50%)",
        "shape1_bg": "linear-gradient(135deg, rgba(67, 233, 123, 0.25) 0%, rgba(56, 249, 215, 0.25) 100%)",
        "shape2_bg": "linear-gradient(135deg, rgba(79, 172, 254, 0.25) 0%, rgba(0, 242, 254, 0.25) 100%)",
        "header_gradient": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
        "border_color": "rgba(67, 233, 123, 0.3)",
        "hover_border": "#43e97b",
        "icon_color": "#43e97b",
        "button_gradient": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
        "button_shadow": "rgba(67, 233, 123, 0.3)"
    }
]

# Create files
created = []
for config in converters:
    filename = config['filename']
    html_content = create_converter_html(config)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    created.append(filename)
    print(f"✅ Created {filename}")

print(f"\n🎉 Successfully created {len(created)} more converter pages!")
print(f"Total new pages in this batch: {len(created)}")
