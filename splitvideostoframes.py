import torch
import torchvision.transforms as transforms
from PIL import Image
import lpips
from IPython import embed
import os
import glob
import csv  # You need to import csv

import numpy as np
import imageio
import numpy as np

def create_tensor_from_frame(frame):
    # Convert the frame (a NumPy array) to a PIL Image and ensure it is in RGB format
    image = Image.fromarray(frame).convert("RGB")
    
    # Define the transformation pipeline
    transform = transforms.Compose([
        transforms.Resize((64, 64)),                # Resize to 64x64
        transforms.ToTensor(),                       # Convert to tensor ([0,1] range, CxHxW)
        transforms.Normalize(mean=[0.5, 0.5, 0.5],     # Normalize to [-1, 1]
                             std=[0.5, 0.5, 0.5])
    ])
    
    # Apply the transformation and add a batch dimension (1, 3, 64, 64)
    image_tensor = transform(image).unsqueeze(0)
    return image_tensor

def createtensor(path):
    image = Image.open(path).convert("RGB")  # Ensure it's RGB

    # Define transformation
    transform = transforms.Compose([
        transforms.Resize((64, 64)),  # Resize to 64x64
        transforms.ToTensor(),         # Convert to [0,1] range (C,H,W format)
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])  # Normalize to [-1,1]
    ])

    # Apply transformation and add batch dimension (1,3,64,64)
    image_tensor = transform(image).unsqueeze(0)
    return image_tensor


    

def distance(image1, image2, entry):
        
        d = loss_fn_alex(image1, image2)
        # Convert the distance tensor to a Python number (if d is a single value)
        distance = d.item() if hasattr(d, 'item') else d
        datapoint = [entry, distance]
        return datapoint
        
  

    
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
    # List of common image file extensions
    image_extensions = ('*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp',  '*.mp4', '*.webp')
    locations = []  # Fixed variable name from 'location' to 'locations'
    print("Runned")
    for ext in image_extensions:
       
        # Create a search pattern for the current extension
        pattern = os.path.join(directory, ext)
        # Iterate over all files matching the current pattern
        for image_file in glob.glob(pattern):
            print("Found image:", image_file)
            locations.append(image_file)  # Use 'locations' here
        
    return locations


if __name__ == "__main__":
    # Load image1
    image_path1 = r"C:\Users\paulp\Documents\Workflows\Bildersequenzen\AlpsOwn\Hunyan\Bilder\videos_00163.png"
    

    # Get list of images to compare
    directory = r"C:\Users\paulp\Documents\Workflows\Bildersequenzen\AlpsOwn\Sora"
    
    vergleichlocations = iterate_images(directory)
    lpsusvalues = []

    # Initialize LPIPS model once (more efficient)
    loss_fn_alex = lpips.LPIPS(net='alex')  # best forward scores
    image1 = createtensor(image_path1)
    
    for entry in vergleichlocations:
    
        reader = imageio.get_reader(entry)
        for frame in reader:
            frame=create_tensor_from_frame(frame)
            lpsusvalues.append(distance(image1, frame, entry))
            
        # Compute LPIPS distance between image1 and image2
    
    # Write the computed distances to a CSV file
    referencepoint=lpsusvalues[0][0]
    valesuforshot=[]
    overallvalues=[]
    for datapoint in  lpsusvalues:
        if(datapoint[0]==referencepoint):
            valesuforshot.append(datapoint[1])
        elif datapoint[0]!=referencepoint:
            average= np.mean(valesuforshot)
            overallvalues.append(average)
            valesuforshot=[]
            referencepoint= datapoint[0]
            print("new shot:")
            print(average)
            print(datapoint[0])
            
            
   
        
    
    writecsv(r"C:\Users\paulp\Desktop\Masterarbeit\Code\MistyMountainsSoravsHunyanvideos_00163.csv",   overallvalues)
    
  
    
   