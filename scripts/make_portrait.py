import cv2
import numpy as np
RAMP = " :+#@" 

def image_to_ascii_svg(image_path, output_svg_path, width=80):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    aspect_ratio = img.shape[0] / img.shape[1]
    height = int(width * aspect_ratio * 0.55) # Adjust for character aspect ratio
    resized = cv2.resize(img, (width, height))
    
    normalized = (resized / 255.0) * (len(RAMP) - 1)
    
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width * 10}" height="{height * 14}" viewBox="0 0 {width * 10} {height * 14}">',
        '<style>text { font-family: "JetBrains Mono", monospace; font-size: 12px; fill: #ffffff; white-space: pre; }</style>',
        '<rect width="100%" height="100%" fill="#0d1117"/>'
    ]
    
    for y in range(height):
        line_chars = ""
        for x in range(width):
            val = int(normalized[y, x])
            line_chars += RAMP[val]
        svg_lines.append(f'<text x="10" y="{(y + 1) * 14}">{line_chars}</text>')
        
    svg_lines.append('</svg>')
    
    with open(output_svg_path, 'w') as f:
        f.write('\n'.join(svg_lines))

if __name__ == "__main__":
    image_to_ascii_svg('scripts/headshot2.jpeg', 'ascii.svg')
