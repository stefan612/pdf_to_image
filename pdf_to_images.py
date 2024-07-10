#!/usr/bin/env python3

import os
import sys
from pdf2image import convert_from_path

def pdf_to_images(pdf_path, dpi=300):
    # Get the directory and filename without extension
    pdf_dir = os.path.dirname(pdf_path)
    pdf_filename = os.path.splitext(os.path.basename(pdf_path))[0]
    
    # Create output folder named after the PDF
    output_folder = os.path.join(pdf_dir, pdf_filename)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Convert PDF to a list of images
    images = convert_from_path(pdf_path, dpi=dpi)
    
    # Save each image to the output folder
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f"page_{i + 1}.png")
        image.save(image_path, "PNG")
        print(f"Saved {image_path}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: convert_pdf_to_images.py <pdf_path>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    pdf_to_images(pdf_path)

