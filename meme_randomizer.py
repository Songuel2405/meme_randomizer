# Imports
import random                                                   # für die zufällige Ausgabe der Memes
import os                                                       # Interaktion mit dem Betriebssystem, in diesem Fall Zugriff auf die Dateien der Memes
import tkinter as tk                                            # GUI Tool - graphical user interface
from tkinter import filedialog, colorchooser, font              # Dateien öffnen+speichern - Farbwähler - Schriftart
from tkinter import messagebox                                  # ermöglicht Pop-up Nachrichten
from PIL import Image, ImageTk, ImageOps, ImageDraw, ImageFont  # Bibliothek für Bildverarbeitung; Image=Klasse für Bilder öffnen, bearbeiten und speichern; ImageTk=Schnittstelle zu Tkinter; Draw=Zeichnen; Font=Schriftart
import emoji

# Dictionary mit Ordnern mit Memes nach Kategorie
CATEGORIES = {
    "Tiere": 
    {"Hunde": r"memes\Tiere\Hunde",
     "Katzen": r"memes\Tiere\Katzen",
     "Hund+Katze": r"memes\Tiere\Hund+Katze",
     "Katze+Maus": r"memes\Tiere\Katze+Maus",
     "Elefant": r"memes\Tiere\Elefant",
     "Maus": r"memes\Tiere\Maus",
     "Wildtiere": r"memes\Tiere\Wildtiere",
     "Vögel": r"memes\Tiere\Vögel"},
     "Emotionen": 
     {"Glücklich": r"memes\Emotionen\Glücklich",
      "Traurig": r"memes\Emotionen\Traurig",
      "Verwirrt": r"memes\Emotionen\Verwirrt"},
    "Gaming": r"memes\Gaming",
    "IT": r"memes\IT",
    "Deutsch": r"memes\Deutsch",
    "Kochen": r"memes\Kochen",
    "Musik": r"memes\Musik"}

