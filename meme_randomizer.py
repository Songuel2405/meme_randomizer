# Imports
import random                       # für die zufällige Ausgabe der Memes
import os                           # Interaktion mit dem Betriebssystem, in diesem Fall Zugriff auf die Dateien der Memes
import tkinter as tk                # GUI für die grafische Benutzeroberfläche
from PIL import Image, ImageTk      # Bibliothek für Bildverarbeitung; Image=Klasse für Bilder öffnen, bearbeiten und speichern; ImageTk=Schnittstelle zu Tkinter

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
     "Meerestiere":r"memes\Tiere\Meerestiere",
     "Vögel": r"memes\Tiere\Vögel"},
     "Emotionen": 
     {"Glücklich": r"memes\Emotionen\Glücklich",
      "Traurig": r"memes\Emotionen\Traurig",
      "Verwirrt": r"memes\Emotionen\Verwirrt"},
    "Gaming": r"memes\Gaming",
    "IT": r"memes\IT",
    "Deutsch": r"memes\Deutsch"}

# GUI erstellen
root = tk.Tk()                      # erstellt das Hauptfenster der Tkinter-Anwendung
root.title("Meme Randomizer")       # gibt dem Fenster einen Titel

# Suchfeld zur GUI hinzufügen
search_var = tk.StringVar()                             # Variable für den Suchbegriff

search_entry = tk.Entry(root, textvariable=search_var)  # Eingabefeld im Hauptfenster root erstellen und Ergebnis in Variable speichern
search_entry.pack()                                     # und einbetten

search_button = tk.Button(root, text="🔍 Suchen", command=lambda: search_memes(search_var.get()))   # Suchbutton erstellen
search_button.pack()                                                                                 # und einbetten

# Funktion die ein Meme zufällig auswählt
def show_random_meme(category, subcategory=None):     
    if subcategory:
        folder = CATEGORIES[category][subcategory]   # der Ordner der die Memes der ausgewählten Kategorie enthält
    else:
        folder = CATEGORIES[category]

    memes = os.listdir(folder)                      # listet alle Dateien des gewählten Ordners auf
    
    if not memes:                                   # falls kein Meme gefunden wurde 
        meme_label.config(text="Keine Memes gefunden", image="")
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

    back_btn = tk.Button(frame, text="← Zurück", command= show_categories)  # definiert den Zurück-Button
    back_btn.pack(side=tk.LEFT, padx=10, pady=5)   # bettet den Button im Tkinter-Fenster ein, mit automatischer Skallierung des Buttons; Abstand zu anderen Objekten 10 Pixel horizontal und 5 Pixel vertikal

# Funktion die alle Kategorien umfasst
def show_categories():
    for widget in frame.winfo_children():   # gibt eine Liste aller Widgets
        widget.destroy()                    # entfernt alle bisherigen Elemente

    meme_label.config(image="",text="")     # Meme Label leeren, falls vorher ein Bild angezeigt wurde wird es hier entfernt

    for category in CATEGORIES:                                                                         # iteriert durch die Hauptkategorien
        if isinstance(CATEGORIES[category],dict):
            btn = tk.Button(frame, text=category, command=lambda c=category: show_subcategories(c))     # mit Klick auf eine Hauptkategorie wird die Unterkategorie aufgerufen, falls vorhanden
        else:
            btn = tk.Button(frame, text=category, command=lambda c=category:show_random_meme(c, None))  # ansonsten wird die Funktion show_random_meme ausgeführt
        
        btn.pack(side=tk.LEFT, padx=10, pady=5)                                                         # bettet den Button im Hauptfenster ein

# Funktion die nur die Unterkategorien umfasst
def show_subcategories(category):
    for widget in frame.winfo_children():   # gibt eine Liste aller Widgets
        widget.destroy()                    # entfernt alle bisherigen Elemente

    for subcategory in CATEGORIES[category]:                                                                        # iteriert durch alle Unterkategorien der gewählten Hauptkategorie
        btn = tk.Button(frame, text=subcategory, command=lambda c=category, s=subcategory: show_random_meme(c, s))  # definiert die Buttons der Unterkategorien und führt dan show_random_meme aus
        btn.pack(side=tk.LEFT, padx=10, pady=5)                                                                     # bettet den Button im Hauptfenster ein

    back_btn = tk.Button(frame, text="← Zurück", command= show_categories)  # definiert wieder einen Zurück-Button
    back_btn.pack(side=tk.LEFT, padx=10, pady=5)                            # bettet den Button ein

# Suchfunktion
def search_memes(query):
    query = query.lower()   # alles klein schreiben um Suche zu vereinfachen
    results = []            # Leere Liste für die Dateipfade der Suchergebnisse

    for category, value in CATEGORIES.items():                              # iteriert durch alle Kategorien und Unterkategorien
        if isinstance(value, dict):                                         # falls es Unterkategorien gibt (value=dict)
            for subcategory, path in value.items():                         # iteriert durch alle Bilder der Unterkategorie
                if os.path.exists(path):                                    # prüft ob der Ordner existiert
                    for filename in os.listdir(path):                       # geht alle Dateien im Ordner durch und sucht nach Übereinstimmungen
                        if query in filename.lower():                       # falls der Dateiname den Suchbegriff enthält
                            results.append(os.path.join(path, filename))    # wird der Pfad der Liste results hinzugefügt
        else:                                                               # falls es keine Unterkategorie gibt
                if os.path.exists(value):
                    for filename in os.listdir(value):
                        if query in filename.lower():
                            results.append(os.path.join(value, filename))
    
    if not results:                                                         # falls nichts gefunden wurde
        meme_label.config(text="Keine Ergebnisse gefunden", image="")
        return
    
    for widget in frame.winfo_children():                                   # löscht alle bisherigen Buttons im frame, damit nur die neuen Suchergebnisse angezeigt werden
        widget.destroy()

    for meme_path in results:                                               # iteriert durch alle gefundenen Ergebnisse
        btn = tk.Button(frame, text=os.path.basename(meme_path),            # und erstellt einen Button der dann bei Klick das jeweilige Meme anzeigt
                        command=lambda path=meme_path: show_meme(path))
        btn.pack()                                                          # bettet die Buttons ins Fenster ein
    
    back_btn = tk.Button(frame, text="← Zurück", command=show_categories)   # erstellt den Zurück-Button
    back_btn.pack()

# Meme öffnen für die Suchfunktion
def show_meme(meme_path):
    if not os.path.exists(meme_path): # falls die Datei nicht mehr exestiert
        meme_label.config(text="Fehler: Datei nicht gefunden", image="")
        return
    
    img = Image.open(meme_path)     # öffnet das Bild
    img = img.resize((500,500))     # passt die Größe an
    img = ImageTk.PhotoImage(img)   # wandelt in Tkinter-Format um

    meme_label.config(image=img)    # Tkinter Widget zur Bildverarbeitung
    meme_label.image = img          # Referenz speichern

# Frame-Widget erstellen
frame = tk.Frame(root)              # erstellt ein Frame-Widget im Hauptfenster, das als Container für die Buttons dient
frame.pack()                        # bettet das Frame in das Fenster ein

# Label für das Bild
meme_label = tk.Label(root)         # Erstellung eines Label-Widgets im Hauptfenster, wo das Meme drauf plaziert wird
meme_label.pack()                   # bettet das Label in der Benutzeroberfläche ein

show_categories()

root.mainloop()                     # startet die Tkinter-Anwendung, Fenster bleibt geöffnet und reagiert auf Benutzerinteraktionen