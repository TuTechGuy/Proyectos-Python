from PIL import Image
import pytesseract

class FacturaProcessor:
    @staticmethod
    def extraer_texto(imagen):
        img = Image.open(imagen)
        return pytesseract.image_to_string(img)
