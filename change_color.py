from PIL import Image

# Wczytanie obrazu
path = input("Podaj nazwę pliku:\n")
image = Image.open(path)

# Konwersja obrazu na tryb RGB
image = image.convert("RGB")

# Pobranie rozmiarów obrazu
width, height = image.size

# Iteracja przez piksele obrazu i zmiana koloru na zielony
for x in range(width):
    for y in range(height):
        r, g, b = image.getpixel((x, y))
        image.putpixel((x, y), (r, 0, 0))  # Ustawienie wartości kanału R i B na 0, zostawienie wartości kanału G

# Zapisanie zmienionego obrazu jako pliku JPG
image.save("red_kobieta.jpg", "JPEG")
