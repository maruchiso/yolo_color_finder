import torch
from PIL import Image
import colorsys

#załadowanie modelu
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
#załadowanie obrazka
path = input("Podaj sciezke do obrazu:\n")
image = Image.open(path)

#detekcja obiektów oraz wyświetlenie wyników
results = model(image)
results.print()
results.show()

#na liście detected zapisywane są znalezione obiekty
detected = results.xyxy[0]
names = model.names

#nazwy znalezionych obiektów
for obj in detected:
    id = int(obj[5])
    name = names[id]


x = input("Podaj nazwe obiektu:\n")
if x in name:
    print(f"Obiekt {x} znajduje sie na obrazie i jego kolor to:")


#zebranie koordynatów (rogów prostokąta)
for obj in detected:
    if name == x:
        xmin = int(obj[0])
        ymin = int(obj[1])
        xmax = int(obj[2])
        ymax = int(obj[3])
try:
    #wycięcie małego fragmentu ze środka obiektu
    width = xmax - xmin
    height = ymax - ymin
    centerx = (xmax + xmin) / 2
    centery = (ymax + ymin) / 2
    size = min(width, height)
    x1 = int(centerx - size / 8)
    y1 = int(centery - size / 8)
    x2 = int(centerx + size / 8)
    y2 = int(centery + size / 8)

    #wyświetlenie wyciętego fragmentu
    crop = image.crop((x1, y1, x2, y2))
    crop.show()

    #odczytanie wartości HSV z wyciętego fragmentu oraz znormalizowaine wartość do przedziału 0-1
    pixels = image.load()
    hues = []

    for y in range(y1, y2):
        for x in range(x1, x2):
            r, g, b = pixels[x, y]

            hsv = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)

            hue = hsv[0]
            saturation = hsv[1]
            value = hsv[2]
            hues.append(hue)
    avg_hue = sum(hues) / len(hues)
    #print(avg_hue, saturation, value) wyświetlenie wartości HSV

    #translacja wartości HSV na nazwę koloru
    color_name = ""

    if value < 0.2:
        color_name = "Czarny"
    elif value > 0.8 and saturation < 0.2:
        color_name = "Biały"
    elif saturation < 0.1:
        color_name = "Szary"
    elif 0.1 > avg_hue >= 0 or 1 >= avg_hue >= 0.92:
        color_name = "Czerwony"
    elif 0.1 <= avg_hue < 0.25:
        color_name = "Żółty"
    elif 0.25 <= avg_hue < 0.45:
        color_name = "Zielony"
    elif 0.45 <= avg_hue < 0.75:
        color_name = "Niebieski"
    elif 0.75 <= avg_hue < 0.92:
        color_name = "Różowy"
    else:
        color_name = "Nieznany"

    #odczytanie jasności koloru
    odcien = ''
    if 0.2 <= value < 0.4:
        odcien = 'Ciemny'
    elif 0.6 < value:
        odcien = 'Jasny'
    else:
        odcien = odcien
    if color_name == "Biały" or color_name == "Czarny":
        odcien = ''


    print(odcien, color_name)
except:
    print(f"Obiekt {x} nie znajduje sie na obrazie\n")
#wykrywanie "jest tyle samochodów i kolor każdego" "2 różne rzeczy na obrazku" oraz buckety (czyli piki jakie są i mówi jakie kolory)
#narazie 4, półoceny wyżej jeśli wykonam jedno z góry
