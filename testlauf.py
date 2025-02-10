import tkinter as tk
from tkinter import filedialog, colorchooser, font
from PIL import Image, ImageTk, ImageOps
import emoji

class MemeGenerator:
    def __init__(self, root):
        # Initialisiere das Hauptfenster des Programms und grundlegende Variablen
        self.root = root
        self.root.title("Meme Generator")

        # Erstelle ein Canvas (Zeichenfläche), auf dem das Bild und Text angezeigt werden
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Variablen für das Bild, die Tkinter-kompatible Version und Textobjekte
        self.img = None  # Das Bild, das bearbeitet wird
        self.tk_img = None  # Tkinter-kompatibles Bild, das auf dem Canvas angezeigt wird
        self.text_items = []  # Liste zur Speicherung der Textobjekte, die hinzugefügt werden
        self.current_text = None  # Der aktuell ausgewählte Text
        self.x, self.y = 400, 300  # Startkoordinaten für das Bild und den Text auf dem Canvas

        # Erstellen der Buttons im unteren Bereich des Fensters
        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        # Button-Layout: Liste von Buttons mit jeweils einer Funktion, die aufgerufen wird
        buttons = [
            ("Bild hochladen", self.upload_image),
            ("Text hinzufügen", self.add_text),
            ("Text bearbeiten", self.edit_text),
            ("Emoji auswählen", self.show_emoji_selection),
            ("Rahmen hinzufügen", self.add_border),
            ("Bild verschieben", self.move_image),
            ("Bild zuschneiden", self.crop_image),
            ("Bild drehen", self.rotate_image),
            ("Bildgröße anpassen", self.resize_image),
            ("Speichern", self.save_image),
            ("Rückgängig", self.undo),  # Rückgängig-Button
            ("Schriftfarbe ändern", self.change_text_color),
            ("Hintergrundfarbe ändern", self.change_background_color)
        ]

        # Buttons im Layout anordnen (4 Buttons pro Zeile)
        for i, (text, command) in enumerate(buttons):
            btn = tk.Button(self.button_frame, text=text, command=command)
            btn.grid(row=i // 4, column=i % 4, padx=5, pady=5)

        # Emojis-Liste
        self.emoji_list = [
            ":grinning_face:", ":face_with_tears_of_joy:", ":red_heart:",
            ":dog_face:", ":sunglasses:", ":heart_eyes:", ":thinking_face:",
            ":cat_face:", ":unicorn_face:", ":skull:"
        ]
        self.emoji_selection_window = None  # Fenster für die Emoji-Auswahl

    def upload_image(self):
        # Funktion, um ein Bild vom Computer hochzuladen
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.img = Image.open(file_path)  # Das ausgewählte Bild öffnen
            self.display_image()  # Bild auf der Canvas anzeigen

    def display_image(self):
        # Funktion, um das Bild im Tkinter-kompatiblen Format anzuzeigen
        self.tk_img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(self.x, self.y, image=self.tk_img, anchor=tk.CENTER, tags="moveable_image")

    def add_text(self):
        # Funktion, um Text auf das Bild hinzuzufügen
        self.current_text = self.canvas.create_text(self.x, self.y, text="Text", fill="black", font=("Arial", 20), tags="editable")
        self.text_items.append(self.current_text)  # Speichern der Text-ID

        # Text auswählbar und verschiebbar machen
        self.canvas.tag_bind(self.current_text, "<Button-1>", self.select_text)  # Text auswählen
        self.canvas.tag_bind(self.current_text, "<B1-Motion>", self.move_text)  # Text mit der Maus bewegen

    def select_text(self, event):
        # Funktion zum Auswählen und Bearbeiten des Textes
        self.current_text = event.widget.find_closest(event.x, event.y)[0]  # Nähesten Text-Objekt finden
        self.edit_text()  # Text bearbeiten

    def move_text(self, event):
        # Funktion, um den Text mit der Maus zu verschieben
        new_x = event.x
        new_y = event.y
        self.canvas.coords(self.current_text, new_x, new_y)  # Textposition auf der Canvas aktualisieren
        self.x, self.y = new_x, new_y  # Koordinaten für den Text speichern

    def edit_text(self):
        # Funktion, um den ausgewählten Text zu bearbeiten
        if self.current_text:
            edit_window = tk.Toplevel(self.root)  # Neues Fenster für Textbearbeitung
            edit_window.title("Text bearbeiten")
            entry = tk.Entry(edit_window)  # Eingabefeld für neuen Text
            entry.pack()

            # Funktion zum Speichern des neuen Textes
            def update_text():
                new_text = entry.get()  # Neuer Text aus dem Eingabefeld
                self.canvas.itemconfig(self.current_text, text=new_text)  # Text auf Canvas aktualisieren
                edit_window.destroy()  # Fenster schließen

            tk.Button(edit_window, text="Speichern", command=update_text).pack()

    def change_text_color(self):
        # Funktion, um die Schriftfarbe zu ändern
        color = colorchooser.askcolor()[1]  # Farbwahl für die Schrift
        if color and self.current_text:
            self.canvas.itemconfig(self.current_text, fill=color)  # Textfarbe ändern

    def change_background_color(self):
        # Funktion, um die Hintergrundfarbe des Texts zu ändern
        color = colorchooser.askcolor()[1]  # Farbwahl für den Hintergrund
        if color and self.current_text:
            self.canvas.itemconfig(self.current_text, background=color)  # Hintergrundfarbe ändern

    def show_emoji_selection(self):
        # Funktion, um das Emoji-Auswahlfenster anzuzeigen
        if self.emoji_selection_window:
            return  # Wenn das Fenster bereits geöffnet ist, tue nichts

        # Neues Fenster zur Auswahl von Emojis
        self.emoji_selection_window = tk.Toplevel(self.root)
        self.emoji_selection_window.title("Wähle ein Emoji")
        for i, emoji_code in enumerate(self.emoji_list):
            emoji_label = tk.Label(self.emoji_selection_window, text=emoji.emojize(emoji_code), font=("Arial", 40), padx=10, pady=10)
            emoji_label.grid(row=i // 3, column=i % 3)

            # Emoji beim Klicken hinzufügen
            emoji_label.bind("<Button-1>", lambda e, emoji_code=emoji_code: self.add_emoji(emoji_code))

    def add_emoji(self, emoji_code):
        # Funktion, um das ausgewählte Emoji zum Bild hinzuzufügen
        emoji_text = emoji.emojize(emoji_code)  # Emoji-Text
        self.current_text = self.canvas.create_text(self.x, self.y + 50, text=emoji_text, font=("Arial", 40), tags="editable")
        self.text_items.append(self.current_text)  # Speichern der Emoji-ID

    def add_border(self):
        # Funktion, um einen schwarzen Rahmen um das Bild hinzuzufügen
        if self.img:
            self.img = ImageOps.expand(self.img, border=10, fill="black")  # Bild um 10 Pixel erweitern
            self.display_image()

    def move_image(self):
        # Funktion, um das Bild zu verschieben
        if self.img:
            self.canvas.tag_bind("moveable_image", "<Button-1>", self.start_move)
            self.canvas.tag_bind("moveable_image", "<B1-Motion>", self.move)

    def start_move(self, event):
        # Funktion zum Starten der Bewegung (Berechnung der Verschiebung)
        self.offset_x = event.x - self.x
        self.offset_y = event.y - self.y

    def move(self, event):
        # Funktion zum Verschieben des Bildes
        new_x = event.x - self.offset_x
        new_y = event.y - self.offset_y
        self.canvas.coords("moveable_image", new_x, new_y)  # Bild auf neuer Position setzen
        self.x, self.y = new_x, new_y  # Neue Koordinaten speichern

    def crop_image(self):
        # Funktion, um das Bild zuzuschneiden (Beispielwerte)
        if self.img:
            left = 100
            top = 100
            right = 500
            bottom = 400
            cropped_img = self.img.crop((left, top, right, bottom))  # Bild zuschneiden
            self.img = cropped_img  # Neues Bild setzen
            self.display_image()

    def rotate_image(self):
        # Funktion, um das Bild zu drehen (90 Grad)
        if self.img:
            self.img = self.img.rotate(90, expand=True)  # Bild um 90 Grad drehen
            self.display_image()

    def resize_image(self):
        # Funktion, um die Bildgröße anzupassen
        if self.img:
            resize_window = tk.Toplevel(self.root)  # Neues Fenster für die Größe
            resize_window.title("Bildgröße anpassen")
            width_label = tk.Label(resize_window, text="Breite:")
            width_label.pack()
            width_entry = tk.Entry(resize_window)
            width_entry.pack()
            height_label = tk.Label(resize_window, text="Höhe:")
            height_label.pack()
            height_entry = tk.Entry(resize_window)
            height_entry.pack()

            # Funktion, um die neue Größe anzuwenden
            def apply_resize():
                try:
                    width = int(width_entry.get())  # Neue Breite
                    height = int(height_entry.get())  # Neue Höhe
                    new_img = self.img.resize((width, height))  # Bildgröße ändern
                    self.img = new_img
                    self.display_image()  # Neues Bild anzeigen
                    resize_window.destroy()  # Fenster schließen
                except ValueError:
                    print("Ungültige Größe eingegeben")  # Fehlerbehandlung

            tk.Button(resize_window, text="Größe anpassen", command=apply_resize).pack()

    def save_image(self):
        # Speichern des bearbeiteten Bildes
        if self.img:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
            if file_path:
                self.img.save(file_path)  # Bild speichern

    def undo(self):
        # Rückgängig-Funktion, um die letzte Aktion rückgängig zu machen
        pass

# Starten der Anwendung
if __name__ == "__main__":
    root = tk.Tk()  # Erstelle das Tkinter-Hauptfenster
    app = MemeGenerator(root)  # Erstelle das Meme-Generator-Objekt
    root.mainloop()  # Starte die Tkinter-Ereignisschleife

