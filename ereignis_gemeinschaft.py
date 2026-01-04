from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import pandas as pd


def create_dkt_cards_from_excel(excel_file="ereignis_gemeinschaft.xlsx", output_folder="output/dkt_cards"):
    """
    Erstellt dkt-Karten aus Excel-Datei mit abgerundeten äußeren Ecken

    Args:
        excel_file (str): Pfad zur Excel-Datei
        output_folder (str): Ordner für die generierten Bilder
    """

    try:
        # Excel-Datei einlesen
        df = pd.read_excel(excel_file)
        print(f"📊 Excel-Datei geladen: {len(df)} Karten gefunden")

        # Überprüfen ob die erforderlichen Spalten vorhanden sind
        required_columns = ['Text', 'Aktion']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            print(f"❌ Fehlende Spalten in der Excel-Datei: {missing_columns}")
            print(f"📋 Verfügbare Spalten: {list(df.columns)}")
            return

        # Kartenabmessungen im Querformat
        card_width = 1050
        card_height = 675

        # Ausgabeordner erstellen
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Für jede Zeile in der Excel-Datei eine Karte erstellen
        for index, row in df.iterrows():
            text = str(row['Text']) if pd.notna(row['Text']) else ""
            action = str(row['Aktion']) if pd.notna(row['Aktion']) else ""

            # Leere Zeilen überspringen
            if not text and not action:
                continue

            # Neues Bild mit transparentem Hintergrund erstellen
            img = Image.new('RGBA', (card_width, card_height), (0, 0, 0, 0))

            # Abgerundete Karte als Basis erstellen
            card_base = create_rounded_card_base(card_width, card_height)
            img.paste(card_base, (0, 0))

            draw = ImageDraw.Draw(img)

            # Inneren Rahmen zeichnen
            border_width = 12
            border_margin = 40
            inner_corner_radius = 35

            # Innerer Rahmen (abgerundete Ecken)
            draw.rounded_rectangle(
                [border_margin, border_margin,
                 card_width - border_margin, card_height - border_margin],
                radius=inner_corner_radius,
                outline='black',
                width=border_width
            )

            # Text hinzufügen
            add_centered_text_from_excel(draw, text, action, card_width, card_height)

            # In RGB konvertieren für Speicherung
            final_img = Image.new('RGB', (card_width, card_height), 'white')
            final_img.paste(img, (0, 0), img)

            # Bild speichern
            filename = f"dkt_card_{index + 1:02d}.png"
            filepath = os.path.join(output_folder, filename)
            final_img.save(filepath, dpi=(300, 300))
            print(f"Karte {index + 1} erstellt: {filepath}")

        print(f"\n✅ {len(df)} dkt-Karten aus Excel erfolgreich erstellt!")

    except FileNotFoundError:
        print(f"❌ Excel-Datei '{excel_file}' nicht gefunden!")
        print("📝 Stelle sicher, dass die Datei im gleichen Ordner liegt.")
        create_sample_excel(excel_file)
    except Exception as e:
        print(f"❌ Fehler beim Lesen der Excel-Datei: {e}")


