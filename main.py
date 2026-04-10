import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk

class UpscalingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Applicazione Upscaling Immagini")
        
        self.original_image = None
        self.upscaled_image = None
        self.original_path = None
        
        # Frame principale
        main_frame = tk.Frame(root)
        main_frame.pack(padx=10, pady=10)
        
        # Frame per i controlli
        control_frame = tk.Frame(main_frame)
        control_frame.pack(pady=10)
        
        # Pulsante Carica Immagine
        self.load_btn = tk.Button(control_frame, text="Carica Immagine", command=self.load_image)
        self.load_btn.grid(row=0, column=0, padx=5, pady=5)
        
        # Menu a tendina per il fattore di upscaling
        tk.Label(control_frame, text="Fattore:").grid(row=0, column=1, padx=5, pady=5)
        self.scale_var = tk.StringVar(value="2x")
        self.scale_menu = tk.OptionMenu(control_frame, self.scale_var, "2x", "4x")
        self.scale_menu.grid(row=0, column=2, padx=5, pady=5)
        
        # Pulsante Applica Upscaling
        self.upscale_btn = tk.Button(control_frame, text="Applica Upscaling", command=self.apply_upscaling)
        self.upscale_btn.grid(row=0, column=3, padx=5, pady=5)
        
        # Pulsante Salva Immagine
        self.save_btn = tk.Button(control_frame, text="Salva Immagine", command=self.save_image)
        self.save_btn.grid(row=0, column=4, padx=5, pady=5)
        
        # Frame per le anteprime
        preview_frame = tk.Frame(main_frame)
        preview_frame.pack(pady=10)
        
        # Anteprima immagine originale
        tk.Label(preview_frame, text="Originale").grid(row=0, column=0, padx=10)
        self.original_label = tk.Label(preview_frame)
        self.original_label.grid(row=1, column=0, padx=10, pady=10)
        
        # Anteprima immagine modificata
        tk.Label(preview_frame, text="Upscaled").grid(row=0, column=1, padx=10)
        self.upscaled_label = tk.Label(preview_frame)
        self.upscaled_label.grid(row=1, column=1, padx=10, pady=10)
        
    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Seleziona un'immagine",
            filetypes=[("File immagine", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        
        if file_path:
            self.original_path = file_path
            self.original_image = cv2.imread(file_path)
            
            if self.original_image is not None:
                # Converti da BGR a RGB per PIL
                rgb_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(rgb_image)
                
                # Ridimensiona per l'anteprima se necessario
                max_size = (400, 400)
                pil_image.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                self.original_photo = ImageTk.PhotoImage(pil_image)
                self.original_label.config(image=self.original_photo)
                
                # Reset dell'immagine upscaled
                self.upscaled_image = None
                self.upscaled_label.config(image="")
                
                messagebox.showinfo("Successo", "Immagine caricata con successo!")
            else:
                messagebox.showerror("Errore", "Impossibile caricare l'immagine.")
    
    def apply_upscaling(self):
        if self.original_image is None:
            messagebox.showwarning("Attenzione", "Carica prima un'immagine!")
            return
        
        # Ottieni il fattore di scala
        scale_factor = int(self.scale_var.get().replace("x", ""))
        
        # Calcola le nuove dimensioni
        height, width = self.original_image.shape[:2]
        new_width = width * scale_factor
        new_height = height * scale_factor
        
        # Applica l'upscaling con interpolazione LANCZOS4
        self.upscaled_image = cv2.resize(
            self.original_image, 
            (new_width, new_height), 
            interpolation=cv2.INTER_LANCZOS4
        )
        
        # Mostra l'anteprima dell'immagine upscaled
        rgb_upscaled = cv2.cvtColor(self.upscaled_image, cv2.COLOR_BGR2RGB)
        pil_upscaled = Image.fromarray(rgb_upscaled)
        
        # Ridimensiona per l'anteprima se necessario
        max_size = (400, 400)
        pil_upscaled.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        self.upscaled_photo = ImageTk.PhotoImage(pil_upscaled)
        self.upscaled_label.config(image=self.upscaled_photo)
        
        messagebox.showinfo("Completato", f"Upscaling {scale_factor}x applicato con successo!")
    
    def save_image(self):
        if self.upscaled_image is None:
            messagebox.showwarning("Attenzione", "Applica prima l'upscaling!")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Salva immagine upscaled",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp")]
        )
        
        if file_path:
            success = cv2.imwrite(file_path, self.upscaled_image)
            if success:
                messagebox.showinfo("Successo", "Immagine salvata con successo!")
            else:
                messagebox.showerror("Errore", "Impossibile salvare l'immagine.")

if __name__ == "__main__":
    root = tk.Tk()
    app = UpscalingApp(root)
    root.mainloop()
