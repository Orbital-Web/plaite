import cv2
from pyzbar.pyzbar import decode


def read_barcode(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray_image)

    if not barcodes:
        return "No barcode found."

    for barcode in barcodes:
        barcode_data = barcode.data.decode("utf-8")
        barcode_type = barcode.type
        print(f"Barcode: {barcode_data}, Type: {barcode_type}")

    return barcodes


image_path = r".\plaite\image.png"
barcodes = read_barcode(image_path)

if barcodes:
    print("Barcodes detected successfully!")