# Meme-Randomizer starten
def start_meme_randomizer():
    start_window.configure(bg="grey25")                 # Randomizer Fenster in grau konfigurieren
    start_window.destroy()                              # Startfenster schließen

    global root                                         # global damit root auch außerhalb funktioniert
    root = tk.Tk()                                      # erstellt das Hauptfenster des Randomizers
    root.geometry("800x600")                            # Startgröße des Fensters
    root.title("Meme Randomizer")                       # gibt dem Fenster einen Titel
    root.configure(bg="grey25")                         # grauer Hintergrund

    # Kategorien anzeigen
    def show_categories():
        for widget in frame.winfo_children():
            widget.destroy()                                # entfernt die bestehenden Widgets im frame, doppelte Buttons vermeiden
        meme_label.config(image="", text="",bg="grey25")    # löscht Bild und Text im Label

        for category in CATEGORIES:                         # iteriert durch alle Kategorien
            if isinstance(CATEGORIES[category], dict):      # wenn eine Kategorie Unterkategorien hat, wird def show_subcategories aufgerufen
                btn = tk.Button(frame, text=category, font=("Alasassy Caps", 12), fg="white", bg="grey25", command=lambda c=category: show_subcategories(c))
            else:                                           # ansonsten wird def show_random_meme aufgerufen
                btn = tk.Button(frame, text=category, font=("Alasassy Caps", 12), fg="white", bg="grey25", command=lambda c=category: show_random_meme(c, None))
            btn.pack(side=tk.LEFT, padx=10, pady=5)         # fügt die Buttons ins frame ein
    
    # Unterkategorien anzeigen
    def show_subcategories(category):
        for widget in frame.winfo_children():           
            widget.destroy()                                                                                # entfernt bestehende Buttons
        for subcategory in CATEGORIES[category]:                                                            # iteriert durch die Unterkategorien
            btn = tk.Button(frame, text=subcategory, font=("Alasassy Caps", 12), fg= "white", bg="gray25",  # Buttons für die Unterkategorien erstellen, 
            command=lambda c=category, s=subcategory: show_random_meme(c, s))                               # die bei Klick ein random meme aufrufen
            btn.pack(side=tk.LEFT, padx=10, pady=5)                                                         # bettet den Button für die Unterkategorien ein

        back_btn = tk.Button(frame, text="← Zurück", font=("Alasassy Caps", 12), fg="white", bg="grey25", command= show_categories)  # definiert den Zurück-Button
        back_btn.pack(side=tk.LEFT, padx=10, pady=5)   # bettet den Button ein, mit automatischer Skallierung des Buttons; Abstand zu anderen Objekten 10 Pixel horizontal und 5 Pixel vertikal
    
    # Frame-Widget mit Scroll-Leiste erstellen
    canvas = tk.Canvas(root)                                                # "Leinwand" erstellen
    canvas.configure(bg="grey25")                                           # in grau
    scrollbar = tk.Scrollbar(root,orient="vertical", command=canvas.yview)  # erstellt eine vertikale Scroll-Leiste im Hauptfenster
    frame = tk.Frame(canvas, background= "grey25")                          # erstellt ein Frame-Widget im Hauptfenster mit grauem Hintergrund, das als Container für die Buttons dient
    frame.pack()                                                            # bettet das Frame in das Canvas ein
    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))  # konfiguriert die Scroll-Leiste
    canvas.create_window((0, 0), window=frame, anchor="nw")                 # Position (nord-west) des Frames als Fenster im Canvas
    canvas.configure(yscrollcommand=scrollbar.set)                          # verknüpft Scrollbar mit Canvas
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)                    # platziert Canvas und lässt ihn den verfügbaren Platz einnehmen
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)                                # bettet die Scroll-Leiste rechts ein

    # Suchfeld hinzufügen
    search_var = tk.StringVar()                                                                         # Variable für den Suchbegriff
    search_entry = tk.Entry(root, textvariable=search_var, font=("Alasassy Caps", 12))                  # Eingabefeld im Hauptfenster root erstellen und Ergebnis in Variable speichern
    search_entry.pack(pady=10)  # Abstand zur Leserlichkeit                                             # und einbetten
    search_button = tk.Button(root, text="🔍 Suchen", font=("Alasassy Caps", 12),                      
                          fg="white", bg="grey25",  command=lambda: search_memes(search_var.get()))     # Suchbutton erstellen der def search_memes aufruft
    search_button.pack()                                                                                # und einbetten
    
    # Suchfunktion
    def search_memes(query):
        query = query.lower()   # alles klein schreiben um Suche zu vereinfachen
        results = []            # Leere Liste für die Dateipfade der Suchergebnisse

        for category, value in CATEGORIES.items():                              # iteriert durch alle Kategorien
            if isinstance(value, dict):                                         # falls es Unterkategorien gibt
                for subcategory, path in value.items():                         # iteriert durch alle Unterkategorien
                    if os.path.exists(path):                                    # prüft ob der Ordner existiert
                        for filename in os.listdir(path):                       # geht alle Dateien im Ordner durch und sucht nach Übereinstimmungen
                            if query in filename.lower():                       # falls der Dateiname den Suchbegriff enthält
                                results.append(os.path.join(path, filename))    # wird der Pfad der Liste results hinzugefügt
            else:                                                               
                    if os.path.exists(value):                                   # falls es keine Unterkategorie gibt
                        for filename in os.listdir(value):                      # geht alle Dateien im Ordner durch
                            if query in filename.lower():                       # falls der Dateiname den Suchbegriff enthält
                                results.append(os.path.join(value, filename))   # wird der Pfad der Liste results hinzugefügt

            if not results:                                                     # falls nichts gefunden wurde
                meme_label.config(text="Keine Ergebnisse gefunden",             # wird diese Meldung angezeigt
                font=("Alasassy Caps", 12), fg="white", image="")                
                return
    
        for widget in frame.winfo_children():                                   
            widget.destroy()                                                    # löscht alle bisherigen Buttons im frame, damit nur die neuen Suchergebnisse angezeigt werden

        for meme_path in results:                                               # iteriert durch alle gefundenen Ergebnisse
            btn = tk.Button(frame, text=os.path.basename(meme_path),
            font=("Alasassy Caps", 12), fg="white", bg="grey25",                # und erstellt einen Button der dann bei Klick das jeweilige Meme anzeigt
            command=lambda path=meme_path: show_meme(path))
            btn.pack()                                                          # bettet die Buttons ins Fenster ein
       
        back_btn = tk.Button(frame, text="← Zurück", font=("Alasassy Caps", 12),
        fg="white", bg="grey25", command= show_categories)                      # definiert den Zurück-Button
        back_btn.pack(side=tk.LEFT, padx=10, pady=5)                            # bettet den Button ein

    # Meme öffnen für die Suchfunktion
    def show_meme(meme_path):
        if not os.path.exists(meme_path):                                       # falls die Datei nicht mehr exestiert
            meme_label.config(text="Fehler: Datei nicht gefunden",              # wird dieser Fehler angezeigt
            font=("Alasassy Caps", 12), fg="white", image="")    
            return
    
        img = Image.open(meme_path)     # öffnet das Bild
        img = img.resize((500,500))     # passt die Größe an
        img = ImageTk.PhotoImage(img)   # wandelt in Tkinter-Format um

        meme_label.config(image=img)    # Tkinter Widget zur Bildverarbeitung
        meme_label.image = img          # Referenz speichern

    # Funktion die ein Meme zufällig auswählt
    def show_random_meme(category, subcategory=None):    
        if subcategory:
            folder = CATEGORIES[category][subcategory]   # der Ordner der die Memes der ausgewählten Kategorie enthält
        else:
            folder = CATEGORIES[category]

        memes = os.listdir(folder)                      # listet alle Dateien des gewählten Ordners auf
    
        if not memes:                                   # falls kein Meme gefunden wurde 
            meme_label.config(text="Keine Memes gefunden", font=("Alasassy Caps", 12), fg="white", image="")
            return
    
        random_meme = random.choice(memes)              # wählt zufällig ein Meme aus
        meme_path = os.path.join(folder, random_meme)   # kombiniert den Ordnerpfad mit dem ausgewählten Meme, um den vollständigen Dateipfad zu erhalten

        img = Image.open(meme_path)                     # öffnet das zufällig ausgewählte Meme
        img = img.resize((500,500))                     # Größe anpassen 500x500 Pixel
        img = ImageTk.PhotoImage(img)                   # wandelt in ein Tkinter Format um

        meme_label.config(image=img)                    # Tkinter Widget zur Bilddarstellung
        meme_label.image = img                          # Referenz speichern

        for widget in frame.winfo_children():
            widget.destroy()                            # vorherige Buttons entfernen

        back_btn = tk.Button(frame, text="← Zurück", font=("Alasassy Caps", 12), 
        fg="white", bg="grey25", command= show_categories)  # definiert den Zurück-Button
        back_btn.pack(side=tk.LEFT, padx=10, pady=5)   # bettet den Button im Tkinter-Fenster ein, mit automatischer Skallierung des Buttons; Abstand zu anderen Objekten 10 Pixel horizontal und 5 Pixel vertikal

    back_btn = tk.Button(frame, text="← Zurück", font=("Alasassy Caps", 12), 
    fg="white", bg="grey25", command=show_categories)   # erstellt den Zurück-Button
    back_btn.pack()
    # Label für das Bild
    meme_label = tk.Label(root)         # Erstellung eines Label-Widgets im Hauptfenster, wo das Meme drauf plaziert wird
    meme_label.pack()                   # bettet das Label in der Benutzeroberfläche ein

    show_categories()

    root.mainloop()                     # startet die Tkinter-Anwendung, Fenster bleibt geöffnet und reagiert auf Benutzerinteraktionen

