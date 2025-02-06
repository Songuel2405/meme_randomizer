# Imports
import random
import os
import tkinter as tk
from PIL import Image, ImageTk

# Dictionary mit Ordnern mit Memes nach Kategorie
CATEGORIES = {
    "Tiere": 
    {"Hunde": "Praxisprojekt\memes\Tiere\Hunde",
     "Katzen": "Praxisprojekt\memes\Tiere\Katzen",
     "Wildtiere": "Praxisprojekt\memes\Tiere\Wildtiere",
     "Meerestiere":"Praxisprojekt\memes\Tiere\Meerestiere",},
    "Gaming": {"Minecraft":"Praxisprojekt\memes\Gaming\Minecraft",
               "Zelda":"Praxisprojekt\memes\Gaming\Zelda",
               },
    "IT": "memes\IT",
    "Deutsche Sprache": "memes\Deutsche Sprache"
}

# Bild laden
def show_random_meme(category):
    folder = CATEGORIES[category]   # der Ordner der die Memes der ausgewählten Kategorie enthält
    memes = os.listdir(folder)      # listet alle Dateien des gewählten Ordners auf
    random_meme = random.choice(memes)  # wählt zufällig ein Meme aus
    meme_path = os.path.join(folder, random_meme)   # kombiniert den Ordnerpfad mit dem ausgewählten Meme, um den vollständigen Dateipfad zu erhalten

    img = Image.open(meme_path) # öffnet das zufällig ausgewählte Meme
    img = img.resize((500,500)) # Größe anpassen 500x500 Pixel
    img = ImageTk.PhotoImage(img) # wandelt in ein Tkinter Format um

    meme_label.config(image=img)    # Tkinter Widget zur Bilddarstellung
    meme_label.image = img          # Referenz speichern

# GUI erstellen
root = tk.Tk()                  # erstellt das Hauptfenster der Tkinter-Anwendung
root.title("Meme Generator")    # gibt dem Fenster einen Titel

# Buttons für Themenbereiche
for category in CATEGORIES:     # iteriert über alle Kategorien
    btn = tk.Button(root, text=category, command=lambda c=category:show_random_meme(c)) # Button erstellen ; wenn der Button geklickt wird wird die Funktion show_random_meme aufgerufen
    btn.pack(side=tk.LEFT, padx=10, pady=5) # bettet den Button im Tkinter-Fenster ein, mit automatischer Skallierung des Buttons; Abstand zu anderen Objekten 10 Pixel horizontal und 5 Pixel vertikal

# Label für das Bild
meme_label = tk.Label(root) # Erstellung eines Label-Widgets im Hauptfenster, wo das Meme drauf plaziert wird
meme_label.pack()   # bettet das Label in der Benutzeroberfläche ein

root.mainloop() # startet die Tkinter-Anwendung, Fenster bleibt geöffnet und reagiert auf Benutzerinteraktionen
