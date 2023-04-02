from PIL import Image, ImageDraw, ImageFont
from typing import List, Tuple, Dict
import subprocess
from pathlib import Path
import os
import cv2
import subprocess
import natsort
from concate_video  import concatenate_videos
import re

Sample: Dict[str, any] = {
    "text": str, 
    "font_location": str, 
    "text_size": int, 
    "text_position": Tuple[int, int], 
    "text_color": Tuple[int, int, int],
    "begin": int,
    "end": int,
}

def add_text_on_image(font_file: str, font_size: int, text: str, image_location: List[str],
                      output_location: Path, text_body_position: Tuple[int, int] = (50, 50),
                      text_color: Tuple[int, int, int] = (0, 0, 0),
                      stroke: int = 2,
                      stroke_color: Tuple[int, int, int] = (0, 0, 0),
                      shadow: Tuple[int, int] = (4, 4),
                      shadow_color: Tuple[int, int, int] = (0, 0, 0)) -> None:
    
    """
    Adds text to an image and saves the resulting image in a specified output location.

    Parameters:
    font_file (str): The path to the font file to be used.
    font_size (int): The size of the font to be used.
    text (str): The text to be added to the image.
    image_location (List[str]): The location(s) of the image(s) to add the text to.
    output_location (Path): The path to the output directory where the resulting image(s) should be saved.
    text_body_position (Tuple[int, int]): The (x, y) position where the text should start being added to the image. Default is (50, 50).
    text_color (Tuple[int, int, int]): The color of the text to be added to the image. Default is black.
    stroke (int): The size of the stroke to be added to the text. Default is 2.
    stroke_color (Tuple[int, int, int]): The color of the stroke to be added to the text. Default is black.
    shadow (Tuple[int, int]): The (x, y) position of the shadow to be added to the text. Default is (4, 4).
    shadow_color (Tuple[int, int, int]): The color of the shadow to be added to the text. Default is black.

    Returns:
    None
    """
    # Create the output directory if it does not exist
    output_location_path = Path(output_location)
    output_location_path_directory = output_location_path.parent

    output_location_path_directory.mkdir(parents=True, exist_ok=True)

    # Load the font
    font = ImageFont.truetype(font_file, font_size)

    # Loop through the image locations with an index
    for img_location in image_location:
        image = Image.open(img_location)
        # Create an ImageDraw object
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

        # Define the output file name
        filename = Path(img_location).name
        output_file_path = output_location_path / filename

        output_file_path_dir = output_file_path.parent
        og_loc = Path.cwd()
        output_file_path_dir.mkdir(parents=True, exist_ok=True)
        os.chdir(output_file_path_dir)

        # Save the image with the text
        image.save(filename)
        os.chdir(og_loc)


def interval(movie_path:Path, destination:Path, begin=None, end=None):
    # Create the destination directory if it doesn't exist
    if not os.path.exists(destination):
        os.makedirs(destination)

    # Open the video file
    cap = cv2.VideoCapture(movie_path)

    # Get the frames per second and total number of frames
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the start and end frame numbers
    start_frame = begin * fps if begin is not None else 0
    end_frame = end * fps if end is not None else total_frames

    # Check that the start and end frames are within bounds
    if start_frame >= total_frames or end_frame > total_frames:
        raise ValueError("Invalid start or end frame")

    # Set the video capture position to the start frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    # Iterate through the frames and save them as individual image files
    for i in range(start_frame, end_frame):
        ret, frame = cap.read()
        if not ret:
            break
        filename = os.path.join(destination, f"frame_{i}.jpg")
        cv2.imwrite(filename, frame)

    # Release the video capture
    cap.release()


def convert_jpg_to_mp4(input_dir, output_file, reference_video):
    cap = cv2.VideoCapture(reference_video)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    cap.release()

    # get a list of all jpg files in the input directory
    jpg_files = [f for f in os.listdir(input_dir) if f.endswith('.jpg')]

    # sort the list of jpg files in natural sort order
    jpg_files_sorted = natsort.natsorted(jpg_files)

    # get the name of the first frame
    first_frame_name = jpg_files_sorted[0]

    # extract the digits from the file name using regular expressions
    match = re.search(r'\d+', first_frame_name)
    if match:
        start_frame = int(match.group())
    else:
        start_frame = 1

    # build the FFmpeg command
    cmd = [
        'ffmpeg',
        '-framerate', str(fps),
        '-start_number', str(start_frame),
        '-i', f'{input_dir}/frame_%d.jpg',
        '-c:v', 'libx264',
        '-profile:v', 'high',
        '-crf', '20',
        '-pix_fmt', 'yuv420p',
        f'{output_file}.mp4'
    ]

    # run the command as a subprocess
    subprocess.run(cmd, check=True)


