# import cv2
# import numpy as np
# RAMP = " :+#@" 

# def image_to_ascii_svg(image_path, output_svg_path, width=80):
#     img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#     aspect_ratio = img.shape[0] / img.shape[1]
#     height = int(width * aspect_ratio * 0.55) # Adjust for character aspect ratio
#     resized = cv2.resize(img, (width, height))
    
#     normalized = (resized / 255.0) * (len(RAMP) - 1)
    
#     svg_lines = [
#         f'<svg xmlns="http://www.w3.org/2000/svg" width="{width * 10}" height="{height * 14}" viewBox="0 0 {width * 10} {height * 14}">',
#         '<style>text { font-family: "JetBrains Mono", monospace; font-size: 12px; fill: #ffffff; white-space: pre; }</style>',
#         '<rect width="100%" height="100%" fill="#0d1117"/>'
#     ]
    
#     for y in range(height):
#         line_chars = ""
#         for x in range(width):
#             val = int(normalized[y, x])
#             line_chars += RAMP[val]
#         svg_lines.append(f'<text x="10" y="{(y + 1) * 14}">{line_chars}</text>')
        
#     svg_lines.append('</svg>')
    
#     with open(output_svg_path, 'w') as f:
#         f.write('\n'.join(svg_lines))

# if __name__ == "__main__":
#     image_to_ascii_svg('scripts/headshot2.jpeg', 'ascii.svg')

import cv2
import numpy as np

RAMP = " :+#@"

def crop_center_square(img):
    """Crops the image to a strict 1:1 square centered on the subject."""
    h, w = img.shape[:2]
    min_dim = min(h, w)
    start_x = (w - min_dim) // 2
    start_y = (h - min_dim) // 2
    return img[start_y:start_y + min_dim, start_x:start_x + min_dim]

def image_to_ascii_svg(image_path, output_svg_path, width=70):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not load image at {image_path}")

    # 1. Force strict center square crop
    cropped = crop_center_square(img)

    # 2. Set height based on monospace font character aspect ratio (~0.55)
    # This prevents vertical stretching on square crops
    height = int(width * 0.55)
    resized = cv2.resize(cropped, (width, height))

    # 3. Normalize pixels to character ramp
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
