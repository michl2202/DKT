from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import pandas as pd


def create_property_cards_from_excel(excel_file="besitzkarten.xlsx", output_folder="property_cards"):
    """
    Erstellt Grundstückskarten aus Excel-Datei mit farbigem oberen Balken

    Args:
        excel_file (str): Pfad zur Excel-Datei
        output_folder (str): Ordner für die generierten Bilder
    """

    try:
        # Excel-Datei einlesen
        df = pd.read_excel(excel_file)
        print(f"📊 Excel-Datei geladen: {len(df)} Grundstückskarten gefunden")

        # Überprüfen ob die erforderlichen Spalten vorhanden sind
        required_columns = ['Name', 'Farbe', 'Kaufpreis', 'Miete', 'Miete_1_Haus', 'Miete_2_Haus', 'Miete_3_Haus',
                            'Miete_4_Haus', 'Miete_Hotel', 'Hauspreis', 'Hypothek']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            print(f"❌ Fehlende Spalten in der Excel-Datei: {missing_columns}")
            print(f"📋 Verfügbare Spalten: {list(df.columns)}")
            return

        # Kartenabmessungen im Hochformat (Grundstückskarten)
        card_width = 675  # Schmaler als Ereigniskarten
        card_height = 1050  # Höher als Ereigniskarten

        # Ausgabeordner erstellen
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Für jede Zeile in der Excel-Datei eine Karte erstellen
        for index, row in df.iterrows():
            # Daten aus Excel lesen
            property_data = {
                'name': str(row['Name']) if pd.notna(row['Name']) else "",
                'color': str(row['Farbe']) if pd.notna(row['Farbe']) else "#0066CC",
                'kaufpreis': int(row['Kaufpreis']) if pd.notna(row['Kaufpreis']) else 0,
                'miete': int(row['Miete']) if pd.notna(row['Miete']) else 0,
                'miete_1_haus': int(row['Miete_1_Haus']) if pd.notna(row['Miete_1_Haus']) else 0,
                'miete_2_haus': int(row['Miete_2_Haus']) if pd.notna(row['Miete_2_Haus']) else 0,
                'miete_3_haus': int(row['Miete_3_Haus']) if pd.notna(row['Miete_3_Haus']) else 0,
                'miete_4_haus': int(row['Miete_4_Haus']) if pd.notna(row['Miete_4_Haus']) else 0,
                'miete_hotel': int(row['Miete_Hotel']) if pd.notna(row['Miete_Hotel']) else 0,
                'hauspreis': int(row['Hauspreis']) if pd.notna(row['Hauspreis']) else 0,
                'hypothek': int(row['Hypothek']) if pd.notna(row['Hypothek']) else 0
            }

            # Leere Namen überspringen
            if not property_data['name']:
                continue

            # Grundstückskarte erstellen
            img = create_property_card(property_data, card_width, card_height)

            # Bild speichern
            filename = f"property_card_{index + 1:02d}_{property_data['name'].replace(' ', '_')}.png"
            filepath = os.path.join(output_folder, filename)
            img.save(filepath, dpi=(300, 300))
            print(f"Grundstückskarte {index + 1} erstellt: {filepath}")

        print(f"\n✅ {len(df)} Grundstückskarten aus Excel erfolgreich erstellt!")

    except FileNotFoundError:
        print(f"❌ Excel-Datei '{excel_file}' nicht gefunden!")
        print("📝 Stelle sicher, dass die Datei im gleichen Ordner liegt.")
        create_sample_property_excel(excel_file)
    except Exception as e:
        print(f"❌ Fehler beim Lesen der Excel-Datei: {e}")