def create_rounded_card_base(width, height):
    """
    Erstellt eine abgerundete Kartenbasis mit weißem Hintergrund
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


def add_centered_text_from_excel(draw, description, action, card_width, card_height):
    """
    Fügt zentrierten Text aus Excel-Daten mit einheitlichen Schriftgrößen hinzu
    """

    # Einheitliche Schriftgrößen definieren
    try:
        font_text = ImageFont.truetype("arial.ttf", 46)  # Text (Beschreibung)
        font_action = ImageFont.truetype("arial.ttf", 42)  # Aktion (etwas kleiner)
    except:
        font_text = ImageFont.load_default()
        font_action = ImageFont.load_default()

    # Feste Zeichen pro Zeile für einheitliches Layout
    text_chars_per_line = 42  # Für Beschreibungstext
    action_chars_per_line = 35  # Für Aktionstext

    # Beschreibungstext in Zeilen aufteilen
    desc_lines = textwrap.fill(description, width=text_chars_per_line).split('\n') if description else []

    # Aktionstext in Zeilen aufteilen
    action_lines = textwrap.fill(action, width=action_chars_per_line).split('\n') if action else []

    # Zeilenhöhen berechnen
    desc_line_height = font_text.getbbox("Ag")[3] - font_text.getbbox("Ag")[1] + 8
    action_line_height = font_action.getbbox("Ag")[3] - font_action.getbbox("Ag")[1] + 8

    # Gesamthöhe berechnen
    total_desc_height = len(desc_lines) * desc_line_height
    total_action_height = len(action_lines) * action_line_height
    separator_space = 25 if desc_lines and action_lines else 0  # Etwas mehr Abstand

    total_height = total_desc_height + separator_space + total_action_height

    # Startposition für vertikale Zentrierung
    start_y = (card_height - total_height) // 2

    # Beschreibungstext zeichnen (größere Schrift)
    current_y = start_y
    for line in desc_lines:
        bbox = draw.textbbox((0, 0), line, font=font_text)
        text_width = bbox[2] - bbox[0]
        x = (card_width - text_width) // 2
        draw.text((x, current_y), line, fill='black', font=font_text)
        current_y += desc_line_height

    # Abstand zwischen Beschreibung und Aktion
    current_y += separator_space

    # Aktionstext zeichnen (kleinere Schrift)
    for line in action_lines:
        bbox = draw.textbbox((0, 0), line, font=font_action)
        text_width = bbox[2] - bbox[0]
        x = (card_width - text_width) // 2
        draw.text((x, current_y), line, fill='black', font=font_action)
        current_y += action_line_height


def create_sample_excel(filename="ereignis_gemeinschaft.xlsx"):
    """
    Erstellt eine Beispiel-Excel-Datei mit der korrekten Struktur
    """

    sample_data = {
        'Text': [
            'Du gehst direkt ins Gefängnis. Gehe nicht über Los.',
            'Rücke vor bis zur Schlossallee. Wenn du über Los kommst,',
            'Du hast im Lotto gewonnen!',
            'Zahle deine Versicherungsprämie.',
            'Du kommst aus dem Gefängnis frei.',
            'Ein entfernter Verwandter ist verstorben.',
            'Du warst beim Arzt und musst die Rechnung bezahlen.',
            'Du gehst spazieren und findest eine Abkürzung.',
            'Das Finanzamt hat einen Fehler in deiner Steuererklärung gefunden.',
            'Heute ist dein Geburtstag und alle gratulieren dir.',
            'Du hast bei einem Schönheitswettbewerb teilgenommen.',
            'Die Bank hat einen Rechenfehler gemacht.',
            'Du hilfst einer alten Dame über die Straße.',
            'Deine Hausratversicherung zahlt nach einem kleinen Schaden.',
            'Du musst zur Nachschulung für deinen Führerschein.'
        ],
        'Aktion': [
            'Ziehe nicht 4000€ ein.',
            'ziehe 4000€ ein.',
            'Erhalte 2000€ aus der Bank.',
            'Zahle 1000€ an die Bank.',
            'Gehe zurück zum Startfeld.',
            'Du erbst 2000€.',
            'Zahle 1000€.',
            'Rücke vor zur nächsten Straße.',
            'Zahle 4000€.',
            'Erhalte von jedem Mitspieler 200€.',
            'Erhalte 100€ für den zweiten Platz.',
            'Bankfehler zu deinen Gunsten - erhalte 2000€.',
            'Gehe vor bis Los und ziehe 4000€ ein.',
            'Erhalte 1500€.',
            'Zahle 500€ Gebühren.'
        ]
    }

    df = pd.DataFrame(sample_data)
    df.to_excel(filename, index=False)
    print(f"📄 Beispiel-Excel-Datei '{filename}' erstellt!")
    print("📝 Bearbeite die Datei und führe das Skript erneut aus.")


# Hauptfunktion
if __name__ == "__main__":
    # Karten aus Excel erstellen
    create_dkt_cards_from_excel()
    print("📁 Die Karten findest du im Ordner 'dkt_cards'")
    print("🎯 Format: Querformat mit einheitlichen Schriftgrößen")