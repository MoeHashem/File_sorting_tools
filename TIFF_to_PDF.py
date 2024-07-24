import os
from PIL import Image #pip install pillow
from pypdf import PdfWriter, PdfReader #pip install pypdf
from tqdm import tqdm #pip install tqdm

# Increase the maximum image size limit to handle large images
Image.MAX_IMAGE_PIXELS = None

def process_tiff_files_in_subfolder(subfolder_path):
    tiff_images = []

    # Collect all TIFF images in the subfolder
    for file in os.listdir(subfolder_path):
        if file.lower().endswith('.tiff') or file.lower().endswith('.tif'):
            file_path = os.path.join(subfolder_path, file)
            try:
                # Open the image and rotate it counter-clockwise
                img = Image.open(file_path)
                rotated_img = img.rotate(90, expand=True)
                tiff_images.append(rotated_img)
            except Image.DecompressionBombError:
                print(f"Skipped {file_path}: Image too large.")
            except Exception as e:
                print(f"Skipped {file_path}: {e}")

    return tiff_images

def save_images_as_pdf(images, output_pdf_path):
    pdf_writer = PdfWriter()

    for image in tqdm(images, desc="Processing images", unit="image"):
        # Convert image to RGB mode (required for saving as PDF)
        img_rgb = image.convert('RGB')
        # Save the image temporarily as a PDF
        img_temp_path = 'temp_image.pdf'
        img_rgb.save(img_temp_path)

        # Read the temporary PDF and add its pages to the PdfWriter
        with open(img_temp_path, 'rb') as img_temp_file:
            pdf_reader = PdfReader(img_temp_file)
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)

        # Remove the temporary file
        os.remove(img_temp_path)

    # Write all collected pages to the final PDF
    with open(output_pdf_path, 'wb') as output_pdf_file:
        pdf_writer.write(output_pdf_file)

def main():
    base_folder_path = r"C:\Users\Mohammed.Hashem\Desktop\TPH02011SCANS"  # Replace with the path to your folder

    # Walk through all subdirectories in the base folder
    for root, dirs, files in os.walk(base_folder_path):
        for subfolder in tqdm(dirs, desc="Processing subfolders", unit="subfolder"):
            subfolder_path = os.path.join(root, subfolder)
            tiff_images = process_tiff_files_in_subfolder(subfolder_path)
            if tiff_images:
                # Extract the portion of the subfolder name after the hyphen and up to the first space
                subfolder_name_parts = subfolder.split(' - ')
                output_pdf_name = f"{subfolder_name_parts[1]}_COMBINED.pdf"
                

                output_pdf_path = os.path.join(subfolder_path, output_pdf_name)
                save_images_as_pdf(tiff_images, output_pdf_path)
                print(f"PDF created successfully at {output_pdf_path}")

if __name__ == "__main__":
    main()