def create_property_card(property_data, card_width, card_height):
    """
    Erstellt eine einzelne Grundstückskarte
    """

    # Neues Bild mit transparentem Hintergrund erstellen
    img = Image.new('RGBA', (card_width, card_height), (0, 0, 0, 0))

    # Abgerundete Karte als Basis erstellen
    card_base = create_rounded_property_base(card_width, card_height)
    img.paste(card_base, (0, 0))

    draw = ImageDraw.Draw(img)

    # Farbiger oberer Balken
    color_bar_height = 120
    corner_radius = 50

    # Oberer farbiger Balken (abgerundete obere Ecken)
    draw.rounded_rectangle(
        [3, 3, card_width - 3, color_bar_height],
        radius=corner_radius,
        fill=property_data['color'],
        outline='black',
        width=2
    )

    # Rechteck unten am farbigen Balken (um untere Ecken gerade zu machen)
    draw.rectangle(
        [3, color_bar_height - corner_radius, card_width - 3, color_bar_height],
        fill=property_data['color'],
        outline=None
    )

    # Linie unter dem farbigen Balken
    draw.line(
        [3, color_bar_height, card_width - 3, color_bar_height],
        fill='black',
        width=2
    )

    # Grundstücksname im farbigen Balken
    add_property_name(draw, property_data['name'], card_width, color_bar_height)

    # Preisinformationen hinzufügen
    add_property_details(draw, property_data, card_width, card_height, color_bar_height)

    # In RGB konvertieren für Speicherung
    final_img = Image.new('RGB', (card_width, card_height), 'white')
    final_img.paste(img, (0, 0), img)

    return final_img


def create_rounded_property_base(width, height):
    """
    Erstellt eine abgerundete Grundstückskarten-Basis
    """
    base = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(base)

    outer_corner_radius = 50

    draw.rounded_rectangle(
        [0, 0, width, height],
        radius=outer_corner_radius,
        fill='white',
        outline='black',
        width=3
    )

    return base


def add_property_name(draw, name, card_width, color_bar_height):
    """
    Fügt den Grundstücksnamen im farbigen Balken hinzu
    """
    try:
        font_name = ImageFont.truetype("arial.ttf", 48)  # Viel größer: 48pt
    except:
        font_name = ImageFont.load_default()

    # Text in Zeilen aufteilen falls zu lang
    max_chars = 14  # Weniger Zeichen da größere Schrift
    name_lines = textwrap.fill(name, width=max_chars).split('\n')

    # Zeilenhöhe berechnen
    line_height = font_name.getbbox("Ag")[3] - font_name.getbbox("Ag")[1] + 4
    total_height = len(name_lines) * line_height

    # Startposition für vertikale Zentrierung im farbigen Balken
    start_y = (color_bar_height - total_height) // 2

    # Namen zeichnen (weiß auf farbigem Hintergrund)
    current_y = start_y
    for line in name_lines:
        bbox = draw.textbbox((0, 0), line, font=font_name)
        text_width = bbox[2] - bbox[0]
        x = (card_width - text_width) // 2
        draw.text((x, current_y), line, fill='white', font=font_name)
        current_y += line_height


