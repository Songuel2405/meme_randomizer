import tkinter as tk
from tkinter import filedialog, colorchooser, font
from PIL import Image, ImageTk, ImageDraw, ImageOps
import emoji

class MemeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Meme Generator")
        
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.img = None
        self.tk_img = None
        self.text_items = []
        self.current_text = None
        self.x, self.y = 400, 300  # Starting position for the image
        
        self.guidelines = []  # For the visual guidelines (waterwaage)
        
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
            ("Rückgängig", self.undo)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = tk.Button(self.button_frame, text=text, command=command)
            btn.grid(row=i // 4, column=i % 4, padx=5, pady=5)

        # Bind mouse motion for adding guidelines
        self.canvas.bind("<Motion>", self.update_guidelines)

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.img = Image.open(file_path)
            self.display_image()

    def display_image(self):
        self.tk_img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(self.x, self.y, image=self.tk_img, anchor=tk.CENTER, tags="moveable_image")
    
    def add_text(self):
        self.current_text = self.canvas.create_text(self.x, self.y, text="Text", fill="black", font=("Arial", 20), tags="editable")
        self.text_items.append(self.current_text)
        self.canvas.tag_bind(self.current_text, "<Button-1>", self.select_text)
    
    def select_text(self, event):
        self.current_text = event.widget.find_closest(event.x, event.y)[0]
        self.edit_text()

    def edit_text(self):
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
        self.current_text = self.canvas.create_text(self.x, self.y + 50, text=emoji.emojize(":smile:"), font=("Arial", 20), tags="editable")
        self.text_items.append(self.current_text)

    def add_border(self):
        if self.img:
            self.img = ImageOps.expand(self.img, border=10, fill="black")
            self.display_image()

    def move_image(self):
        if self.img:
            self.canvas.tag_bind("moveable_image", "<Button-1>", self.start_move)
            self.canvas.tag_bind("moveable_image", "<B1-Motion>", self.move)
    
    def start_move(self, event):
        self.offset_x = event.x - self.x
        self.offset_y = event.y - self.y

    def move(self, event):
        new_x = event.x - self.offset_x
        new_y = event.y - self.offset_y
        self.canvas.coords("moveable_image", new_x, new_y)
        self.x, self.y = new_x, new_y

    def crop_image(self):
        if self.img:
            left = 100
            top = 100
            right = 500
            bottom = 400
            cropped_img = self.img.crop((left, top, right, bottom))
            self.img = cropped_img
            self.display_image()

    def rotate_image(self):
        if self.img:
            self.img = self.img.rotate(90, expand=True)
            self.display_image()

    def resize_image(self):
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
                width = int(width_entry.get())
                height = int(height_entry.get())
                self.img = self.img.resize((width, height))
                self.display_image()
                resize_window.destroy()

            tk.Button(resize_window, text="Größe anpassen", command=apply_resize).pack()

    def undo(self):
        if self.text_items:
            last_text = self.text_items.pop()
            self.canvas.delete(last_text)

    def update_guidelines(self, event):
        # Remove old guidelines
        for guideline in self.guidelines:
            self.canvas.delete(guideline)
        self.guidelines.clear()

        # Draw horizontal and vertical guidelines at the mouse position
        self.guidelines.append(self.canvas.create_line(0, event.y, 800, event.y, fill="gray", dash=(4, 2)))
        self.guidelines.append(self.canvas.create_line(event.x, 0, event.x, 600, fill="gray", dash=(4, 2)))
        
if __name__ == "__main__":
    root = tk.Tk()
    app = MemeGenerator(root)
    root.mainloop()

