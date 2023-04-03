import cv2
from pathlib import Path
import os
from typing import List, Tuple, Dict
import subprocess
import re
from PIL import Image
import natsort
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm


def video_to_dir(output_dir, video_path) -> None:
    """
    Extracts all frames from a video and saves them as images in the specified directory.

    :param output_dir: str
        Path to the output directory where the extracted frames will be saved.
    :param video_path: str
        Path to the input video file.
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    cap = cv2.VideoCapture(video_path)
    frame_count = 0

    # Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Use tqdm to create a progress bar
    with tqdm(total=total_frames, desc="Processing frames") as progress_bar:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_file = os.path.join(output_dir, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_file, frame)
            frame_count += 1

            # Update the progress bar
            progress_bar.update(1)

    cap.release()


def add_text_on_image(font_file: str, font_size: int, text: str, image_location: Path,
                      output_location: Path, text_body_position: Tuple[int, int] = (50, 50),
                      text_color: Tuple[int, int, int] = (0, 0, 0),
                      stroke: int = 2,
                      stroke_color: Tuple[int, int, int] = (0, 0, 0),
                      shadow: Tuple[int, int] = (4, 4),
                      shadow_color: Tuple[int, int, int] = (0, 0, 0)) -> None:

    """
    Adds text to an image with optional stroke, shadow and other customizations.

    :param font_file: str
        Path to the font file.
    :param font_size: int
        Size of the font.
    :param text: str
        Text to be added to the image.
    :param image_location: Path
        Path to the input image file.
    :param output_location: Path
        Path to the output image file.
    :param text_body_position: Tuple[int, int], default: (50, 50), position of the text on the image.
    :param text_color: Tuple[int, int, int], default: (0, 0, 0), color of the text in RGB.
    :param stroke: int, default: 2, width of the stroke outline.
    :param stroke_color: Tuple[int, int, int], default: (0, 0, 0), color of the stroke outline in RGB.
    :param shadow: Tuple[int, int], default: (4, 4), offset of the text shadow in x and y direction.
    :param shadow_color: Tuple[int, int, int], default: (0, 0, 0), color of the text shadow in RGB.
    """

    # Load the font
    font = ImageFont.truetype(font_file, font_size)

    # Load the image
    image = Image.open(image_location)
    draw = ImageDraw.Draw(image)


    # Split the text into lines that fit within the image
    lines = []
    font_width, font_height = font.getsize(text)
    image_width, image_height = image.size
    max_text_width = image_width - 100  # leave a margin of 50 pixels on each side

    if font_width <= max_text_width:
        lines.append(text)
    else:
        words = text.split()
        current_line = words[0]
        for word in words[1:]:
            line_width = font.getsize(current_line + ' ' + word)[0]
            if line_width <= max_text_width:
                current_line += ' ' + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)

    # Draw the text on the image
    text_position = text_body_position  # make a copy of the original position
    for line in lines:
        # add stroke
        for x in range(-stroke, stroke + 1):
            for y in range(-stroke, stroke + 1):
                draw.text((text_position[0]+x, text_position[1]+y), line, stroke_color, font=font)
        draw.text(text_position, line, text_color, font=font)
        # add shadow
        draw.text((text_position[0]+shadow[0], text_position[1]+shadow[1]), line, shadow_color, font=font)
        text_position = (text_position[0], text_position[1] + font.getsize(line)[1] + 10)  # add 10 pixels of spacing between lines


    # Save the image with the text
    image.save(Path(output_location))


def convert_jpg_to_mp4(ref_video_path: Path, output_file: Path, input_directory: Path, overwrite=False) -> None:
    """
    Converts a directory of .jpg or .png images to an .mp4 video file, using a reference video's FPS.

    :param ref_video_path: Path
        Path to the reference video file used to determine the output video's FPS.
    :param output_file: Path
        Path to the output .mp4 video file.
    :param input_directory: Path
        Path to the directory containing the .jpg or .png images to be converted to a video.
    :param overwrite: bool, default: False
        If True, overwrites the output file if it exists.
    """
    
    # Use OpenCV to get the FPS value from the reference video
    cap = cv2.VideoCapture(str(ref_video_path))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    cap.release()

    input_dir = input_directory

    jpg_files = [f for f in os.listdir(input_dir) if f.endswith('.jpg') or f.endswith('.png')]

    jpg_files_sorted = natsort.natsorted(jpg_files)

    first_frame_name = jpg_files_sorted[0]

    match = re.search(r'\d+', first_frame_name)
    if match:
        start_frame = int(match.group())
    else:
        start_frame = 1

    original_dir = os.getcwd()
    os.chdir(input_dir)
    
    pattern = "frame_%d.jpg"
    temp = os.path.join(original_dir, input_dir, pattern)

    os.chdir(original_dir)

    cmd = [
        'ffmpeg',
        '-framerate', str(fps),
        '-start_number', str(start_frame),
        '-i', temp,
        '-c:v', 'libx264',
        '-profile:v', 'high',
        '-crf', '20',
        '-pix_fmt', 'yuv420p',
        f'{output_file}'
    ]

    if overwrite:
        cmd += ["-y"]

    subprocess.run(cmd, check=True)
    os.chdir(original_dir)

