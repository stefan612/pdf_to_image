import sys
from PIL import Image
import img2pdf
import subprocess
import os

def show_format_selection_dialog():
    try:
        output_format = subprocess.check_output([
            'zenity', '--list', '--title=Select Output Format', '--column=Format', 'PNG', 'JPG', 'PDF', 'ICO'
        ]).decode('utf-8').strip()
        return output_format.lower()
    except subprocess.CalledProcessError:
        return None

def show_file_selection_dialog():
    try:
        file_paths = subprocess.check_output([
            'zenity', '--file-selection', '--multiple', '--separator=|', '--title=Select Image Files'
        ]).decode('utf-8').strip()
        return file_paths.split('|') if file_paths else []
    except subprocess.CalledProcessError:
        return []

def convert_image(input_path, output_format):
    try:
        img = Image.open(input_path)
        print(f"Starting conversion of {input_path} to {output_format}")
        base = os.path.splitext(input_path)[0]
        output_path = f"{base}.{output_format}"
        
        if output_format in ['jpg', 'jpeg']:
            if img.mode in ('RGBA', 'LA'):
                img = img.convert('RGB')
            img.save(output_path, 'JPEG')
        elif output_format == 'png':
            img.save(output_path, 'PNG')
        elif output_format == 'gif':
            img.save(output_path, 'GIF')
        elif output_format == 'ico':
            img = img.resize((64, 64), Image.LANCZOS)
            img.save(output_path, format='ICO')
        elif output_format == 'pdf':
            temp_img_path = f"{base}_temp.jpg"
            if img.mode in ('RGBA', 'LA'):
                img = img.convert('RGB')
            img.save(temp_img_path, 'JPEG')
            with open(output_path, 'wb') as f:
                f.write(img2pdf.convert(temp_img_path))
            os.remove(temp_img_path)
        else:
            print(f"Unsupported format: {output_format}")
            return
        
        print(f"Converted {input_path} to {output_path}")
    except Exception as e:
        print(f"Error converting {input_path}: {e}")

if __name__ == "__main__":
    # Use files from command-line args (from Nemo) instead of opening a selection dialog
    file_paths = sys.argv[1:]  # Get file paths from command line arguments
    
    if not file_paths:
        file_paths = show_file_selection_dialog()  # Fallback to manual selection if none provided

    if not file_paths:
        print("No files selected.")
        sys.exit(1)

    chosen_format = show_format_selection_dialog()
    if chosen_format:
        for path in file_paths:
            convert_image(path.strip(), chosen_format)