def convert_jpg_to_mp4(input_dir, output_file, reference_video, overwrite=False):
    cap = cv2.VideoCapture(reference_video)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    cap.release()

    # get a list of all jpg files in the input directory
    jpg_files = [f for f in os.listdir(input_dir) if f.endswith('.jpg')]

    # sort the list of jpg files in natural sort order
    jpg_files_sorted = natsort.natsorted(jpg_files)

    # get the name of the first frame
    first_frame_name = jpg_files_sorted[0]

    # extract the digits from the file name using regular expressions
    match = re.search(r'\d+', first_frame_name)

    if match:
        start_frame = int(match.group())
    else:
        start_frame = 1

    # build the FFmpeg command
    cmd = [
        'ffmpeg',
        '-framerate', str(fps),
        '-start_number', str(start_frame),
        '-i', f'{input_dir}/frame_%d.jpg',
        '-c:v', 'libx264',
        '-profile:v', 'high',
        '-crf', '20',
        '-pix_fmt', 'yuv420p',
        f'{output_file}.mp4'
    ]

    # insert the -y option if overwrite is True
    if overwrite:
        cmd.insert(1, '-y')

    # run the command as a subprocess
    subprocess.run(cmd, check=True)


def get_sorted_image_files(input_dir):
    image_files = natsort.natsorted([os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.jpg') or f.endswith('.png')])
    return image_files


if __name__ == '__main__':

    # define the text strings separately
    text_1 = "This is a temporary place holder, guess. Yo What is good my guy"
    text_2 =  text_1 + "The West Indies is a subregion of North America, surrounded by the North Atlantic Ocean and the Caribbean Sea, which comprises 13 independent island countries, 18 dependencies, and three archipelagos: the Greater Antilles, the Lesser Antilles, and the Lucayan Archipelago."
    text_3 = text_2 + ("The subregion includes all the islands in the Antilles, plus The Bahamas and the Turks and Caicos Islands, which are in the North Atlantic Ocean. "
          "Nowadays, the term West Indies is often interchangeable with the term Caribbean. "
          "However, the term Caribbean may also include some Central and South American mainland nations which have Caribbean coastlines, such as Belize, French Guiana, Guyana, and Suriname, as well as the Atlantic island nations of Barbados, Bermuda, and Trinidad and Tobago. "
          "These countries are geographically distinct from the three main island groups, but culturally related.")
    
    text_color = (0, 0, 0)
    font_file = Path(r"Roboto/Roboto-Bold.ttf").__str__()
    font_size = 100
    default_text_position = (50,50)
    
    text_list = [
        {
            "text": text_1,
            "font_location": font_file,
            "text_size": font_size,
            "text_position": default_text_position,
            "text_color": text_color,
            "begin": 0,
            "end": 10
        },
        {
            "text": text_2,
            "font_location": font_file,
            "text_size": font_size,
            "text_position": default_text_position,
            "text_color": text_color,
            "begin": 10,
            "end": 20
        },
        {
            "text": text_3,
            "font_location": font_file,
            "text_size": font_size,
            "text_position": default_text_position,
            "text_color": text_color,
            "begin": 20,
            "end": None
        }
    ]


    video_file = Path("/wiki_data_set/video.mp4")

    temp = lambda x : Path(f"data_sample/ssample_{x}")

    text_data_with_index = [*enumerate(text_list)]

    video_list = []

    for i, data in text_data_with_index:
        interval(str(video_file), str(temp(i)), data["begin"], data["end"])
        x = get_sorted_image_files(temp(i))

        add_text_on_image(
            data['font_location'],
            data['text_size'],
            data['text'],
            x,
            f"temp/sample_{i}",

        )
        convert_jpg_to_mp4(f"temp/sample_{i}", f"sample_{i}",str(video_file),overwrite=True)
        video_list.append(f"sample_{i}.mp4")
        
    concatenate_videos(videos=video_list,output="drip.mp4")


    x=0