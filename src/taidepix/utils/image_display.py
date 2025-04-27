from taidepix.algorithms.dither_algorithms import DitherAlgorithms
import sys

ASCII_CHARS = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@']
BLOCK_CHARS = [' ', '░', '▒', '▓', '█']

def rgb_to_ansi(r, g, b):
    return f'\033[38;2;{r};{g};{b}m'

def image_display(img, width=80, charset='ascii', color=False):
    if color:
        # Color mode: use '█' and 24-bit ANSI color
        img = img.convert('RGB')
        aspect_ratio = img.height / img.width
        new_height = int(aspect_ratio * width * 0.5)
        img = img.resize((width, new_height))
        pixels = list(img.getdata())
        out = ''
        for i, (r, g, b) in enumerate(pixels):
            out += f"{rgb_to_ansi(r, g, b)}█"
            if (i + 1) % width == 0:
                out += '\033[0m\n'
        out += '\033[0m'
        return out

    if charset == 'braille':
        # Braille: each char = 2x2 pixels
        aspect_ratio = img.height / img.width
        new_width = width * 2
        new_height = int(aspect_ratio * width * 2)
        img = img.resize((new_width, new_height))
        arr = list(img.getdata())
        arr = [arr[i * new_width:(i + 1) * new_width] for i in range(new_height)]
        lines = []
        for y in range(0, new_height, 4):
            line = ''
            for x in range(0, new_width, 2):
                dots = 0
                for dy in range(4):
                    for dx in range(2):
                        yy = y + dy
                        xx = x + dx
                        if yy < new_height and xx < new_width:
                            pixel = arr[yy][xx]
                            if pixel < 128:
                                # Braille dot order: 0,3,1,4,2,5,6,7
                                dot_idx = [0,3,1,4,2,5,6,7][dy*2+dx]
                                dots |= (1 << dot_idx)
                braille_char = chr(0x2800 + dots)
                line += braille_char
            lines.append(line)
        return '\n'.join(lines)

    aspect_ratio = img.height / img.width
    new_height = int(aspect_ratio * width * 0.5)
    img = img.resize((width, new_height))
    pixels = img.getdata()
    if charset == 'blocks':
        chars = BLOCK_CHARS
        step = 256 // len(chars)
    else:
        chars = ASCII_CHARS
        step = 256 // len(chars)
    ascii_str = ''
    for i, pixel in enumerate(pixels):
        ascii_str += chars[min(pixel // step, len(chars)-1)]
        if (i + 1) % width == 0:
            ascii_str += '\n'
    return ascii_str