import tkinter as tk
from tkinter import filedialog, colorchooser, font
from PIL import Image, ImageTk, ImageOps
import emoji

class MemeGenerator:
    def __init__(self, root):
        # Initialisiere das Fenster und die grundlegenden Variablen
        self.root = root
        self.root.title("Meme Generator")
        
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.img = None  # Bild, das bearbeitet wird
        self.tk_img = None  # Tkinter-kompatibles Bild
        self.text_items = []  # Liste für Textobjekte
        self.current_text = None  # Aktuell ausgewählter Text
        self.x, self.y = 400, 300  # Startkoordinaten für Bild und Text
        
        # Liste zur Speicherung der Aktionen für "Rückgängig"
        self.history = []  # History für Bildänderungen
        self.undo_stack = []  # Stack für "Rückgängig"-Aktionen
        
        # Erstellen der Buttons im unteren Bereich des Fensters
        self.button_frame = tk.Frame(root)
        self.button_frame.pack()
        
        buttons = [
            ("Bild hochladen", self.upload_image),
            ("Text hinzufügen", self.add_text),
            ("Text bearbeiten", self.edit_text),
            ("Emoji hinzufügen", self.add_emoji),
            ("Rahmen hinzufügen", self.add_border),
            ("Bild verschieben", self.move_image),
            ("Bild zuschneiden", self.crop_image),
            ("Bild drehen", self.rotate_image),
            ("Bildgröße anpassen", self.resize_image),
            ("Rückgängig", self.undo)  # Hier ist der "Rückgängig"-Button
        ]
        
        # Button-Layout
        for i, (text, command) in enumerate(buttons):
            btn = tk.Button(self.button_frame, text=text, command=command)
            btn.grid(row=i // 4, column=i % 4, padx=5, pady=5)

    def upload_image(self):
        # Funktion, um ein Bild auszuwählen und zu laden
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.img = Image.open(file_path)  # Bild öffnen
            self.history.append(("upload", self.img))  # Speichern für Rückgängig
            self.display_image()  # Bild auf der Canvas anzeigen

    def display_image(self):
        # Konvertiere das Bild in ein Tkinter-kompatibles Format und zeige es an
        self.tk_img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(self.x, self.y, image=self.tk_img, anchor=tk.CENTER, tags="moveable_image")

    def add_text(self):
        # Funktion, um Text hinzuzufügen
        self.current_text = self.canvas.create_text(self.x, self.y, text="Text", fill="black", font=("Arial", 20), tags="editable")
        self.text_items.append(self.current_text)
        self.canvas.tag_bind(self.current_text, "<Button-1>", self.select_text)
    
    def select_text(self, event):
        # Funktion zum Auswählen und Bearbeiten des Textes
        self.current_text = event.widget.find_closest(event.x, event.y)[0]
        self.edit_text()

    def edit_text(self):
        # Funktion zum Bearbeiten des ausgewählten Textes
        if self.current_text:
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Text bearbeiten")
            entry = tk.Entry(edit_window)
            entry.pack()
            
            def update_text():
                new_text = entry.get()
                self.canvas.itemconfig(self.current_text, text=new_text)
                edit_window.destroy()
            
            tk.Button(edit_window, text="Speichern", command=update_text).pack()

    def add_emoji(self):
        # Funktion, um ein Emoji hinzuzufügen
        self.current_text = self.canvas.create_text(self.x, self.y + 50, text=emoji.emojize(":smile:"), font=("Arial", 20), tags="editable")
        self.text_items.append(self.current_text)

    def add_border(self):
        # Funktion, um einen Rahmen um das Bild hinzuzufügen
        if self.img:
            self.img = ImageOps.expand(self.img, border=10, fill="black")
            self.history.append(("border", self.img))  # Speichern für Rückgängig
            self.display_image()

    def move_image(self):
        # Funktion, um das Bild zu verschieben
        if self.img:
            self.canvas.tag_bind("moveable_image", "<Button-1>", self.start_move)
            self.canvas.tag_bind("moveable_image", "<B1-Motion>", self.move)
    
    def start_move(self, event):
        # Funktion zum Starten der Bewegung
        self.offset_x = event.x - self.x
        self.offset_y = event.y - self.y

    def move(self, event):
        # Funktion zum Verschieben des Bildes
        new_x = event.x - self.offset_x
        new_y = event.y - self.offset_y
        self.canvas.coords("moveable_image", new_x, new_y)
        self.x, self.y = new_x, new_y

    def crop_image(self):
        # Funktion, um das Bild zuzuschneiden
        if self.img:
            left = 100
            top = 100
            right = 500
            bottom = 400
            cropped_img = self.img.crop((left, top, right, bottom))
            self.img = cropped_img
            self.history.append(("crop", self.img))  # Speichern für Rückgängig
            self.display_image()

    def rotate_image(self):
        # Funktion, um das Bild zu drehen
        if self.img:
            self.img = self.img.rotate(90, expand=True)
            self.history.append(("rotate", self.img))  # Speichern für Rückgängig
            self.display_image()

    def resize_image(self):
        # Funktion, um die Bildgröße anzupassen
        if self.img:
            resize_window = tk.Toplevel(self.root)
            resize_window.title("Bildgröße anpassen")
            width_label = tk.Label(resize_window, text="Breite:")
            width_label.pack()
            width_entry = tk.Entry(resize_window)
            width_entry.pack()
            height_label = tk.Label(resize_window, text="Höhe:")
            height_label.pack()
            height_entry = tk.Entry(resize_window)
            height_entry.pack()
            
            def apply_resize():
                # Wende die neue Größe an
                try:
                    width = int(width_entry.get())
                    height = int(height_entry.get())
                    new_img = self.img.resize((width, height))
                    self.history.append(("resize", self.img))  # Speichern für Rückgängig
                    self.img = new_img
                    self.display_image()
                    resize_window.destroy()
                except ValueError:
                    print("Ungültige Größe eingegeben")

            tk.Button(resize_window, text="Größe anpassen", command=apply_resize).pack()

    def undo(self):
        # Rückgängig-Funktion, um die letzte Aktion rückgängig zu machen
        if self.history:
            last_action, last_state = self.history.pop()
            self.img = last_state  # Setze das Bild auf den letzten Zustand
            self.display_image()  # Bild erneut anzeigen
        else:
            print("Rückgängig-Funktion noch nicht implementiert")

if __name__ == "__main__":
    root = tk.Tk()  # Erstelle das Tkinter-Hauptfenster
    app = MemeGenerator(root)  # Erstelle das Meme-Generator-Objekt
    root.mainloop()  # Starte die Tkinter-Ereignisschleife
