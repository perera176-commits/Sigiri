import os

def create_hub_page(config):
    conversions_html = ""
    for conv in config["conversions"]:
        conversions_html += f'''
                    <a href="{conv['link']}" class="conversion-option">
                        <div class="conversion-icon">
                            <i class="{conv['icon']}"></i>
                        </div>
                        <div class="conversion-info">
                            <h3>{conv['title']}</h3>
                            <p>{conv['description']}</p>
                        </div>
                        <i class="fas fa-arrow-right conversion-arrow"></i>
                    </a>'''
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{config["title"]} - Convert {config["format_name"]} Files - SIGIRI</title>
    <meta name="description" content="{config["meta_description"]}">
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
        
        /* Sidebar */
        .left-sidebar {{ width: 70px; background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(30px); border-right: 1px solid rgba(255, 255, 255, 0.5); display: flex; flex-direction: column; align-items: center; padding: 20px 0; position: fixed; height: 100vh; z-index: 1000; box-shadow: 4px 0 20px rgba(0, 0, 0, 0.05); }}
        .sidebar-logo {{ font-size: 1.5rem; font-weight: 800; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 40px; }}
        .sidebar-item {{ width: 50px; height: 50px; border-radius: 10px; display: flex; flex-direction: column; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s; text-decoration: none; color: #666; font-size: 0.7rem; gap: 2px; margin-bottom: 10px; }}
        .sidebar-item i {{ font-size: 1.3rem; }}
        .sidebar-item:hover {{ background: rgba(245, 245, 255, 0.6); }}
        
        /* Main Container */
        .main-container {{ margin-left: 70px; flex: 1; display: flex; justify-content: center; padding: 30px 20px; position: relative; z-index: 1; }}
        .content {{ width: 100%; max-width: 1200px; }}
        
        /* Breadcrumb */
        .breadcrumb {{ display: flex; align-items: center; gap: 8px; margin-bottom: 25px; font-size: 0.9rem; color: #666; flex-wrap: wrap; }}
        .breadcrumb a {{ color: #667eea; text-decoration: none; transition: color 0.2s; }}
        .breadcrumb a:hover {{ color: #764ba2; text-decoration: underline; }}
        .breadcrumb i {{ font-size: 0.7rem; color: #999; }}
        
        /* Header */
        .hub-header {{ text-align: center; margin-bottom: 40px; }}
        .format-badge {{ display: inline-block; background: {config["badge_gradient"]}; color: white; padding: 8px 20px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; margin-bottom: 15px; box-shadow: 0 4px 15px {config["badge_shadow"]}; }}
        .hub-header h1 {{ font-size: 2.8rem; margin-bottom: 15px; background: {config["header_gradient"]}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
        .hub-header p {{ color: #666; font-size: 1.15rem; line-height: 1.6; max-width: 800px; margin: 0 auto; }}
        
        /* Format Info */
        .format-info {{ background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(25px); border-radius: 16px; padding: 30px; margin-bottom: 40px; border: 1px solid rgba(255, 255, 255, 0.5); }}
        .format-info h2 {{ font-size: 1.4rem; color: #333; margin-bottom: 12px; }}
        .format-info p {{ color: #666; line-height: 1.7; font-size: 1rem; }}
        
        /* Ad Container */
        .ad-container {{ background: rgba(248, 249, 250, 0.5); backdrop-filter: blur(10px); border: 1px dashed rgba(102, 126, 234, 0.2); border-radius: 12px; padding: 15px; margin: 30px 0; text-align: center; min-height: 100px; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
        .ad-label {{ font-size: 0.75rem; color: #999; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }}
        body.premium-user .ad-container {{ display: none; }}
        
        /* Conversions Section */
        .conversions-section {{ margin-top: 40px; }}
        .conversions-section h2 {{ font-size: 1.8rem; color: #333; margin-bottom: 25px; font-weight: 700; }}
        .conversions-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; }}
        .conversion-option {{ background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(25px); border-radius: 12px; padding: 20px; display: flex; align-items: center; gap: 15px; text-decoration: none; color: inherit; transition: all 0.3s; border: 1px solid rgba(255, 255, 255, 0.5); cursor: pointer; }}
        .conversion-option:hover {{ transform: translateY(-3px); box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12); border-color: {config["hover_border"]}; }}
        .conversion-icon {{ width: 50px; height: 50px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; color: white; background: {config["icon_gradient"]}; flex-shrink: 0; }}
        .conversion-info {{ flex: 1; }}
        .conversion-info h3 {{ font-size: 1rem; color: #333; margin-bottom: 4px; font-weight: 600; }}
        .conversion-info p {{ font-size: 0.85rem; color: #666; }}
        .conversion-arrow {{ font-size: 1.2rem; color: {config["arrow_color"]}; }}
        
        /* Popular Badge */
        .popular-badge {{ display: inline-block; background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; font-weight: 600; margin-left: 8px; }}
        
        /* Features */
        .features {{ margin-top: 50px; display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }}
        .feature-card {{ background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(25px); padding: 25px; border-radius: 12px; text-align: center; border: 1px solid rgba(255, 255, 255, 0.5); }}
        .feature-card i {{ font-size: 2.2rem; color: {config["feature_icon_color"]}; margin-bottom: 15px; }}
        .feature-card h4 {{ font-size: 1.05rem; color: #333; margin-bottom: 8px; }}
        .feature-card p {{ color: #666; font-size: 0.9rem; line-height: 1.5; }}
        
        @media (max-width: 768px) {{
            .hub-header h1 {{ font-size: 2rem; }}
            .conversions-grid {{ grid-template-columns: 1fr; }}
        }}
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
            <!-- Breadcrumb -->
            <div class="breadcrumb">
                <a href="dashboard.html">Home</a>
                <i class="fas fa-chevron-right"></i>
                <a href="converters.html">Image Converters</a>
                <i class="fas fa-chevron-right"></i>
                <span>{config["format_name"]} Converter</span>
            </div>
            
            <!-- Ad Header -->
            <div class="ad-container">
                <div class="ad-label">Advertisement</div>
                <ins class="adsbygoogle" style="display:inline-block;width:728px;height:90px" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="1234567890"></ins>
                <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
            </div>
            
            <!-- Header -->
            <div class="hub-header">
                <div class="format-badge">.{config["format_ext"]} FORMAT</div>
                <h1>{config["heading"]}</h1>
                <p>{config["description"]}</p>
            </div>
            
            <!-- Format Info -->
            <div class="format-info">
                <h2>About {config["format_name"]} Format</h2>
                <p>{config["format_description"]}</p>
            </div>
            
            <!-- Conversions Section -->
            <div class="conversions-section">
                <h2>Convert {config["format_name"]} Files To:</h2>
                <div class="conversions-grid">{conversions_html}
                </div>
            </div>
            
            <!-- Ad Middle -->
            <div class="ad-container">
                <div class="ad-label">Advertisement</div>
                <ins class="adsbygoogle" style="display:inline-block;width:336px;height:280px" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="0987654321"></ins>
                <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
            </div>
            
            <!-- Features -->
            <div class="features">
                <div class="feature-card">
                    <i class="fas fa-bolt"></i>
                    <h4>Fast Conversion</h4>
                    <p>Convert your {config["format_name"]} files in seconds with our optimized processing</p>
                </div>
                <div class="feature-card">
                    <i class="fas fa-shield-alt"></i>
                    <h4>100% Secure</h4>
                    <p>Your files are encrypted and deleted automatically after conversion</p>
                </div>
                <div class="feature-card">
                    <i class="fas fa-star"></i>
                    <h4>High Quality</h4>
                    <p>Maintain maximum quality during {config["format_name"]} file conversion</p>
                </div>
            </div>
            
            <!-- Ad Footer -->
            <div class="ad-container" style="margin-top: 40px;">
                <div class="ad-label">Advertisement</div>
                <ins class="adsbygoogle" style="display:inline-block;width:728px;height:90px" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="1122334455"></ins>
                <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
            </div>
        </div>
    </div>
    
    <script>
        function checkPremiumStatus() {{
            const isPremium = localStorage.getItem('isPremiumUser') === 'true';
            if (isPremium) {{
                document.body.classList.add('premium-user');
            }}
        }}
        checkPremiumStatus();
    </script>
</body>
</html>'''

# Hub page configurations
hubs = [
    {
        "filename": "heic-converter.html",
        "title": "HEIC Converter",
        "format_name": "HEIC",
        "format_ext": "heic",
        "heading": "HEIC File Converter",
        "description": "Convert your iPhone HEIC/HEIF photos to any image format. Fast, free, and secure conversion for Apple's High Efficiency Image Format.",
        "meta_description": "Free HEIC converter - Convert iPhone HEIC/HEIF photos to JPG, PNG, PDF and more. Fast, secure, and easy to use.",
        "format_description": "HEIC (High Efficiency Image Container) is Apple's proprietary image format that uses HEVC compression to reduce file size by up to 50% compared to JPEG while maintaining the same quality. Introduced with iOS 11, HEIC is the default format for photos taken on iPhone and iPad devices. However, HEIC files have limited compatibility with non-Apple devices and older software, making conversion necessary for sharing and editing.",
        "bg_gradient": "rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%",
        "bg_radial": "radial-gradient(circle at 20% 30%, rgba(102, 126, 234, 0.15) 0%, transparent 50%)",
        "shape1_bg": "linear-gradient(135deg, rgba(102, 126, 234, 0.25) 0%, rgba(118, 75, 162, 0.25) 100%)",
        "shape2_bg": "linear-gradient(135deg, rgba(67, 233, 123, 0.25) 0%, rgba(56, 249, 215, 0.25) 100%)",
        "badge_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "badge_shadow": "rgba(102, 126, 234, 0.3)",
        "header_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "hover_border": "#667eea",
        "icon_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "arrow_color": "#667eea",
        "feature_icon_color": "#667eea",
        "conversions": [
            {"link": "heic-to-jpg.html", "icon": "fas fa-image", "title": "HEIC to JPG", "description": "Convert to universal JPG format"},
            {"link": "heif-to-png.html", "icon": "fas fa-file-image", "title": "HEIC to PNG", "description": "Convert to PNG with transparency"},
            {"link": "heic-to-pdf.html", "icon": "fas fa-file-pdf", "title": "HEIC to PDF", "description": "Create PDF documents from HEIC"},
            {"link": "heic-to-webp.html", "icon": "fas fa-images", "title": "HEIC to WEBP", "description": "Convert to modern WEBP format"},
            {"link": "heic-to-bmp.html", "icon": "fas fa-image", "title": "HEIC to BMP", "description": "Convert to Windows BMP format"},
            {"link": "heic-to-tiff.html", "icon": "fas fa-file-image", "title": "HEIC to TIFF", "description": "Convert to professional TIFF"},
        ]
    },
    {
        "filename": "png-converter.html",
        "title": "PNG Converter",
        "format_name": "PNG",
        "format_ext": "png",
        "heading": "PNG File Converter",
        "description": "Convert PNG images to any format. Portable Network Graphics supports transparency and lossless compression for high-quality images.",
        "meta_description": "Free PNG converter - Convert PNG images to JPG, PDF, WEBP, SVG and more. Fast, secure online conversion.",
        "format_description": "PNG (Portable Network Graphics) is a raster graphics format that supports lossless compression, transparency, and high-quality images. Developed as an improved replacement for GIF, PNG is widely used for web graphics, logos, screenshots, and images requiring transparency. PNG files are larger than JPG but preserve perfect quality, making them ideal for graphics with text, sharp edges, or transparent backgrounds.",
        "bg_gradient": "rgba(79, 172, 254, 0.1) 0%, rgba(0, 242, 254, 0.1) 100%",
        "bg_radial": "radial-gradient(circle at 20% 30%, rgba(79, 172, 254, 0.15) 0%, transparent 50%)",
        "shape1_bg": "linear-gradient(135deg, rgba(79, 172, 254, 0.25) 0%, rgba(0, 242, 254, 0.25) 100%)",
        "shape2_bg": "linear-gradient(135deg, rgba(67, 233, 123, 0.25) 0%, rgba(56, 249, 215, 0.25) 100%)",
        "badge_gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
        "badge_shadow": "rgba(79, 172, 254, 0.3)",
        "header_gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
        "hover_border": "#4facfe",
        "icon_gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
        "arrow_color": "#4facfe",
        "feature_icon_color": "#4facfe",
        "conversions": [
            {"link": "png-to-jpg.html", "icon": "fas fa-image", "title": "PNG to JPG", "description": "Convert to compressed JPG format"},
            {"link": "png-to-pdf.html", "icon": "fas fa-file-pdf", "title": "PNG to PDF", "description": "Create PDF documents from PNG"},
            {"link": "png-to-webp.html", "icon": "fas fa-images", "title": "PNG to WEBP", "description": "Convert to modern web format"},
            {"link": "png-to-svg.html", "icon": "fas fa-vector-square", "title": "PNG to SVG", "description": "Trace to scalable vector format"},
            {"link": "png-to-ico.html", "icon": "fas fa-icons", "title": "PNG to ICO", "description": "Create Windows icons"},
            {"link": "png-to-bmp.html", "icon": "fas fa-image", "title": "PNG to BMP", "description": "Convert to BMP format"},
        ]
    },
    {
        "filename": "jpg-converter.html",
        "title": "JPG Converter",
        "format_name": "JPG",
        "format_ext": "jpg",
        "heading": "JPG/JPEG File Converter",
        "description": "Convert JPG/JPEG images to any format. The most popular image format for photos and web graphics with lossy compression.",
        "meta_description": "Free JPG converter - Convert JPG/JPEG images to PNG, PDF, WEBP and more. Fast, secure online conversion.",
        "format_description": "JPG/JPEG (Joint Photographic Experts Group) is the most widely used image format for photographs and web images. It uses lossy compression to significantly reduce file size while maintaining acceptable quality, making it perfect for photos, web graphics, and digital photography. JPG files are universally compatible across all devices, platforms, and software, but don't support transparency or animations.",
        "bg_gradient": "rgba(250, 112, 154, 0.1) 0%, rgba(254, 225, 64, 0.1) 100%",
        "bg_radial": "radial-gradient(circle at 20% 30%, rgba(250, 112, 154, 0.15) 0%, transparent 50%)",
        "shape1_bg": "linear-gradient(135deg, rgba(250, 112, 154, 0.25) 0%, rgba(254, 225, 64, 0.25) 100%)",
        "shape2_bg": "linear-gradient(135deg, rgba(240, 147, 251, 0.25) 0%, rgba(245, 87, 108, 0.25) 100%)",
        "badge_gradient": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
        "badge_shadow": "rgba(250, 112, 154, 0.3)",
        "header_gradient": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
        "hover_border": "#fa709a",
        "icon_gradient": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
        "arrow_color": "#fa709a",
        "feature_icon_color": "#fa709a",
        "conversions": [
            {"link": "jpg-to-png.html", "icon": "fas fa-image", "title": "JPG to PNG", "description": "Convert to PNG with transparency support"},
            {"link": "jpg-to-pdf.html", "icon": "fas fa-file-pdf", "title": "JPG to PDF", "description": "Create PDF documents from JPG"},
            {"link": "jpg-to-webp.html", "icon": "fas fa-images", "title": "JPG to WEBP", "description": "Convert to modern WEBP format"},
            {"link": "jpg-to-ico.html", "icon": "fas fa-icons", "title": "JPG to ICO", "description": "Create Windows icons from photos"},
            {"link": "jpg-to-gif.html", "icon": "fas fa-film", "title": "JPG to GIF", "description": "Convert to GIF format"},
            {"link": "jpg-to-bmp.html", "icon": "fas fa-image", "title": "JPG to BMP", "description": "Convert to BMP format"},
        ]
    },
    {
        "filename": "gif-converter.html",
        "title": "GIF Converter",
        "format_name": "GIF",
        "format_ext": "gif",
        "heading": "GIF File Converter",
        "description": "Convert GIF animations to video or extract frames. Graphics Interchange Format for animated images and simple graphics.",
        "meta_description": "Free GIF converter - Convert GIF animations to MP4, PNG, and more. Extract frames or convert to video format.",
        "format_description": "GIF (Graphics Interchange Format) is a bitmap image format that supports both static and animated images. Introduced in 1987, GIF became popular for web graphics and animations due to its support for transparency and frame-based animation. GIF uses lossless LZW compression and is limited to 256 colors, making it ideal for simple graphics, logos, and short animations, but not suitable for photographs or complex images.",
        "bg_gradient": "rgba(67, 233, 123, 0.1) 0%, rgba(56, 249, 215, 0.1) 100%",
        "bg_radial": "radial-gradient(circle at 20% 30%, rgba(67, 233, 123, 0.15) 0%, transparent 50%)",
        "shape1_bg": "linear-gradient(135deg, rgba(67, 233, 123, 0.25) 0%, rgba(56, 249, 215, 0.25) 100%)",
        "shape2_bg": "linear-gradient(135deg, rgba(79, 172, 254, 0.25) 0%, rgba(0, 242, 254, 0.25) 100%)",
        "badge_gradient": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
        "badge_shadow": "rgba(67, 233, 123, 0.3)",
        "header_gradient": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
        "hover_border": "#43e97b",
        "icon_gradient": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
        "arrow_color": "#43e97b",
        "feature_icon_color": "#43e97b",
        "conversions": [
            {"link": "gif-to-mp4.html", "icon": "fas fa-film", "title": "GIF to MP4", "description": "Convert animation to video format"},
            {"link": "gif-to-png.html", "icon": "fas fa-image", "title": "GIF to PNG", "description": "Extract frames to PNG images"},
            {"link": "gif-to-jpg.html", "icon": "fas fa-image", "title": "GIF to JPG", "description": "Convert to JPG images"},
            {"link": "gif-to-webp.html", "icon": "fas fa-images", "title": "GIF to WEBP", "description": "Convert to modern WEBP"},
            {"link": "gif-to-apng.html", "icon": "fas fa-film", "title": "GIF to APNG", "description": "Convert to animated PNG"},
            {"link": "gif-to-webm.html", "icon": "fas fa-video", "title": "GIF to WEBM", "description": "Convert to WEBM video"},
        ]
    },
    {
        "filename": "webp-converter.html",
        "title": "WEBP Converter",
        "format_name": "WEBP",
        "format_ext": "webp",
        "heading": "WEBP File Converter",
        "description": "Convert WEBP images to JPG, PNG, and more. Google's modern image format with superior compression and quality.",
        "meta_description": "Free WEBP converter - Convert WEBP images to JPG, PNG, GIF and more. Fast, secure online conversion.",
        "format_description": "WEBP is a modern image format developed by Google that provides superior lossless and lossy compression for images on the web. WEBP files are 25-35% smaller than JPEG at equivalent quality and support transparency like PNG. The format also supports animation, making it a versatile replacement for JPEG, PNG, and GIF. While browser support has improved significantly, some older systems may require conversion to more compatible formats.",
        "bg_gradient": "rgba(48, 207, 208, 0.1) 0%, rgba(51, 8, 103, 0.1) 100%",
        "bg_radial": "radial-gradient(circle at 20% 30%, rgba(48, 207, 208, 0.15) 0%, transparent 50%)",
        "shape1_bg": "linear-gradient(135deg, rgba(48, 207, 208, 0.25) 0%, rgba(51, 8, 103, 0.25) 100%)",
        "shape2_bg": "linear-gradient(135deg, rgba(102, 126, 234, 0.25) 0%, rgba(118, 75, 162, 0.25) 100%)",
        "badge_gradient": "linear-gradient(135deg, #30cfd0 0%, #330867 100%)",
        "badge_shadow": "rgba(48, 207, 208, 0.3)",
        "header_gradient": "linear-gradient(135deg, #30cfd0 0%, #330867 100%)",
        "hover_border": "#30cfd0",
        "icon_gradient": "linear-gradient(135deg, #30cfd0 0%, #330867 100%)",
        "arrow_color": "#30cfd0",
        "feature_icon_color": "#30cfd0",
        "conversions": [
            {"link": "webp-to-jpg.html", "icon": "fas fa-image", "title": "WEBP to JPG", "description": "Convert to universal JPG format"},
            {"link": "webp-to-png.html", "icon": "fas fa-file-image", "title": "WEBP to PNG", "description": "Convert to PNG format"},
            {"link": "webp-to-gif.html", "icon": "fas fa-film", "title": "WEBP to GIF", "description": "Convert to GIF animation"},
            {"link": "webp-to-bmp.html", "icon": "fas fa-image", "title": "WEBP to BMP", "description": "Convert to BMP format"},
            {"link": "webp-to-ico.html", "icon": "fas fa-icons", "title": "WEBP to ICO", "description": "Create icons from WEBP"},
            {"link": "webp-to-pdf.html", "icon": "fas fa-file-pdf", "title": "WEBP to PDF", "description": "Create PDF from WEBP"},
        ]
    }
]

# Create hub pages
created = []
for hub in hubs:
    filename = hub['filename']
    html_content = create_hub_page(hub)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    created.append(filename)
    print(f"✅ Created {filename}")

print(f"\n🎉 Successfully created {len(created)} format hub pages!")
print("\nHub pages created:")
for page in created:
    print(f"  • {page}")
