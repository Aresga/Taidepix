from PIL import Image

def load_image(path, size=None):
    """
    Load an image, convert to RGB, and optionally resize.
    Returns a Pillow Image object in 'RGB' mode.
    """
    print(f"Loading image from {path}")
    try:
        img = Image.open(path).convert('RGB')
        if size:
            img = img.resize(size)
        return img
    except Exception as e:
        print(f"Error loading image: {e}")
        exit(1)
        # return None
