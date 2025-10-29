from pathlib import Path
import argparse

from converter import pdf_to_images, get_pdf_page_size, save_images
from providers import LocalProvider, AlibabaCloudProvider, VLLMProvider
from config import (
    DEFAULT_MODEL,
    USE_MOE,
    DEFAULT_PDF_FOLDER,
    DEFAULT_OUTPUT_FOLDER,
    TARGET_LONGEST_SIDE,
    DEFAULT_PROMPT,
    DEFAULT_PROVIDER,
    ALIBABA_MODEL,
    ALIBABA_REGION,
    ALIBABA_MAX_TOKENS,
    ALIBABA_TEMPERATURE,
    VLLM_MODEL,
    VLLM_HOST,
    VLLM_PORT,
    VLLM_MAX_TOKENS,
    VLLM_TEMPERATURE,
)


def main(
    pdf_folder_path: Path,
    output_folder: Path = Path("output/"),
    provider: str = "local",
):
    """Main workflow for batch processing PDFs with OCR.
    
    Args:
        pdf_folder_path: Path to folder containing PDF files
        output_folder: Path to output folder for results
        provider: OCR provider to use ("local", "alibaba_cloud", or "vllm")
    """
    # Initialize the appropriate provider
    if provider == "local":
        provider_model = LocalProvider(model_name=DEFAULT_MODEL, use_moe=USE_MOE)
    elif provider == "alibaba_cloud":
        provider_model = AlibabaCloudProvider(
            model_name=ALIBABA_MODEL,
            region=ALIBABA_REGION,
            max_tokens=ALIBABA_MAX_TOKENS,
            temperature=ALIBABA_TEMPERATURE,
        )
    elif provider == "vllm":
        provider_model = VLLMProvider(
            model_name=VLLM_MODEL,
            host=VLLM_HOST,
            port=VLLM_PORT,
            max_tokens=VLLM_MAX_TOKENS,
            temperature=VLLM_TEMPERATURE,
        )
    else:
        raise ValueError(f"Unknown provider: {provider}")

    # Convert all PDFs to images
    image_paths = []
    for pdf_path in pdf_folder_path.rglob("*.pdf"):
        # Get PDF page size
        page_size = get_pdf_page_size(pdf_path)

        # Define DPI such that longest side matches target resolution
        dpi = int(TARGET_LONGEST_SIDE / max(page_size) * 72)

        # Convert PDF to images
        images = pdf_to_images(pdf_path, dpi=dpi)

        # Save images - preserve directory structure
        relative_path = pdf_path.relative_to(pdf_folder_path)
        pdf_output_folder = output_folder / relative_path.parent / pdf_path.stem
        image_paths.extend(save_images(pdf_output_folder, images))

    # Process each image with the provider
    for image_path in image_paths:
        output_text = provider_model.process_image(str(image_path), DEFAULT_PROMPT)
        # Save the text output alongside the image
        text_path = image_path.with_suffix(".txt")
        text_path.write_text(output_text, encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Batch process PDFs with Qwen3-VL OCR models"
    )
    parser.add_argument(
        "--pdf-folder",
        type=Path,
        default=DEFAULT_PDF_FOLDER,
        help=f"Path to folder containing PDF files (default: {DEFAULT_PDF_FOLDER})",
    )
    parser.add_argument(
        "--output-folder",
        type=Path,
        default=DEFAULT_OUTPUT_FOLDER,
        help=f"Path to output folder for results (default: {DEFAULT_OUTPUT_FOLDER})",
    )
    parser.add_argument(
        "--provider",
        type=str,
        default=DEFAULT_PROVIDER,
        choices=["local", "alibaba_cloud", "vllm"],
        help=f"OCR provider to use (default: {DEFAULT_PROVIDER})",
    )

    args = parser.parse_args()

    # Resolve paths to absolute
    pdf_folder = args.pdf_folder.resolve()
    output_folder = args.output_folder.resolve()
    provider = args.provider  # This is already a string, don't resolve it

    # Validate PDF folder exists
    if not pdf_folder.exists():
        print(f"Error: PDF folder not found: {pdf_folder}")
        print("Please create the folder or specify a different path with --pdf-folder")
        exit(1)

    if not any(pdf_folder.rglob("*.pdf")):
        print(f"Warning: No PDF files found in {pdf_folder}")
        exit(1)

    # Create output folder if it doesn't exist
    output_folder.mkdir(parents=True, exist_ok=True)

    print(f"PDF folder: {pdf_folder}")
    print(f"Output folder: {output_folder}")
    print(f"Provider: {provider}")
    print(f"Found {len(list(pdf_folder.rglob('*.pdf')))} PDF file(s)")
    print()

    main(pdf_folder, output_folder, provider=provider)
