#!/usr/bin/env python3
"""
Generate HTML for remaining converter cards (GIF and EPS sections)
"""

# GIF converters - FROM GIF
gif_audio_video = [
    ('aac', 'AAC', 'music', 'Convert GIF to AAC audio'),
    ('aiff', 'AIFF', 'music', 'Convert GIF to AIFF audio'),
    ('flac', 'FLAC', 'music', 'Convert GIF to FLAC audio'),
    ('m4a', 'M4A', 'music', 'Convert GIF to M4A audio'),
    ('mp3', 'MP3', 'music', 'Convert GIF to MP3 audio'),
    ('wav', 'WAV', 'music', 'Convert GIF to WAV audio'),
    ('wma', 'WMA', 'music', 'Convert GIF to WMA audio'),
    ('avi', 'AVI', 'video', 'Convert GIF to AVI video'),
    ('flv', 'FLV', 'video', 'Convert GIF to FLV video'),
    ('mkv', 'MKV', 'video', 'Convert GIF to MKV video'),
    ('mov', 'MOV', 'video', 'Convert GIF to MOV video'),
    ('mp4', 'MP4', 'video', 'Convert GIF to MP4 video'),
    ('webm', 'WEBM', 'video', 'Convert GIF to WEBM video'),
    ('wmv', 'WMV', 'video', 'Convert GIF to WMV video'),
]

# TO GIF converters (excluding ones already added)
to_gif_formats = [
    ('3g2', '3G2', 'video'), ('3gp', '3GP', 'video'), ('3gpp', '3GPP', 'video'),
    ('avi', 'AVI', 'video'), ('cavs', 'CAVS', 'video'), ('dv', 'DV', 'video'),
    ('dvr', 'DVR', 'video'), ('flv', 'FLV', 'video'), ('m2ts', 'M2TS', 'video'),
    ('m4v', 'M4V', 'video'), ('mkv', 'MKV', 'video'), ('mod', 'MOD', 'video'),
    ('mov', 'MOV', 'video'), ('mp4', 'MP4', 'video'), ('mpeg', 'MPEG', 'video'),
    ('mpg', 'MPG', 'video'), ('mts', 'MTS', 'video'), ('mxf', 'MXF', 'video'),
    ('ogv', 'OGV', 'video'), ('rm', 'RM', 'video'), ('rmvb', 'RMVB', 'video'),
    ('swf', 'SWF', 'video'), ('ts', 'TS', 'video'), ('vob', 'VOB', 'video'),
    ('webm', 'WEBM', 'video'), ('wmv', 'WMV', 'video'), ('wtv', 'WTV', 'video'),
    ('dwg', 'DWG', 'drafting-compass'), ('dxf', 'DXF', 'project-diagram'),
    ('emf', 'EMF', 'file-image'), ('eps', 'EPS', 'file-image'),
    ('gif', 'GIF', 'film'), ('ico', 'ICO', 'icons'),
    ('jfif', 'JFIF', 'image'), ('jpeg', 'JPEG', 'image'), ('jpg', 'JPG', 'image'),
    ('odd', 'ODD', 'file-alt'), ('pdf', 'PDF', 'file-pdf'),
    ('ppm', 'PPM', 'file-image'), ('ps', 'PS', 'file-image'), ('psd', 'PSD', 'image'),
    ('svg', 'SVG', 'vector-square'), ('svgz', 'SVGZ', 'vector-square'),
    ('tif', 'TIF', 'file-image'), ('tiff', 'TIFF', 'file-image'),
    ('xcf', 'XCF', 'layer-group'), ('xps', 'XPS', 'file-pdf'),
]

# EPS converters - FROM EPS (with vector formats)
eps_extra = [
    ('dxf', 'DXF', 'Convert EPS to DXF CAD format'),
    ('emf', 'EMF', 'Convert EPS to EMF vector'),
    ('svg', 'SVG', 'Convert EPS to SVG vector'),
    ('wmf', 'WMF', 'Convert EPS to WMF vector'),
]

