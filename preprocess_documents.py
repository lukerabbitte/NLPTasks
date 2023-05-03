import os
from pdf2image import convert_from_path
from PIL import Image, ImageFilter, ImageEnhance

# Define input and output directories
input_dir = "source_documents"
output_dir = "output_documents"

# Define preprocessing functions
def sharpen_image(img):
    # Sharpen image using ImageFilter kernel
    return img.filter(ImageFilter.Kernel((3, 3), (-1, -1, -1, -1, 9, -1, -1, -1, -1)))


def enhance_contrast(img):
    # Enhance contrast using ImageEnhance
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(1.5)


# Loop through all files in input directory
for filename in os.listdir(input_dir):

    # Check if file is a pdf
    if filename.endswith(".pdf"):

        # Convert pdf to list of JPEG images
        pdf_path = os.path.join(input_dir, filename)
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        img_format = "jpg"
        images = convert_from_path(pdf_path, 300, poppler_path=r'\your\bin\path\here')

        # Create subdirectory for pdf_name in output_dir
        pdf_dir = os.path.join(output_dir, pdf_name)
        os.makedirs(pdf_dir, exist_ok=True)

        # Iterate through JPEG images and apply preprocessing
        for i, image in enumerate(images):

            # Convert to greyscale and apply noise reduction
            page_img = image.convert("L").filter(ImageFilter.MedianFilter())

            # Apply preprocessing
            page_img = sharpen_image(page_img)
            page_img = enhance_contrast(page_img)

            page_img.save(f"{pdf_dir}/{pdf_name}_{i + 1}.{img_format}")

    elif filename.endswith(".jpg"):

        # Load image and apply preprocessing
        img_path = os.path.join(input_dir, filename)
        img_name = os.path.splitext(os.path.basename(img_path))[0]
        img_format = "jpg"
        image = Image.open(img_path)

        # Split image down the middle
        width, height = image.size
        left_half = image.crop((0, 0, width / 2, height))
        right_half = image.crop((width / 2, 0, width, height))

        # Apply preprocessing to each half
        left_half = left_half.convert("L").filter(ImageFilter.MedianFilter())
        left_half = sharpen_image(left_half)
        left_half = enhance_contrast(left_half)
        right_half = right_half.convert("L").filter(ImageFilter.MedianFilter())
        right_half = sharpen_image(right_half)
        right_half = enhance_contrast(right_half)

        # Save output as two separate images
        left_output_path = os.path.join(output_dir, f"{img_name}_first_half.{img_format}")
        right_output_path = os.path.join(output_dir, f"{img_name}_second_half.{img_format}")
        left_half.save(left_output_path)
        right_half.save(right_output_path)