# Startfenster erstellen
start_window = tk.Tk()                  # Startfenster erstellen
start_window.title("Meme Master")       # Name des Fensters
start_window.geometry("400x300")        # Größe
start_window.configure(bg="grey25")     # Hintergrund
label = tk.Label(start_window, text="Meme Master",font=("Goudy Stout", 14),fg="white", bg= "grey25")    # Überschrift
label.pack(pady=20)                                                                                     # einbetten
btn_randomizer = tk.Button(start_window, text="Meme Randomizer", font=("Alasassy Caps", 12), fg="white", bg="grey25",command=start_meme_randomizer) # Button Meme Randomizer erstellen
btn_randomizer.pack(pady=10)                                                                                                                        # einbetten

class MemeGenerator:
    def __init__(self, root):
        # Initialisiere das Hauptfenster des Programms und grundlegende Variablen
        self.root = root
        self.root.title("Meme Generator")
        self.root.configure(bg="grey25")

        # Erstelle ein Canvas (Zeichenfläche), auf dem das Bild und Text angezeigt werden
        self.canvas = tk.Canvas(root, width=800, height=600, bg="grey40")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Variablen für das Bild, die Tkinter-kompatible Version und Textobjekte
        self.img = None  # Das Bild, das bearbeitet wird
        self.tk_img = None  # Tkinter-kompatibles Bild, das auf dem Canvas angezeigt wird
        self.text_items = []  # Liste zur Speicherung der Textobjekte, die hinzugefügt werden
        self.current_text = None  # Der aktuell ausgewählte Text
        self.x, self.y = 400, 300  # Startkoordinaten für das Bild und den Text auf dem Canvas

        # Erstellen der Buttons im unteren Bereich des Fensters
        self.button_frame = tk.Frame(root, bg="grey25")
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
            ("Hintergrundfarbe ändern", self.change_background_color)
        ]

        # Buttons im Layout anordnen (4 Buttons pro Zeile)
        for i, (text, command) in enumerate(buttons):
            btn = tk.Button(self.button_frame, text=text, font=("Alasassy Caps", 12), fg="white", bg="grey25", command=command)
            btn.grid(row=i // 4, column=i % 4, padx=5, pady=5)

        # Emojis-Liste
        self.emoji_list = [
            ":grinning_face:", ":face_with_tears_of_joy:", ":red_heart:",
            ":dog_face:", ":sunglasses:", ":heart_eyes:", ":thinking_face:",
            ":cat_face:", ":unicorn_face:", ":skull:"
        ]
        self.emoji_selection_window = None  # Fenster für die Emoji-Auswahl
        self.history = [] # speichert die Zwischenschritte der Bildbearbeitung

    def upload_image(self):
        # Funktion, um ein Bild vom Computer hochzuladen
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.save_state()
            self.img = Image.open(file_path)  # Das ausgewählte Bild öffnen
            self.display_image()  # Bild auf der Canvas anzeigen

    def display_image(self):
        # Funktion, um das Bild im Tkinter-kompatiblen Format anzuzeigen
        if self.img:
            self.tk_img = ImageTk.PhotoImage(self.img)
            self.canvas.delete("all")                   # vorherige Elemente löschen
            self.canvas.create_image(self.x, self.y, image=self.tk_img, anchor=tk.CENTER, tags="moveable_image")
            self.canvas.update_idletasks()

    def add_text(self):
        # Funktion, um Text auf das Bild hinzuzufügen
        if not hasattr(self, "img"):
            print("Kein Bild geladen!")
            return
        text_window = tk.Toplevel(self.root)    # Fenster für Texteingabe
        text_window.title("Text hinzufügen")

        tk.Label(text_window, text="Text eingeben:").pack()
        text_entry = tk.Entry(text_window)
        text_entry.pack()

        tk.Label(text_window, text="Schriftgröße:").pack()
        size_entry = tk.Entry(text_window)
        size_entry.pack()

        def choose_color(button):
            color = colorchooser.askcolor()[1]
            if color:
                button.config(bg=color)
                button.color = color

        tk.Label(text_window, text="Textfarbe wählen:").pack()
        color_button = tk.Button(text_window, text="Farbe wählen", command=lambda:choose_color(color_button))
        color_button.pack()

        def apply_text():
            text = text_entry.get()
            size = size_entry.get()
            color = getattr(color_button, "color","white")

            if not text:
                print("Kein Text eingegeben!")
                return

            try:
                size = int(size)
            except ValueError:
                print("Ungültige Schriftgröße!")
                return

            self.current_text = self.canvas.create_text(
                self.x, self.y, text=text, font=("Arial",size), fill=color, tags="editable")
            self.text_items.append(self.current_text)
            self.save_state()   # Speichern für Undo func

            draw = ImageDraw.Draw(self.img) # zeichnet direkt aufs Bild

            try:
                font = ImageFont.truetype("arial.ttf", size)
            except:
                font = ImageFont.load_default()
            
            bbox = draw.textbbox((0,0), text, font=font)
            text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
            img_width, img_height = self.img.size
            x = (img_width - text_width) // 2
            y = img_height - text_height - 20   # Abstand zum unteren Rand

            draw.text((x,y), text, font=font, fill=color)

            self.display_image()
            self.img.save("meme_with_text.jpg")
            text_window.destroy()
            
        tk.Button(text_window, text="Text hinzufügen", command=apply_text).pack()

        if hasattr(self, "current_text") and self.current_text:
        # Text auswählbar und verschiebbar machen
            self.canvas.tag_bind(self.current_text, "<Button-1>", lambda event: self.select_text(event))  # Text auswählen
            self.canvas.tag_bind(self.current_text, "<B1-Motion>", lambda event: self.move_text(event))  # Text mit der Maus bewegen

    def select_text(self, event):
        # Funktion zum Auswählen und Bearbeiten des Textes
        self.current_text = event.canvas.find_closest(event.x, event.y)[0]  # Nähesten Text-Objekt finden
        self.edit_text()  # Text bearbeiten

    def move_text(self, event):
        # Funktion, um den Text mit der Maus zu verschieben
        new_x = event.x
        new_y = event.y
        self.canvas.coords(self.current_text, new_x, new_y)  # Textposition auf der Canvas aktualisieren

    def edit_text(self):
        # Funktion, um den ausgewählten Text zu bearbeiten
        if self.current_text:
            edit_window = tk.Toplevel(self.root)  # Neues Fenster für Textbearbeitung
            edit_window.title("Text bearbeiten")
            current_text = self.canvas.itemcget(self.current_text, "text")
            entry = tk.Entry(edit_window)  # Eingabefeld für neuen Text
            entry.pack()
            entry.insert(0, current_text)

            # Funktion zum Speichern des neuen Textes
            def update_text():
                new_text = entry.get()  # Neuer Text aus dem Eingabefeld
                if new_text:
                    self.canvas.itemconfig(self.current_text, text=new_text)  # Text auf Canvas aktualisieren
                edit_window.destroy()  # Fenster schließen

            tk.Button(edit_window, text="Speichern",font=("Alasassy Caps", 12), fg="white", bg="grey25", command=update_text).pack()

    def change_background_color(self):
        # Funktion, um die Hintergrundfarbe des Texts zu ändern
        self.save_state()
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
        self.save_state()
        emoji_text = emoji.emojize(emoji_code)  # Emoji-Text
        self.current_text = self.canvas.create_text(self.x, self.y + 50, text=emoji_text, font=("Arial", 40), tags="editable")
        self.text_items.append(self.current_text)  # Speichern der Emoji-ID

    def add_border(self):
        # Funktion, um einen schwarzen Rahmen um das Bild hinzuzufügen
        self.save_state()
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
        self.save_state()
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
        self.save_state()
        if self.img:
            self.img = self.img.rotate(90, expand=True)  # Bild um 90 Grad drehen
            self.display_image()

    def resize_image(self):
        # Funktion, um die Bildgröße anzupassen
        if self.img:
            resize_window = tk.Toplevel(self.root)  # Neues Fenster für die Größe
            resize_window.configure(bg="grey25")
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

            tk.Button(resize_window, text="Größe anpassen", font=("Alasassy Caps", 12), fg="white", bg="grey25", command=apply_resize).pack()

    def save_image(self):
        # Speichern des bearbeiteten Bildes
        if not hasattr(self, "img"):
            print("Kein Meme vorhanden!")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if file_path:
            self.img.save(file_path)  # Bild speichern
            print("Meme gespeichert")

    def save_state(self):
        if self.img:
            self.history.append(self.img.copy())
    # Rückgängig-Funktion, um die letzte Aktion rückgängig zu machen
    def undo(self):
        if self.history:
            self.img = self.history.pop()
            self.display_image()
    
def start_meme_generator():
    start_window.destroy()      # Startfenster schließen
    root = tk.Tk()              # Erstelle das Hauptfenster des Generators
    root.configure(bg="grey25") # in grau
    app = MemeGenerator(root)   # Erstelle das Meme-Generator-Objekt
    root.mainloop()

btn_generator = tk.Button(start_window, text="Meme Generator", font=("Alasassy Caps", 12),fg="white", bg="grey25", command=start_meme_generator)    # Button erstellen für Meme Generator
btn_generator.pack(pady=10)                                                                                                                         # einbetten

start_window.mainloop()