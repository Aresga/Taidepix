import argparse
from taidepix.utils.image_loader import load_image # Updated import
from taidepix.algorithms.dither_algorithms import DitherAlgorithms
from taidepix.utils.image_display import image_display
import sys

ALGORITHM_MAP = {
    'floyd_steinberg': DitherAlgorithms.floyd_steinberg,
    'simple_threshold': DitherAlgorithms.simple_threshold,
    'random': DitherAlgorithms.random_dither,
    'ordered': DitherAlgorithms.ordered_dither,
    'atkinson': DitherAlgorithms.atkinson,
    'burkes': DitherAlgorithms.burkes,
    'sierra': DitherAlgorithms.sierra,
    'jjn': DitherAlgorithms.jjn,
    'stucki': DitherAlgorithms.stucki,
}

def argparser():
    parser = argparse.ArgumentParser(description="Dither an image and display it in the terminal.")
    parser.add_argument('image_path', help='Path to the input image')
    parser.add_argument('--width', '-w', type=int, default=80, help='Output width in characters (default: 80)')
    parser.add_argument('--algorithm', '-a', choices=ALGORITHM_MAP.keys(), default='floyd_steinberg', help='Dithering algorithm to use')
    parser.add_argument('--charset', '-c', choices=['ascii', 'blocks', 'braille'], default='ascii', help='Character set for output (ascii, blocks, or braille)')
    parser.add_argument('--color', action='store_true', help='Enable 24-bit color output (RGB blocks)')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    return parser

def main():
    parser = argparser()
    args = parser.parse_args()

    # Load the original image in color
    img_color = load_image(args.image_path)
    if img_color is None: # Handle potential loading errors if loader returns None
         sys.exit(1)

    # --- Dithering Logic (only if not using --color) ---
    dithered_img = None
    if not args.color:
        # Convert to grayscale *only* for dithering
        img_gray = img_color.convert('L')
        dither_func = ALGORITHM_MAP[args.algorithm]
        if args.algorithm == 'simple_threshold':
            dithered_img = dither_func(img_gray, threshold=150)
        else:
            dithered_img = dither_func(img_gray)
    # --- End Dithering Logic ---

    # Choose which image to display
    display_img = img_color if args.color else dithered_img

    # Pass the chosen image and color flag to image_display
    ascii_art = image_display(display_img, width=args.width, charset=args.charset, color=args.color)
    print(ascii_art)

if __name__ == "__main__":
    main()
