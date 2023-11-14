import requests
import torch
from PIL import Image
from io import BytesIO
import imageio
from PIL import Image
from tqdm import tqdm
import random 

from diffusers import StableDiffusionImg2ImgPipeline

device = "cuda"
model_id_or_path = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id_or_path, torch_dtype=torch.float16)
pipe = pipe.to(device)

url = "https://raw.githubusercontent.com/CompVis/stable-diffusion/main/assets/stable-samples/img2img/sketch-mountains-input.jpg"

response = requests.get(url)
init_image = Image.open(BytesIO(response.content)).convert("RGB")
init_image = init_image.resize((768, 512))


def get_frames_from_video(video_path):
    frames = []
    with imageio.get_reader(video_path) as reader:
        for frame in reader:
            pil_image = Image.fromarray(frame)
            frames.append(pil_image)
    return frames

prompt = "A fantasy landscape, trending on artstation"

video_path = "..\Footage\Example.mp4"
frames = get_frames_from_video(video_path)


for i, frame in tqdm(enumerate(frames)):
    prompt = "Super Ultra Realistical Image With A lot Of Details Like Unreal Engine 5 Render 3D"

    images = pipe(prompt=prompt, image=frame, strength=0.2, guidance_scale=7.5, num_inference_steps=50, seed=random.randint(1,99999999999)).images
    images[0].save(f"Generated\{i}.jpg")