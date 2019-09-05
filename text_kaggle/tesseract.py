try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract as tes

results = tes.image_to_string(Image.open('main.png'), boxes=True)
print results