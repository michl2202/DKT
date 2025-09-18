import cv2
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt


def build_price_string(number):
    return str(number) + "€"


class FixedPricePositionLabeler:
    def __init__(self, template_path):
        self.template_path = template_path
        self.image = cv2.imread(template_path)
        self.image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.height, self.width = self.image.shape[:2]
        
        y_oben_x_links = 0.045
        x_rechts_y_unten = 0.955

        template_str = "{template}"

        df = pd.read_excel('grundstuecke.xlsx')

        # Korrekte Reihenfolge
        self.all_properties = [
            # OBERE Reihe (braun/blau) - von links nach rechts
            {"name": df.Name[0], "price": build_price_string(df.Preis[0]), "x": 0.174, "y": y_oben_x_links, "rotation": 180},
            {"name": df.Name[1], "price": build_price_string(df.Preis[1]), "x": 0.34, "y": y_oben_x_links, "rotation": 180},
            {"name": df.Name[28], "price": build_price_string(df.Preis[28]), "x": 0.421, "y": y_oben_x_links, "rotation": 180},
            {"name": df.Name[22], "price": build_price_string(df.Preis[22]), "x": 0.502, "y": y_oben_x_links, "rotation": 180},
            {"name": df.Name[2], "price": build_price_string(df.Preis[2]), "x": 0.585, "y": y_oben_x_links, "rotation": 180},
            {"name": df.Name[3], "price": build_price_string(df.Preis[3]), "x": 0.747, "y": y_oben_x_links, "rotation": 180},
            {"name": df.Name[4], "price": build_price_string(df.Preis[4]), "x": 0.826, "y": y_oben_x_links, "rotation": 180},

            # RECHTE Seite - Seestraße oben → Berliner Straße unten
            {"name": df.Name[5], "price": build_price_string(df.Preis[5]), "x": x_rechts_y_unten, "y": 0.175, "rotation": 90},
            {"name": df.Name[26], "price": build_price_string(df.Preis[26]), "x": x_rechts_y_unten, "y": 0.259, "rotation": 90},
            {"name": df.Name[6], "price": build_price_string(df.Preis[6]), "x": x_rechts_y_unten, "y": 0.34, "rotation": 90},
            {"name": df.Name[7], "price": build_price_string(df.Preis[7]), "x": x_rechts_y_unten, "y": 0.422, "rotation": 90},
            {"name": df.Name[23], "price": build_price_string(df.Preis[23]), "x": x_rechts_y_unten, "y": 0.505, "rotation": 90},
            {"name": df.Name[8], "price": build_price_string(df.Preis[8]), "x": x_rechts_y_unten, "y": 0.586, "rotation": 90},
            {"name": df.Name[9], "price": build_price_string(df.Preis[9]), "x": x_rechts_y_unten, "y": 0.75, "rotation": 90},
            {"name": df.Name[10], "price": build_price_string(df.Preis[10]), "x": x_rechts_y_unten, "y": 0.83, "rotation": 90},

            # UNTERE Reihe (gelb/rot) - von links nach rechts
            {"name": df.Name[16], "price": build_price_string(df.Preis[16]), "x": 0.172, "y": x_rechts_y_unten, "rotation": 0},
            {"name": df.Name[27], "price": build_price_string(df.Preis[27]), "x": 0.25, "y": x_rechts_y_unten, "rotation": 0},
            {"name": df.Name[15], "price": build_price_string(df.Preis[15]), "x": 0.333, "y": x_rechts_y_unten, "rotation": 0},
            {"name": df.Name[14], "price": build_price_string(df.Preis[14]), "x": 0.414, "y": x_rechts_y_unten, "rotation": 0},
            {"name": df.Name[24], "price": build_price_string(df.Preis[24]), "x": 0.495, "y": x_rechts_y_unten, "rotation": 0},
            {"name": df.Name[13], "price": build_price_string(df.Preis[13]), "x": 0.578, "y": x_rechts_y_unten, "rotation": 0},
            {"name": df.Name[12], "price": build_price_string(df.Preis[12]), "x": 0.66, "y": x_rechts_y_unten, "rotation": 0},
            {"name": df.Name[11], "price": build_price_string(df.Preis[11]), "x": 0.823, "y": x_rechts_y_unten, "rotation": 0},

            # LINKE Seite - Schlossallee oben → Rathausplatz unten
            {"name": df.Name[21], "price": build_price_string(df.Preis[21]), "x": y_oben_x_links, "y": 0.173, "rotation": 270},
            {"name": df.Name[29], "price": build_price_string(df.Preis[29]), "x": y_oben_x_links, "y": 0.253, "rotation": 270},
            {"name": df.Name[20], "price": build_price_string(df.Preis[20]), "x": y_oben_x_links, "y": 0.334, "rotation": 270},
            {"name": df.Name[25], "price": build_price_string(df.Preis[25]), "x": y_oben_x_links, "y": 0.498, "rotation": 270},
            {"name": df.Name[19], "price": build_price_string(df.Preis[19]), "x": y_oben_x_links, "y": 0.58, "rotation": 270},
            {"name": df.Name[18], "price": build_price_string(df.Preis[18]), "x": y_oben_x_links, "y": 0.661, "rotation": 270},
            {"name": df.Name[17], "price": build_price_string(df.Preis[17]), "x": y_oben_x_links, "y": 0.826, "rotation": 270},
        ]

    def create_text_with_rotation(self, text, font, color, rotation=0):
        """Erstellt Text mit Rotation"""
        temp_size = 400
        temp_img = Image.new('RGBA', (temp_size, temp_size), (255, 255, 255, 0))
        temp_draw = ImageDraw.Draw(temp_img)

        temp_draw.text((temp_size // 2, temp_size // 2), text, fill=color, font=font, anchor="mm")
        bbox = temp_draw.textbbox((temp_size // 2, temp_size // 2), text, font=font, anchor="mm")

        padding = 5
        text_img = temp_img.crop((bbox[0] - padding, bbox[1] - padding, bbox[2] + padding, bbox[3] + padding))

        if rotation != 0:
            text_img = text_img.rotate(rotation, expand=True)

        return text_img

    def get_text_color(self, name):
        """Bestimmt Textfarbe"""
        return (0, 0, 0)

    def label_board_fixed_prices(self, output_path, font_size=22):
        """Beschriftet das Brett mit korrekten Preispositionen"""
        pil_image = Image.fromarray(self.image_rgb).convert('RGBA')

        # Font laden
        try:
            font_name = ImageFont.truetype("arial.ttf", font_size)
            font_price = ImageFont.truetype("arial.ttf", font_size - 6)
        except:
            try:
                font_name = ImageFont.truetype("/System/Library/Fonts/arial.ttf", font_size)
                font_price = ImageFont.truetype("/System/Library/Fonts/arial.ttf", font_size - 6)
            except:
                font_name = ImageFont.load_default()
                font_price = ImageFont.load_default()

        overlay = Image.new('RGBA', pil_image.size, (255, 255, 255, 0))

        for prop in self.all_properties:
            name = prop["name"]
            price = prop["price"]
            x_rel = prop["x"]
            y_rel = prop["y"]
            rotation = prop["rotation"]

            x = int(x_rel * self.width)
            y = int(y_rel * self.height)

            name_color = self.get_text_color(name)
            price_color = (0,0,0)

            name_img = self.create_text_with_rotation(name, font_name, name_color, rotation)
            price_img = self.create_text_with_rotation(price, font_price, price_color, rotation)

            # Korrekte Preisposition je nach Rotation
            if rotation == 0:  # UNTEN - Preis unterhalb
                name_x = x - name_img.width // 2
                name_y = y - name_img.height // 2 - 8
                price_x = x - price_img.width // 2
                price_y = name_y + name_img.height + 3

            elif rotation == 180:  # OBEN - Preis oberhalb (wegen Rotation)
                name_x = x - name_img.width // 2
                name_y = y - 8
                price_x = x - price_img.width // 2
                price_y = name_y - name_img.height - 3

            elif rotation == 90:  # LINKS - Preis rechts vom Namen
                name_x = x + 5
                name_y = y - name_img.height // 2
                price_x = name_x + name_img.width + 5
                price_y = y - price_img.height // 2

            elif rotation == 270:  # RECHTS - Preis links vom Namen
                name_x = x - name_img.width - 5
                name_y = y - name_img.height // 2
                price_x = name_x - price_img.width - 5
                price_y = y - price_img.height // 2

            padding = 2

            # Name mit Hintergrund
            name_bg = Image.new('RGBA',
                                (name_img.width + 2 * padding, name_img.height + 2 * padding),
                                (255, 255, 255, 230))
            overlay.paste(name_bg, (name_x - padding, name_y - padding))
            overlay.paste(name_img, (name_x, name_y), name_img)

            # Preis mit Hintergrund
            price_bg = Image.new('RGBA',
                                 (price_img.width + 2 * padding, price_img.height + 2 * padding),
                                 (255, 255, 255, 210))
            overlay.paste(price_bg, (price_x - padding, price_y - padding))
            overlay.paste(price_img, (price_x, price_y), price_img)

        final_image = Image.alpha_composite(pil_image, overlay)
        final_rgb = final_image.convert('RGB')

        final_array = np.array(final_rgb)
        cv2.imwrite(output_path, cv2.cvtColor(final_array, cv2.COLOR_RGB2BGR))

        return final_array


def create_fixed_price_position_board(template_path, output_path="dkt_beschriftet.png", font_size=24):
    """
    Erstellt DKT-Brett mit korrekten Preispositionen
    """
    try:
        labeler = FixedPricePositionLabeler(template_path)
        labeled_image = labeler.label_board_fixed_prices(output_path, font_size)

        plt.figure(figsize=(16, 16))
        plt.imshow(labeled_image)
        plt.title("DKT-Brett - Korrekte Preispositionen", fontsize=18)
        plt.axis('off')
        plt.tight_layout()
        plt.show()

        print(f"✅ DKT-Brett mit korrekten Preispositionen gespeichert als: {output_path}")
        print("🔧 Preispositionen:")
        print("   • UNTEN: Preis unterhalb des Namens ✓")
        print("   • OBEN: Preis oberhalb des Namens (wegen 180° Rotation)")
        print("   • LINKS: Preis rechts vom Namen")
        print("   • RECHTS: Preis links vom Namen")

        return labeled_image

    except Exception as e:
        print(f"❌ Fehler: {str(e)}")
        return None


# Hauptausführung
if __name__ == "__main__":
    template_path = "dkt_template.png"
    result = create_fixed_price_position_board(template_path, "dkt_beschriftet.png", 32)