import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.transforms as transforms

# Einstellungen
feld_breite = 0.8
feld_hoehe = 1.3  # Hochformat wie im echten Brett
felder_pro_seite = 9  # 9 Felder zwischen Ecken
gesamt_felder = 40

# Beispielhafte Felder (wie zuvor)
farbenliste = {
    "brown": "#8B4513",
    "lightblue": "#ADD8E6",
    "pink": "#FFB6C1",
    "orange": "#FFA500",
    "red": "#FF0000",
    "yellow": "#FFFF00",
    "green": "#008000",
    "darkblue": "#00008B",
    "gray": "#B0B0B0",
    "white": "white",
    "skyblue": "#87CEEB"
}

felder = [
    {"name": "Start", "typ": "sonder", "farbe": "white"},
    {"name": "Kärntner Straße", "typ": "straße", "farbe": "brown"},
    {"name": "Gemeinschaft", "typ": "gemeinschaft", "farbe": "skyblue"},
    {"name": "Opernring", "typ": "straße", "farbe": "brown"},
    {"name": "Einkommenssteuer", "typ": "steuer", "farbe": "white"},
    {"name": "Westbahnhof", "typ": "bahnhof", "farbe": "gray"},
    {"name": "Neubaugasse", "typ": "straße", "farbe": "lightblue"},
    {"name": "Ereignis", "typ": "ereignis", "farbe": "orange"},
    {"name": "Mariahilfer Straße", "typ": "straße", "farbe": "lightblue"},
    {"name": "Museumsstraße", "typ": "straße", "farbe": "lightblue"},

    {"name": "Gefängnis", "typ": "sonder", "farbe": "white"},
    {"name": "Burggasse", "typ": "straße", "farbe": "pink"},
    {"name": "Elektrizitätswerk", "typ": "werk", "farbe": "white"},
    {"name": "Lerchenfelder Straße", "typ": "straße", "farbe": "pink"},
    {"name": "Josefstädter Straße", "typ": "straße", "farbe": "pink"},
    {"name": "Franz-Josefs-Bahnhof", "typ": "bahnhof", "farbe": "gray"},
    {"name": "Alser Straße", "typ": "straße", "farbe": "orange"},
    {"name": "Gemeinschaft", "typ": "gemeinschaft", "farbe": "skyblue"},
    {"name": "Währinger Straße", "typ": "straße", "farbe": "orange"},
    {"name": "Schottenring", "typ": "straße", "farbe": "orange"},

    {"name": "Frei Parken", "typ": "sonder", "farbe": "white"},
    {"name": "Universitätsstraße", "typ": "straße", "farbe": "red"},
    {"name": "Ereignis", "typ": "ereignis", "farbe": "orange"},
    {"name": "Schottengasse", "typ": "straße", "farbe": "red"},
    {"name": "Graben", "typ": "straße", "farbe": "red"},
    {"name": "Südbahnhof", "typ": "bahnhof", "farbe": "gray"},
    {"name": "Kohlmarkt", "typ": "straße", "farbe": "yellow"},
    {"name": "Kärntner Ring", "typ": "straße", "farbe": "yellow"},
    {"name": "Wasserwerk", "typ": "werk", "farbe": "white"},
    {"name": "Ringstraße", "typ": "straße", "farbe": "yellow"},

    {"name": "Gehe ins Gefängnis", "typ": "sonder", "farbe": "white"},
    {"name": "Landstraße", "typ": "straße", "farbe": "green"},
    {"name": "Ungargasse", "typ": "straße", "farbe": "green"},
    {"name": "Gemeinschaft", "typ": "gemeinschaft", "farbe": "skyblue"},
    {"name": "Rennweg", "typ": "straße", "farbe": "green"},
    {"name": "Nordbahnhof", "typ": "bahnhof", "farbe": "gray"},
    {"name": "Ereignis", "typ": "ereignis", "farbe": "orange"},
    {"name": "Praterstraße", "typ": "straße", "farbe": "darkblue"},
    {"name": "Luxussteuer", "typ": "steuer", "farbe": "white"},
    {"name": "Stephansplatz", "typ": "straße", "farbe": "darkblue"},
]

# Zeichenfläche vorbereiten
feldanzahl_pro_reihe = felder_pro_seite + 1
brettgröße = feldanzahl_pro_reihe * feld_breite
fig, ax = plt.subplots(figsize=(12, 12))
ax.set_xlim(0, brettgröße)
ax.set_ylim(0, brettgröße)
ax.set_aspect('equal')
ax.axis('off')


# Zeichenfunktion
def zeichne_feld(x, y, name, farbe, horizontal, rotation):
    if horizontal:
        rect = Rectangle((x, y), feld_breite, feld_hoehe, facecolor='white', edgecolor='black')
        balken = Rectangle((x, y + feld_hoehe - 0.3), feld_breite, 0.3, facecolor=farbe, edgecolor='black')
        text_x, text_y = x + feld_breite / 2, y + feld_hoehe / 2 - 0.2
    else:
        rect = Rectangle((x, y), feld_hoehe, feld_breite, facecolor='white', edgecolor='black')
        balken = Rectangle((x + feld_hoehe - 0.3, y), 0.3, feld_breite, facecolor=farbe, edgecolor='black')
        text_x, text_y = x + feld_hoehe / 2, y + feld_breite / 2

    ax.add_patch(rect)
    ax.add_patch(balken)
    trans = transforms.Affine2D().rotate_deg_around(text_x, text_y, rotation) + ax.transData
    ax.text(text_x, text_y, name, ha='center', va='center', fontsize=6, wrap=True, transform=trans)


# Positionen & Zeichnung
for i, feld in enumerate(felder):
    farbe = farbenliste.get(feld["farbe"], "white")

    if i < 10:
        x = brettgröße - (i + 1) * feld_breite
        y = 0
        zeichne_feld(x, y, feld["name"], farbe, horizontal=True, rotation=0)
    elif i < 20:
        x = 0
        y = (i - 10) * feld_breite
        zeichne_feld(x, y, feld["name"], farbe, horizontal=False, rotation=90)
    elif i < 30:
        x = (i - 20) * feld_breite
        y = brettgröße - feld_hoehe
        zeichne_feld(x, y, feld["name"], farbe, horizontal=True, rotation=180)
    else:
        x = brettgröße - feld_hoehe
        y = brettgröße - (i - 30 + 1) * feld_breite
        zeichne_feld(x, y, feld["name"], farbe, horizontal=False, rotation=270)

plt.tight_layout()
plt.show()
