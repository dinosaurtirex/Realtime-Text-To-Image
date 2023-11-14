import torch
from diffusers import AutoPipelineForImage2Image
from diffusers.utils import make_image_grid, load_image

from tqdm import tqdm 

import imageio
from PIL import Image


pipeline = AutoPipelineForImage2Image.from_pretrained(
    "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
).to("cuda")
pipeline.enable_model_cpu_offload()
# remove following line if xFormers is not installed or you have PyTorch 2.0 or higher installed
pipeline.enable_xformers_memory_efficient_attention()

# prepare image
url = "https://huggingface.co/datasets/hug gingface/documentation-images/resolve/main/diffusers/img2img-init.png"

def get_frames_from_video(video_path):
    frames = []
    with imageio.get_reader(video_path) as reader:
        for frame in reader:
            pil_image = Image.fromarray(frame)
            frames.append(pil_image)
    return frames


video_path = "..\Footage\Record.mp4"
frames = get_frames_from_video(video_path)


for i, frame in tqdm(enumerate(frames)):

    init_image = load_image(frame)

    prompt = "ultra realistical version hq"

    # pass prompt and image to pipeline
    image = pipeline(prompt, image=init_image).images[0]
    #make_image_grid([init_image, image], rows=1, cols=2)

    image.save(f"Generated\{i}.jpg")