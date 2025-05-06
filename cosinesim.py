import torch
import clip
from PIL import Image

# Load the model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/16", device=device)

# Load image
image_path = r"C:\Users\paulp\Documents\Workflows\Bildersequenzen\Möwenshot\BaseLine_frame\VergleichMasterarbeit_Möwe001.jpg"
image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)

# Short prompt that fits in CLIP's context window
prompts = [
    "Slowmotion Shot of a beach at sunset, Seagulls flying around. The sky is a beautiful orange and yellow color, with the sun setting over the horizon.",
    "Slowmotion Shot of a beach at sunset, Seagulls flying around. The sky is a beautiful orange and yellow color, with the sun setting over the horizon. The water is calm and the waves are gently lapping against the shore",
    "Slowmotion Shot of a beach at sunset, Seagulls flying around. The sky is a beautiful orange and yellow color, with the sun setting over the horizon. In the distance,you can see the shilouette of a city. The beach is covered in small rocks and pebbles.",
    "Slowmotion Shot of a beach at sunset, Seagulls flying around. The sky is a beautiful orange and yellow color, with the sun setting over the horizon. The overall mood of the image is peaceful and serene. ",
    "Slowmotion Shot of a beach at sunset, Seagulls flying around. The sky is a beautiful orange and yellow color, with the sun setting over the horizon. In the distance,you can see the shilouette of a city. There are a few birds flying in the sky. The overall mood of the image is peaceful and serene."
]
results=[]
# Tokenize prompt
for prompt in prompts:
    text = clip.tokenize([prompt]).to(device)

    # Encode image and text
    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text)

        # Normalize embeddings
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)

        # Compute cosine similarity
        similarity = (image_features @ text_features.T).item()
        results.append(similarity)
        
        
print(f"Cosine Similarity: {results}")
