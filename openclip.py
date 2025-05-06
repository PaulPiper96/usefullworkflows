import torch
import open_clip
from PIL import Image

# Image path
image_path = r"C:\Users\paulp\Documents\Workflows\Bildersequenzen\Möwenshot\HunyanBaslineImage\videos_00149.png"

# Set device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load OpenCLIP model with larger context window
model, _, preprocess = open_clip.create_model_and_transforms(
    'ViT-H-14',
    pretrained='laion2b_s32b_b79k',
    device=device,
    precision='fp16'  # optional, helps with memory
)

# Tokenizer
tokenizer = open_clip.get_tokenizer('ViT-H-14')

# Load and preprocess image
image = preprocess(Image.open(image_path).convert("RGB")).unsqueeze(0).to(device).half()


# Long prompt
prompt = (
    "Slowmotion shot of a beach at sunset, seagulls flying around. "
    "The sky is a beautiful orange and yellow color, with the sun setting over the horizon. "
    "The water is calm and the waves are gently lapping against the shore. "
    "In the distance, you can see the silhouette of a city. The beach is covered in small rocks and pebbles, "
    "and there are a few birds flying in the sky. The overall mood of the image is peaceful and serene."
)

# Tokenize and move to device
text_tokens = tokenizer([prompt]).to(device)

# Encode and compute similarity
with torch.no_grad():
    image_features = model.encode_image(image)
    text_features = model.encode_text(text_tokens)

    image_features /= image_features.norm(dim=-1, keepdim=True)
    text_features /= text_features.norm(dim=-1, keepdim=True)

    similarity = (image_features @ text_features.T).item()

print(f"Cosine similarity: {similarity:.4f}")
