from transformers import (
    AutoProcessor,
    Qwen3VLForConditionalGeneration,
    Qwen3VLMoeForConditionalGeneration,
)
from converter import pdf_to_images, get_pdf_page_size, save_images
from pathlib import Path
import importlib.util
import argparse

QWEN_MODEL = "Qwen/Qwen3-VL-30B-A3B-Instruct"
MOE = True  # Set to True if using the MoE model


def check_flash_attention_available() -> bool:
    """Check if Flash Attention 2 is available on the system.

    Returns:
        bool: True if flash_attn is installed and available, False otherwise.
    """
    return importlib.util.find_spec("flash_attn") is not None


def main(pdf_folder_path: Path, output_folder: Path = Path("output/")):
    # Check if Flash Attention 2 is available
    use_flash_attn = check_flash_attention_available()
    if use_flash_attn:
        print("Flash Attention 2 detected - using optimized attention implementation")
        attn_implementation = "flash_attention_2"
    else:
        print("Flash Attention 2 not available - using default 'eager' implementation")
        attn_implementation = "eager"

    # Load the model on the available device(s)
    model_kwargs = {
        "dtype": "auto",
        "device_map": "auto",
        "attn_implementation": attn_implementation,
    }

    if MOE:
        model = Qwen3VLMoeForConditionalGeneration.from_pretrained(
            QWEN_MODEL,
            **model_kwargs,  # type: ignore
        )
    else:
        model = Qwen3VLForConditionalGeneration.from_pretrained(
            QWEN_MODEL,
            **model_kwargs,  # type: ignore
        )

    print("model loaded")

    processor = AutoProcessor.from_pretrained(QWEN_MODEL)

    print("processor loaded")

    image_paths = []
    for pdf_path in pdf_folder_path.rglob("*.pdf"):
        # Get PDF page size
        page_size = get_pdf_page_size(pdf_path)

        # Define DPI such that longest side is 1800 pixels
        target_longest_side = 1800
        dpi = int(target_longest_side / max(page_size) * 72)

        # Convert PDF to images
        images = pdf_to_images(pdf_path, dpi=dpi)

        # Save images - preserve directory structure
        relative_path = pdf_path.relative_to(pdf_folder_path)
        pdf_output_folder = output_folder / relative_path.parent / pdf_path.stem
        image_paths.extend(save_images(pdf_output_folder, images))

    for image_path in image_paths:
        output_text = qwen_process_image(str(image_path), model, processor)
        # Save the text output alongside the image
        text_path = image_path.with_suffix(".txt")
        text_path.write_text(output_text, encoding="utf-8")


def qwen_process_image(image_path: str, model, processor) -> str:
    ## Adjust the prompt as needed

    prompt = """There is a table in this image. I've extracted the row headers as a csv:

    ```
    RFID Tag No. / Security Label No.,,
    Identification no. of cube,Cube Mark,
    ,Lab Ref. No.,
    Mould no.,,
    Condition on received*,,
    Edges/corners damaged**,,
    Dimensions,W1 - width 1,mm
    ,W2 - height,
    ,W3 - width 2,
    Mass,as received,kg
    ,saturated in air,
    ,in water,
    Density***,by calculation,kg/m3
    ,by water-displacement,
    Maximum load at failure kN,,
    Compressive strength**** MPa,,
    Type of fracture*****,,
    ```

    Can you help me extract the data columns? You don't have to repeat the row headers again, just extract the data columns. You can ignore the rest of the document as well. Thanks!"""

    ## Can use local image file, e.g. "image.png" placed in the same directory
    ## Change to your own image path as needed

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "image": image_path,
                },
                {
                    "type": "text",
                    "text": prompt,
                },
            ],
        }
    ]

    # Preparation for inference
    inputs = processor.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_dict=True,
        return_tensors="pt",
    )
    inputs = inputs.to(model.device)

    # Inference: Generation of the output
    generated_ids = model.generate(**inputs, max_new_tokens=1024)
    generated_ids_trimmed = [
        out_ids[len(in_ids) :]
        for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    output_text = processor.batch_decode(
        generated_ids_trimmed,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )
    print(output_text[0])
    return output_text[0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Batch process PDFs with Qwen3-VL OCR models"
    )
    parser.add_argument(
        "--pdf-folder",
        type=Path,
        default=Path(__file__).parent / "../../data/pdfs",
        help="Path to folder containing PDF files (default: ../../data/pdfs/)",
    )
    parser.add_argument(
        "--output-folder",
        type=Path,
        default=Path(__file__).parent / "../../data/output",
        help="Path to output folder for results (default: ../../data/output/)",
    )

    args = parser.parse_args()

    # Resolve paths to absolute
    pdf_folder = args.pdf_folder.resolve()
    output_folder = args.output_folder.resolve()

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
    print(f"Found {len(list(pdf_folder.rglob('*.pdf')))} PDF file(s)")
    print()

    main(pdf_folder, output_folder)