# TO EPS converters (excluding ones already added)
to_eps_formats = [
    ('ai', 'AI', 'Adobe Illustrator'), ('cdr', 'CDR', 'CorelDRAW'),
    ('cgm', 'CGM', 'Computer Graphics'), ('dps', 'DPS', 'Kingsoft'),
    ('dwg', 'DWG', 'AutoCAD'), ('dxf', 'DXF', 'CAD Exchange'),
    ('emf', 'EMF', 'Windows Metafile'), ('eps', 'EPS', 'PostScript'),
    ('gif', 'GIF', 'image'), ('ico', 'ICO', 'icon'),
    ('jfif', 'JFIF', 'image'), ('jpeg', 'JPEG', 'image'), ('jpg', 'JPG', 'image'),
    ('mos', 'MOS', 'RAW'), ('mrw', 'MRW', 'RAW'), ('nef', 'NEF', 'RAW'),
    ('odd', 'ODD', 'document'), ('odp', 'ODP', 'presentation'),
    ('orf', 'ORF', 'RAW'), ('pdf', 'PDF', 'document'),
    ('pef', 'PEF', 'RAW'), ('png', 'PNG', 'image'),
    ('ppm', 'PPM', 'image'), ('pps', 'PPS', 'presentation'),
    ('ppsx', 'PPSX', 'presentation'), ('ppt', 'PPT', 'presentation'),
    ('pptm', 'PPTM', 'presentation'), ('pptx', 'PPTX', 'presentation'),
    ('ps', 'PS', 'PostScript'), ('psd', 'PSD', 'Photoshop'),
    ('raf', 'RAF', 'RAW'), ('raw', 'RAW', 'camera'), ('rw2', 'RW2', 'RAW'),
    ('sk', 'SK', 'Sketch'), ('sk1', 'SK1', 'Sketch'),
    ('svg', 'SVG', 'vector'), ('svgz', 'SVGZ', 'vector'),
    ('tif', 'TIF', 'image'), ('tiff', 'TIFF', 'image'),
    ('vsd', 'VSD', 'Visio'), ('webp', 'WEBP', 'image'),
    ('wmf', 'WMF', 'Windows Metafile'), ('x3f', 'X3F', 'RAW'),
    ('xcf', 'XCF', 'GIMP'), ('xps', 'XPS', 'document'),
]

def generate_card(href, icon, title, desc):
    return f'''                    <a href="{href}" class="converter-card" target="_blank">
                        <div class="converter-icon">
                            <i class="fas fa-{icon}"></i>
                        </div>
                        <h3>{title}</h3>
                        <p>{desc}</p>
                    </a>'''

# Generate GIF section
print("<!-- GIF to Audio/Video Converters -->")
for fmt, name, icon, desc in gif_audio_video:
    print(generate_card(f"gif-to-{fmt}.html", icon, f"GIF to {name}", desc))

# Generate TO GIF section  
print("\n<!-- Various Formats to GIF Converters -->")
for fmt, name, icon in to_gif_formats:
    print(generate_card(f"{fmt}-to-gif.html", icon, f"{name} to GIF", f"Convert {name} to GIF format"))

# Generate EPS vector section
print("\n<!-- EPS to Vector Formats -->")
for fmt, name, desc in eps_extra:
    print(generate_card(f"eps-to-{fmt}.html", "file-image", f"EPS to {name}", desc))

# Generate TO EPS section
print("\n<!-- Various Formats to EPS Converters -->")
for fmt, name, desc in to_eps_formats:
    icon = 'camera' if 'RAW' in desc or 'camera' in desc else 'file-image'
    print(generate_card(f"{fmt}-to-eps.html", icon, f"{name} to EPS", f"Convert {desc} {name} to EPS"))

print(f"\n<!-- End of generated cards -->")
