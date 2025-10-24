from transformers import AutoModel, AutoTokenizer
import torch
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
model_name = "deepseek-ai/DeepSeek-OCR"

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModel.from_pretrained(
    model_name,
    # _attn_implementation="flash_attention_2",
    trust_remote_code=True,
    use_safetensors=True,
)
model = model.eval().cuda().to(torch.bfloat16)

## Possible prompts (from deepseek-ocr github README):
# document: <image>\n<|grounding|>Convert the document to markdown.
# other image: <image>\n<|grounding|>OCR this image.
# without layouts: <image>\nFree OCR.
# figures in document: <image>\nParse the figure.
# general: <image>\nDescribe this image in detail.
# rec: <image>\nLocate <|ref|>xxxx<|/ref|> in the image.
prompt = "<image>\n<|grounding|>Convert the document to markdown. "

## Adjust the image_file and output_path to your own needs
image_file = "your_image.jpg"
output_path = "your/output/dir"

## Adjust the base_size, image_size, crop_mode to your own needs

## Possible values:
# Tiny: base_size = 512, image_size = 512, crop_mode = False
# Small: base_size = 640, image_size = 640, crop_mode = False
# Base: base_size = 1024, image_size = 1024, crop_mode = False
# Large: base_size = 1280, image_size = 1280, crop_mode = False
# Gundam: base_size = 1024, image_size = 640, crop_mode = True

# Generally, larger base_size and image_size lead to better results but require more GPU memory.

res = model.infer(
    tokenizer,
    prompt=prompt,
    image_file=image_file,
    output_path=output_path,
    base_size=1024,
    image_size=640,
    crop_mode=True,
    save_results=True,
    test_compress=True,
)
