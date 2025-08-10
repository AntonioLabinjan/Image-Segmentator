import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from rembg import remove
import io
import os

class ImageSegmentator:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Background Segmentator")

        self.frame = tk.Frame(root, bg="#2c2f33")
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.btn_load = tk.Button(self.frame, text="Load Image", command=self.load_image, bg="#7289da", fg="white", font=("Arial", 12, "bold"))
        self.btn_load.pack(pady=10)

        self.btn_segment = tk.Button(self.frame, text="Segment Image", command=self.segment_image, state="disabled", bg="#43b581", fg="white", font=("Arial", 12, "bold"))
        self.btn_segment.pack(pady=10)

        self.canvas = tk.Label(self.frame, bg="#23272a")
        self.canvas.pack(pady=10)

        self.btn_save = tk.Button(self.frame, text="Save Segmented Image", command=self.save_image, state="disabled", bg="#faa61a", fg="white", font=("Arial", 12, "bold"))
        self.btn_save.pack(pady=10)

        self.original_image = None
        self.segmented_image = None

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if not file_path:
            return
        self.original_image = Image.open(file_path).convert("RGBA")
        self.display_image(self.original_image)
        self.btn_segment.config(state="normal")
        self.btn_save.config(state="disabled")
        self.segmented_image = None

    def segment_image(self):
        if self.original_image is None:
            messagebox.showerror("Error", "No image loaded!")
            return
        img_bytes = io.BytesIO()
        self.original_image.save(img_bytes, format="PNG")
        segmented_bytes = remove(img_bytes.getvalue())
        self.segmented_image = Image.open(io.BytesIO(segmented_bytes)).convert("RGBA")
        self.display_image(self.segmented_image)
        self.btn_save.config(state="normal")

    def save_image(self):
        if self.segmented_image is None:
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.segmented_image.save(file_path)
            messagebox.showinfo("Success", f"Image saved at {os.path.basename(file_path)}")

    def display_image(self, img):
        max_size = (500, 500)
        img_resized = img.copy()
        img_resized.thumbnail(max_size, Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img_resized)
        self.canvas.config(image=img_tk)
        self.canvas.image = img_tk

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSegmentator(root)
    root.mainloop()
