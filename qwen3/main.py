from transformers import Qwen3VLForConditionalGeneration, AutoProcessor

# default: Load the model on the available device(s)
model = Qwen3VLForConditionalGeneration.from_pretrained(
    "Qwen/Qwen3-VL-4B-Instruct", 
    dtype="auto",
    device_map="auto",
)

print("model loaded")

# We recommend enabling flash_attention_2 for better acceleration and memory saving, especially in multi-image and video scenarios.
# model = Qwen3VLForConditionalGeneration.from_pretrained(
#     "Qwen/Qwen3-VL-2B-Instruct",
#     dtype=torch.bfloat16,
#     attn_implementation="flash_attention_2",
#     device_map="auto",
# )

processor = AutoProcessor.from_pretrained("Qwen/Qwen3-VL-4B-Instruct")

print("processor loaded")

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

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
                # "image": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg",
                "image": "image.png",
            },
            {
                "type": "text",
                "text": prompt, # "Please transcribe the table in this image into a tabular format.",
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
    out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
]
output_text = processor.batch_decode(
    generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
)
print(output_text)
