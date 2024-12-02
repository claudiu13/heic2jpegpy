import os
import webbrowser
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pillow_heif import register_heif_opener

# Register HEIC opener with Pillow
register_heif_opener()

def heic_to_jpeg(heic_path, jpeg_path):
    try:
        # Open HEIC image
        image = Image.open(heic_path)

        # Save the image as JPEG
        image.save(jpeg_path, "JPEG")
    
    except Exception as e:
        print(f"Failed to convert {heic_path}: {e}")

def batch_convert_heic_to_jpeg(input_directory, output_directory, progress, total_files):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Get all HEIC files in the input directory
    files = [f for f in os.listdir(input_directory) if f.lower().endswith(".heic")]
    
    for index, filename in enumerate(files, 1):
        heic_path = os.path.join(input_directory, filename)
        jpeg_filename = os.path.splitext(filename)[0] + ".jpeg"
        jpeg_path = os.path.join(output_directory, jpeg_filename)

        heic_to_jpeg(heic_path, jpeg_path)

        # Update progress bar
        progress['value'] = (index / total_files) * 100
        progress.update_idletasks()

    messagebox.showinfo("Conversion Complete", "All HEIC files have been converted to JPEG.")

# Function to open the desiredweb.com link in a browser
def open_desiredweb_link(event):
    webbrowser.open_new("https://desiredweb.com/")

# GUI Application
class HEICtoJPEGConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HEIC to JPEG Converter")
        self.root.geometry("400x400")  # Adjusted height for the additional link

        # Input Directory Selection
        self.input_label = tk.Label(root, text="Input Directory (HEIC files):")
        self.input_label.pack(pady=5)
        self.input_dir_button = tk.Button(root, text="Select Input Directory", command=self.select_input_dir)
        self.input_dir_button.pack(pady=5)
        self.input_dir_path = tk.StringVar()
        self.input_dir_display = tk.Label(root, textvariable=self.input_dir_path)
        self.input_dir_display.pack(pady=5)

        # Output Directory Selection
        self.output_label = tk.Label(root, text="Output Directory (JPEG files):")
        self.output_label.pack(pady=5)
        self.output_dir_button = tk.Button(root, text="Select Output Directory", command=self.select_output_dir)
        self.output_dir_button.pack(pady=5)
        self.output_dir_path = tk.StringVar()
        self.output_dir_display = tk.Label(root, textvariable=self.output_dir_path)
        self.output_dir_display.pack(pady=5)

        # Progress Bar
        self.progress_label = tk.Label(root, text="Conversion Progress:")
        self.progress_label.pack(pady=5)
        self.progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=5)

        # Convert Button
        self.convert_button = tk.Button(root, text="Convert", command=self.convert_files)
        self.convert_button.pack(pady=20)

        # Made by desiredweb.com Label with Link
        self.made_by_label = tk.Label(root, text="Made by desiredweb.com", fg="blue", cursor="hand2")
        self.made_by_label.pack(pady=5)

        # Bind the label to open the link in the browser
        self.made_by_label.bind("<Button-1>", open_desiredweb_link)

    def select_input_dir(self):
        input_dir = filedialog.askdirectory()
        self.input_dir_path.set(input_dir)

    def select_output_dir(self):
        output_dir = filedialog.askdirectory()
        self.output_dir_path.set(output_dir)

    def convert_files(self):
        input_dir = self.input_dir_path.get()
        output_dir = self.output_dir_path.get()

        if input_dir and output_dir:
            # Count the number of HEIC files to be converted
            total_files = len([f for f in os.listdir(input_dir) if f.lower().endswith(".heic")])
            
            if total_files == 0:
                messagebox.showwarning("No Files", "No HEIC files found in the selected input directory.")
                return

            # Reset progress bar
            self.progress['value'] = 0
            self.progress.update_idletasks()

            # Call the batch conversion function with the progress bar
            batch_convert_heic_to_jpeg(input_dir, output_dir, self.progress, total_files)
        else:
            messagebox.showwarning("Missing Information", "Please select both input and output directories.")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = HEICtoJPEGConverterApp(root)
    root.mainloop()