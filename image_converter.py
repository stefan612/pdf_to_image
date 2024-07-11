import sys
from PIL import Image
import img2pdf
import subprocess
import os


def show_format_selection_dialog():
    try:
        # Create a Zenity list dialog to choose the format
        output_format = subprocess.check_output(
            ['zenity', '--list', '--title=Select Output Format', '--column=Format', 'PNG', 'JPG', 'PDF', 'ICO']).decode(
            'utf-8').strip()
        return output_format.lower()  # Return the selected format in lowercase
    except subprocess.CalledProcessError:
        return None


def convert_image(input_path, output_format):
    try:
        # Load image
        img = Image.open(input_path)
        print("Starte Konvertierung nach:", output_format)
        # Resize image to 64x64
        #img.thumbnail((64, 64), Image.LANCZOS)

        # Determine output path
        base = os.path.splitext(input_path)[0]
        output_path = f"{base}.{output_format.lower()}"
        print(output_path)
        # Convert and save image
        if output_format.lower() in ['jpg', 'jpeg']:
            if img.mode in ('RGBA', 'LA'):
                img = img.convert('RGB')
            img.save(output_path, 'JPEG')
            print(f"Image (JPG) saved successfully: {output_path}")
        elif output_format.lower() == 'png':
            img.save(output_path, 'PNG')
            print(f"Image (PNG) saved successfully: {output_path}")
        elif output_format.lower() == 'gif':
            img.save(output_path, 'GIF')
            print(f"Image (GIF) saved successfully: {output_path}")
        elif output_format.lower() == 'ico':
            img = img.resize((64, 64), Image.LANCZOS)
            img.save(output_path)
        elif output_format.lower() == 'pdf':
            temp_img_path = f"{base}_temp.jpg"
            if img.mode in ('RGBA', 'LA'):
                img = img.convert('RGB')
            img.save(temp_img_path, 'JPEG')
            with open(output_path, 'wb') as f:
                f.write(img2pdf.convert(temp_img_path))
            os.remove(temp_img_path)
            print(f"PDF saved successfully: {output_path}")
        else:
            print("Unsupported format!")
            return

        print(f"Converted {input_path} to {output_path}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    print(sys.argv[0])
    print(sys.argv[1])
    print(len(sys.argv))
    if len(sys.argv) != 2:
        print("Usage: python3 image_converter.py <input_image_path>")
    else:
        input_image_path = sys.argv[1]
        chosen_format = show_format_selection_dialog()
        print(chosen_format)
        if chosen_format:
            convert_image(input_image_path, chosen_format)
