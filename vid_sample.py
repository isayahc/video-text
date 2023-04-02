import cv2
from pathlib import Path
import os
from typing import List, Tuple, Dict
import subprocess
import re
import numpy as np
from PIL import Image
import tempfile
import natsort
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import moviepy
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm

VideoText : Dict[str, any] = {
    "text": str, 
    "font_location": str, 
    "text_size": int, 
    "text_position": Tuple[int, int], 
    "text_color": Tuple[int, int, int],
    "begin": int,
    "end": int,
}


class Video:
    def __init__(self, video_path:Path, temp_directory_name = Path("temp")):
        self.video_path = video_path
        self.temp_directory_name = temp_directory_name

    def video_to_array(self,) -> None:
        cap = cv2.VideoCapture(str(self.video_path))
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # convert BGR to RGB
            yield frame
        cap.release()

    def video_to_dir(self, ) -> None:

        output_dir = str(self.temp_directory_name)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        cap = cv2.VideoCapture(str(self.video_path))
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # convert BGR to RGB
            frame_file = os.path.join(output_dir, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_file, frame)
            frame_count += 1
        cap.release()

    def get_fps(self) -> int:
        video_path = str(self.video_path)

        clip = VideoFileClip(video_path)
        fps = clip.fps
        clip.close()
        return fps

    def get_number_of_frames(self) -> int:

        # Open the video file
        cap = cv2.VideoCapture(str(self.video_path))

        # Get the frames per second and total number of frames
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        return  total_frames

    def get_frames(self, seconds: float):
        cap = cv2.VideoCapture(str(self.video_path))
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frames_to_read = int(fps * seconds)
        start_frame = 0

        while start_frame < total_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
            for i in range(frames_to_read):
                ret, frame = cap.read()
                if not ret:
                    break
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                yield frame
            start_frame += frames_to_read

        cap.release()

    def convert_jpg_to_mp4(self, output_file:Path, overwrite=False) -> None:

        fps = self.get_fps()

        input_dir = str(self.temp_directory_name)
        input_dir = self.temp_directory_name

        # get a list of all jpg files in the input directory
        jpg_files = [f for f in os.listdir(input_dir) if f.endswith('.jpg') or f.endswith('.png')]

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

        original_dir = os.getcwd()
        data = os.chdir(input_dir)
        
        pattern = "frame_%d.jpg"
        temp = os.path.join(original_dir,input_dir,pattern)

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

        # run the command as a subprocess
        subprocess.run(cmd, check=True)
        os.chdir(original_dir)

    def get_video_length(self):
        video_path = str(self.video_path)
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps
        cap.release()
        return duration
    
    def calculate_frame_time(self):
        return self.get_video_length() / self.get_number_of_frames()
    
    def get_first_10_seconds(self):
        clip = VideoFileClip(str(self.video_path)).subclip(0, 10)
        return clip
    
    def get_video_segment(self,start,end=None):
        if end:
            clip = VideoFileClip(str(self.video_path)).subclip(start)
        else:
            clip = VideoFileClip(str(self.video_path)).subclip(start, end)

        return clip
    
    def create_temp_dir_and_convert_video(self):
        tmp_dir = tempfile.mkdtemp()
        video_to_dir(tmp_dir, str(self.video_path))
        convert_jpg_to_mp4(self, "sample_0.mp4", True)
        os.rmdir(tmp_dir)

    def create_temp_dir_and_cool_stuff(self):
        tmp_dir = tempfile.mkdtemp()
        video_to_dir(tmp_dir, str(self.video_path))
        frames = [os.path.join(tmp_dir,i) for i in os.listdir(tmp_dir)]
        convert_jpg_to_mp4(self, "sample_0.mp4", True)

        os.rmdir(tmp_dir)

def generate_video(generator, output_file, fps=30, size=(640, 480)):
    cmd = [
        'ffmpeg',
        '-y',
        '-f', 'rawvideo',
        '-pix_fmt', 'rgb24',
        '-s', f'{size[0]}x{size[1]}',
        '-r', str(fps),
        '-i', '-',
        '-pix_fmt', 'yuv420p',
        '-preset', 'veryslow',
        '-crf', '18',
        '-threads', '0',
        output_file
    ]
    
    try:
        with subprocess.Popen(cmd, stdin=subprocess.PIPE) as ffmpeg:
            for frame in generator:
                # Convert ndarray to bytes and write to FFmpeg process
                if not ffmpeg.stdin.closed:
                    ffmpeg.stdin.write(frame.tobytes())

    except subprocess.SubprocessError as e:
        print(f"Error: {e}")

    finally:
        if ffmpeg.stdin:
            ffmpeg.stdin.close()
        ffmpeg.wait()



def video_to_dir(output_dir, video_path) -> None:

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


def convert_jpg_to_mp4(Video_obj, output_file:Path, input_directory:Path, overwrite=False) -> None:

    fps = Video_obj.get_fps()

    # input_dir = str(Video_obj.temp_directory_name)
    # input_dir = Video_obj.temp_directory_name
    input_dir = input_directory

    # get a list of all jpg files in the input directory
    jpg_files = [f for f in os.listdir(input_dir) if f.endswith('.jpg') or f.endswith('.png')]

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

    original_dir = os.getcwd()
    data = os.chdir(input_dir)
    
    pattern = "frame_%d.jpg"
    temp = os.path.join(original_dir,input_dir,pattern)

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

    # run the command as a subprocess
    subprocess.run(cmd, check=True)
    os.chdir(original_dir)


def convert_jpg_to_mp4(ref_video_path: Path, output_file: Path, input_directory: Path, overwrite=False) -> None:
    
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



def add_text_on_image(font_file: str, font_size: int, text: str, image_location: Path,
                      output_location: Path, text_body_position: Tuple[int, int] = (50, 50),
                      text_color: Tuple[int, int, int] = (0, 0, 0),
                      stroke: int = 2,
                      stroke_color: Tuple[int, int, int] = (0, 0, 0),
                      shadow: Tuple[int, int] = (4, 4),
                      shadow_color: Tuple[int, int, int] = (0, 0, 0)) -> None:


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






if __name__ == '__main__':
    
    video_file = Path("underwater-37712.mp4")

    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:

        tmp_dir = tempfile.mkdtemp()

        tmp_di_0 = tempfile.mkdtemp()

        video = Video(video_file)


        ffmpeg_extract_subclip(str(video_file), 0, 10, targetname=f.name)


        alt_vid = Video(f.name,tmp_di_0)


        video_to_dir(tmp_di_0,f.name)


    ff = [os.path.join(tmp_di_0,i) for i in os.listdir(tmp_di_0)]
    for i in ff:
        add_text_on_image(r"Roboto\Roboto-Light.ttf",
                        50,
                        "hiiiii",
                        i,
                        i,)
        
    convert_jpg_to_mp4(alt_vid,"alt_data.mp4",tmp_di_0,True)



    print(video.calculate_frame_time())
    video.convert_jpg_to_mp4("./sample_0.mp3",True)

    # video.video_to_dir()

    ff = video.get_first_10_seconds()

    [
        video.get_video_segment(0,5),
        video.get_video_segment(5,10),
        video.get_video_segment(5,15)
    ]

    # video.convert_jpg_to_mp4("sample_0",True)
    x=0
