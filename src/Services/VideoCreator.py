import os
import imageio

def create_video_from_images(image_folder, output_path, fps):
    images = []
    filenames = sorted(os.listdir(image_folder))

    for filename in filenames:
        if filename.endswith('.jpg') or filename.endswith('.jpeg'):
            image_path = os.path.join(image_folder, filename)
            images.append(imageio.imread(image_path))

    # Save images as a video
    with imageio.get_writer(output_path, fps=fps) as video_writer:
        for image in images:
            video_writer.append_data(image)


create_video_from_images("Generated", "example.mp4", 24)