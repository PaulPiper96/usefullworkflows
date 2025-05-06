import torch
import os
import glob
import csv  # You need to import csv
import numpy as np
import imageio
import open_clip
from PIL import Image

from random import randrange


def distance(prompt, frame, model, preprocess, device):
    similarity = None
    with torch.no_grad():
        # Convert NumPy frame to PIL Image
        image_pil = Image.fromarray(frame)

        # Preprocess the image for OpenCLIP
        image_tensor = preprocess(image_pil).unsqueeze(0).to(device)
        if model.visual.conv1.weight.dtype == torch.float16:
            image_tensor = image_tensor.half()

        # Tokenize the prompt and move to device
        text_tokens = open_clip.get_tokenizer('ViT-H-14')([prompt]).to(device)

        # Encode and compute similarity
        image_features = model.encode_image(image_tensor)
        text_features = model.encode_text(text_tokens)

        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)

        similarity = (image_features @ text_features.T).item()
        print("Similarity:", similarity)
    return similarity
    
def readcsv(filename, arraytopass):
    # Open CSV file in text mode with newline=''
    with open(filename, 'r') as file:
        content = file.read()
    
    # Split the content by newline characters
    lines = content.split('\n')
    
    # Iterate over each line and process it (here we just print it)
    for index, line in enumerate(lines, start=0):
        print(f"Line {index}: {line}")
        # Create a list for each line with its index and content
        arraytopass.append([index, line])
    return  arraytopass
        
  

def writecsv(path, data):
    # Open CSV file in text mode with newline=''
    with open(path, "w", newline="") as csvfile:
        out = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
        for entry in data:
            # Check if the entry is not an iterable (or is a string, which is iterable but we want to treat as a single value)
            if not isinstance(entry, (list, tuple)):
                entry = [entry]
            out.writerow(entry)
            
def iterate_images(directory):
    directory = directory.rstrip("/\\")
    image_extensions = ('*.mp4', '*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp', '*.webp')
    locations = []

    for ext in image_extensions:
        pattern = os.path.join(directory, '**', ext)
        for image_file in glob.glob(pattern, recursive=True):
            locations.append(image_file)

    # Sort numerically if filenames are numbers (like "12.mp4")
    try:
        locations.sort(key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))
    except ValueError:
        print("Warning: Could not sort numerically, falling back to default sort.")
        locations.sort()

    return locations


if __name__ == "__main__":
    # Load image1
    prompts=[]
    readcsv( r"C:\Users\paulp\Documents\Workflows\MovieGenVideoBench.txt", prompts)
    # Get list of images to compare
    bench_directory = r"C:\Users\paulp\Documents\Workflows\Bildersequenzen\allmovievbench"
    allmp4slocations=iterate_images(bench_directory)
    for something in allmp4slocations:
        print(something)
    
    #initializemodel  
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = open_clip.get_tokenizer('ViT-H-14')
    model, _, preprocess = open_clip.create_model_and_transforms(
    'ViT-H-14',
    pretrained='laion2b_s32b_b79k',
    device=device,
    precision='fp16'  # optional, helps with memory
    )
    cosinedata=[]
    breakiter=0
    for entry in prompts:
        datapoint=[]
        if breakiter > 100:
            break
        if len(entry[1]) > 3:
            reader = imageio.get_reader(allmp4slocations[breakiter])
            num_frames = reader.count_frames()
            randomint = randrange(num_frames)

            for i, frame in enumerate(reader):
                if i == randomint:
                    print("Prompt:", entry)
                    cosinedist= distance(entry[1], frame, model, preprocess, device)
                    datapoint.append(entry[0])
                    datapoint.append(entry[1])
                    datapoint.append(cosinedist)
                    cosinedata.append(datapoint)
                    break
        breakiter += 1
       
    writecsv(r"C:\Users\paulp\Desktop\Masterarbeit\Code\clip\NovieBenchCosine.csv",   cosinedata)
          
    
  
    
   