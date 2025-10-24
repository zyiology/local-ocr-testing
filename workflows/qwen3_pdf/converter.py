import fitz  # PyMuPDF
from typing import List
from PIL import Image
from pathlib import Path


def pdf_to_images(
    pdf_path: str | Path, dpi: int = 300, first_page: int = 1, last_page: int = 1
) -> List[Image.Image]:
    """
    Convert PDF pages to PIL Images.

    Args:
        pdf_path: Path to the PDF file
        dpi: Resolution for conversion (default: 300)
        first_page: First page to convert (1-based)
        last_page: Last page to convert (1-based)

    Returns:
        List of PIL Images
    """

    if isinstance(pdf_path, Path):
        pdf_path = str(pdf_path)

    # Open the PDF
    doc = fitz.open(pdf_path)
    images = []

    # Convert DPI to zoom factor (PyMuPDF uses 72 DPI as base)
    zoom = dpi / 72
    mat = fitz.Matrix(zoom, zoom)

    # Adjust page numbers (PyMuPDF uses 0-based indexing)
    start_page = first_page - 1
    end_page = last_page  # last_page is inclusive in our API, so we don't subtract 1

    for page_num in range(start_page, min(end_page, len(doc))):
        page = doc[page_num]
        pix = page.get_pixmap(matrix=mat)

        # Convert pixmap to PIL Image
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        images.append(img)

    doc.close()
    return images


def save_images(
    output_folder: str | Path,
    images: list[Image.Image],
) -> list[Path]:
    """
    Given a set of images, saves them to a target folder. Images will be named image0.png, image1.png, etc.
    """
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)
    output_paths = []
    for i, img in enumerate(images):
        img.save(output_folder / f"image{i}.png")
        output_paths.append(output_folder / f"image{i}.png")
    return output_paths


def get_pdf_page_size(pdf_path: str | Path, page_num: int = 0) -> tuple[float, float]:
    """
    Get the size of a PDF page in points (1/72 inch).

    Args:
        pdf_path: Path to the PDF file
        page_num: Page number (0-based)

    Returns:
        Tuple of (width, height) in points
    """
    if isinstance(pdf_path, Path):
        pdf_path = str(pdf_path)

    doc = fitz.open(pdf_path)
    if page_num < len(doc):
        page = doc[page_num]
        rect = page.rect
        width, height = rect.width, rect.height
        doc.close()
        return width, height
    doc.close()
    return 0, 0