def add_property_details(draw, property_data, card_width, card_height, color_bar_height):
    """
    Fügt die Preisinformationen zur Grundstückskarte mit vertikal zentriertem Kaufpreis hinzu
    """
    try:
        font_large = ImageFont.truetype("arial.ttf", 40)  # Kaufpreis
        font_medium = ImageFont.truetype("arial.ttf", 30)  # Mieten
        font_small = ImageFont.truetype("arial.ttf", 28)  # Häuser/Hypothek
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Verfügbare Höhe berechnen
    available_height = card_height - color_bar_height - 40  # 40px Rand unten
    start_y = color_bar_height + 30

    margin = 40
    price_column_x = card_width - 80

    # Kompakte Zeilenabstände innerhalb der Abschnitte
    line_spacing_medium = 6  # Kompakter für mehr Platz
    line_spacing_small = 4  # Kompakter für mehr Platz
    separator_height = 8

    # Berechne die Höhe jedes Abschnitts
    # Abschnitt 1: Kaufpreis
    section1_height = font_large.getbbox("Ag")[3] - font_large.getbbox("Ag")[1]

    # Abschnitt 2: Mieten (6 Zeilen)
    miete_content_height = 6 * (
                font_medium.getbbox("Ag")[3] - font_medium.getbbox("Ag")[1] + line_spacing_medium) - line_spacing_medium

    # Abschnitt 3: Häuser + Hypothek (4 Zeilen total)
    house_content_height = 4 * (
                font_small.getbbox("Ag")[3] - font_small.getbbox("Ag")[1] + line_spacing_small) - line_spacing_small

    # Gesamte Content-Höhe
    total_content_height = section1_height + miete_content_height + house_content_height + 2 * separator_height

    # Verfügbaren Platz auf 5 Bereiche verteilen (3 Abschnitte + 2 Trennbereiche)
    remaining_space = available_height - total_content_height
    section_spacing = max(15, remaining_space // 5)  # Mindestens 15px Abstand

    current_y = start_y

    # 1. KAUFPREIS ABSCHNITT (vertikal zentriert in seinem Bereich)
    kaufpreis_section_height = section1_height + section_spacing
    kaufpreis_center_y = current_y + (kaufpreis_section_height - section1_height) // 2

    kaufpreis_text = f"KAUFPREIS {property_data['kaufpreis']} €"
    bbox = draw.textbbox((0, 0), kaufpreis_text, font=font_large)
    text_width = bbox[2] - bbox[0]
    x = (card_width - text_width) // 2
    draw.text((x, kaufpreis_center_y), kaufpreis_text, fill='black', font=font_large)

    current_y += kaufpreis_section_height

    # Trennstrich 1
    draw_separator_line(draw, current_y, card_width, margin, price_column_x)
    current_y += separator_height + section_spacing

    # 2. MIETEN ABSCHNITT
    miete_lines = [
        ("Miete allein", f"{property_data['miete']} €"),
        ("Miete mit 1 Haus", f"{property_data['miete_1_haus']} €"),
        ("Miete mit 2 Häusern", f"{property_data['miete_2_haus']} €"),
        ("Miete mit 3 Häusern", f"{property_data['miete_3_haus']} €"),
        ("Miete mit 4 Häusern", f"{property_data['miete_4_haus']} €"),
        ("Miete mit Hotel", f"{property_data['miete_hotel']} €")
    ]

    for label, value in miete_lines:
        # Label linksbündig
        draw.text((margin, current_y), label, fill='black', font=font_medium)

        # Preis rechtsbündig
        bbox = draw.textbbox((0, 0), value, font=font_medium)
        text_width = bbox[2] - bbox[0]
        draw.text((price_column_x - text_width, current_y), value, fill='black', font=font_medium)

        current_y += font_medium.getbbox("Ag")[3] - font_medium.getbbox("Ag")[1] + line_spacing_medium

    current_y += section_spacing - line_spacing_medium

    # Trennstrich 2
    draw_separator_line(draw, current_y, card_width, margin, price_column_x)
    current_y += separator_height + section_spacing

    # 3. HÄUSER UND HYPOTHEK ABSCHNITT
    house_lines = [
        ("Häuser kosten je", f"{property_data['hauspreis']} €"),
        ("Hotels kosten je", f"{property_data['hauspreis']} €"),
        ("(plus 4 Häuser)", ""),
        ("Hypothek", f"{property_data['hypothek']} €")
    ]

    for label, value in house_lines:
        # Label linksbündig
        if label:
            draw.text((margin, current_y), label, fill='black', font=font_small)

        # Preis rechtsbündig (falls vorhanden)
        if value:
            bbox = draw.textbbox((0, 0), value, font=font_small)
            text_width = bbox[2] - bbox[0]
            draw.text((price_column_x - text_width, current_y), value, fill='black', font=font_small)

        current_y += font_small.getbbox("Ag")[3] - font_small.getbbox("Ag")[1] + line_spacing_small


def draw_separator_line(draw, y_position, card_width, left_margin, right_margin):
    """
    Zeichnet eine dickere Trennlinie, die mit dem Text abschließt
    """
    line_color = '#AAAAAA'  # Hellgrau für dezenten Look

    # Linie von linkem Textrand bis rechtem Textrand
    draw.line(
        [left_margin, y_position, right_margin, y_position],
        fill=line_color,
        width=3  # Dicker: 3px
    )


def create_sample_property_excel(filename="besitzkarten.xlsx"):
    """
    Erstellt eine Beispiel-Excel-Datei für Besitzkarten
    """

    sample_data = {
        'Name': [
            'Badstraße',
            'Turmstraße',
            'Chausseestraße',
            'Elisenstraße',
            'Poststraße',
            'Seestraße',
            'Hafenstraße',
            'Neue Straße',
            'Münchener Straße',
            'Wiener Straße',
            'Berliner Straße',
            'Hamburger Straße',
            'Frankfurter Straße',
            'Kölner Straße',
            'Stuttgarter Straße',
            'Münchener Platz',
            'Wiener Platz',
            'Berliner Platz',
            'Hamburger Platz',
            'Parkstraße',
            'Schlossallee'
        ],
        'Farbe': [
            '#8B4513', '#8B4513',  # Braun
            '#87CEEB', '#87CEEB', '#87CEEB',  # Hellblau
            '#FF69B4', '#FF69B4', '#FF69B4',  # Pink
            '#FFA500', '#FFA500', '#FFA500',  # Orange
            '#FF0000', '#FF0000', '#FF0000',  # Rot
            '#FFFF00', '#FFFF00', '#FFFF00',  # Gelb
            '#00FF00', '#00FF00', '#00FF00',  # Grün
            '#0000FF', '#0000FF'  # Blau
        ],
        'Kaufpreis': [
            60, 60, 100, 100, 120, 140, 140, 160, 180, 180, 200, 220, 220, 240, 260, 280, 300, 300, 320, 350, 400
        ],
        'Miete': [
            2, 4, 6, 6, 8, 10, 10, 12, 14, 14, 16, 18, 18, 20, 22, 24, 26, 26, 28, 35, 50
        ],
        'Miete_1_Haus': [
            10, 20, 30, 30, 40, 50, 50, 60, 70, 70, 80, 90, 90, 100, 110, 120, 130, 130, 150, 175, 200
        ],
        'Miete_2_Haus': [
            30, 60, 90, 90, 100, 150, 150, 180, 200, 200, 220, 250, 250, 300, 330, 360, 390, 390, 450, 500, 600
        ],
        'Miete_3_Haus': [
            90, 180, 270, 270, 300, 450, 450, 500, 550, 550, 600, 700, 700, 750, 800, 850, 900, 900, 1000, 1100, 1400
        ],
        'Miete_4_Haus': [
            160, 320, 400, 400, 450, 625, 625, 700, 750, 750, 900, 875, 875, 925, 975, 1025, 1100, 1100, 1200, 1300,
            1700
        ],
        'Miete_Hotel': [
            250, 450, 550, 550, 600, 750, 750, 900, 950, 950, 1100, 1050, 1050, 1100, 1150, 1200, 1275, 1275, 1400,
            1500, 2000
        ],
        'Hauspreis': [
            50, 50, 50, 50, 50, 100, 100, 100, 100, 100, 100, 150, 150, 150, 150, 150, 200, 200, 200, 200, 200
        ],
        'Hypothek': [
            30, 30, 50, 50, 60, 70, 70, 80, 90, 90, 100, 110, 110, 120, 130, 140, 150, 150, 160, 175, 200
        ]
    }

    df = pd.DataFrame(sample_data)
    df.to_excel(filename, index=False)
    print(f"📄 Beispiel-Excel-Datei '{filename}' erstellt!")
    print("📝 Bearbeite die Datei und führe das Skript erneut aus.")
    print("🎨 Farben können als Hex-Code (#FF0000) oder Farbnamen (red) angegeben werden.")


# Hauptfunktion
if __name__ == "__main__":
    # Besitzkarten aus Excel erstellen
    create_property_cards_from_excel()
    print("📁 Die Besitzkarten findest du im Ordner 'property_cards'")
    print("🏠 Format: Hochformat mit vertikal zentriertem Kaufpreis")
    print("📐 Spalten sind vertikal ausgerichtet")