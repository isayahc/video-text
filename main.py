import os
import tempfile
from moviepy.editor import concatenate_videoclips, VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
# from vid_sample import video_to_dir, add_text_on_image, convert_jpg_to_mp4
from utils import video_to_dir, add_text_on_image, convert_jpg_to_mp4
from typing import List, Dict, Tuple

def add_text_to_video(input_file: str, output_file: str, text_instructions: list[Dict]):
    """
    Add text to specific segments of a video.

    :param input_file: str
        Path to the input video file.
    :param output_file: str
        Path to the output video file.
    :param text_instructions: list
        List of dictionaries containing the following keys:
            - start: int, start time of the segment in seconds.
            - end: int, end time of the segment in seconds.
            - text: str, text to be added to the segment.
            - font_file_location: str, path to the font file.
            - font_size: int, size of the font.
            
        Optional dictionary items for text_instructions (from add_text_on_image):
            - text_body_position: Tuple[int, int], default: (50, 50), position of the text on the image.
            - text_color: Tuple[int, int, int], default: (0, 0, 0), color of the text in RGB.
            - stroke: int, default: 2, width of the stroke outline.
            - stroke_color: Tuple[int, int, int], default: (0, 0, 0), color of the stroke outline in RGB.
            - shadow: Tuple[int, int], default: (4, 4), offset of the text shadow in x and y direction.
            - shadow_color: Tuple[int, int, int], default: (0, 0, 0), color of the text shadow in RGB.

    """
    video_clips = []

    for instruction in text_instructions:
        # Create a temporary file to store the extracted subclip
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_subclip_file:
            # Create temporary directory for processing the frames
            with tempfile.TemporaryDirectory() as tmp_frames_dir:
                # Extract the subclip from the input video
                ffmpeg_extract_subclip(input_file, instruction["start"], instruction["end"], targetname=temp_subclip_file.name)

                # Convert the subclip to individual frames and store them in tmp_frames_dir
                video_to_dir(tmp_frames_dir, temp_subclip_file.name)

                # Add text to each frame in tmp_frames_dir
                frame_files = [os.path.join(tmp_frames_dir, i) for i in os.listdir(tmp_frames_dir)]
                for frame_file in frame_files:
                    add_text_on_image(instruction["font_file_location"], 
                                      instruction["font_size"], instruction["text"], 
                                      frame_file, frame_file, **{k: v for k, v in instruction.items() if k not in {"start", "end", "text", "font_file_location", "font_size"}})

                # Convert the frames with text back to a subclip and store it in subclip_output
                subclip_output = f"{tmp_frames_dir}_modified.mp4"
                convert_jpg_to_mp4(temp_subclip_file.name, subclip_output, tmp_frames_dir)  # Change input_file to temp_subclip_file.name

                # Append the modified subclip file path to the list of video_clips
                video_clips.append(subclip_output)

    # Create moviepy clips from the file paths, concatenate them, and write the output video
    final_video = concatenate_videoclips([VideoFileClip(clip) for clip in video_clips])
    final_video.write_videofile(output_file)

if __name__ == '__main__':
    # Example usage:
    input_file = r"C:\Users\isaya\Desktop\erza_miller_strange_rant.mp4"
    output_file = "output_video.mp4"
    text_instructions = [
        {"start": 0, "end": 10, "text": "Text ", "font_file_location": r"Roboto\Roboto-Light.ttf", "font_size": 50,"text_color":(255,255,255), "stroke":1,},
        {"start": 10, "end": 20, "text": "Text Text", "font_file_location": r"Roboto\Roboto-Light.ttf", "font_size": 50, "text_color":(255,255,255), "stroke":1,},
        {"start": 20, "end": 30, "text": "Text Text Text", "font_file_location": r"Roboto\Roboto-Light.ttf", "font_size": 50, "text_color":(255,255,255), "stroke":1,},
    ]

    add_text_to_video(input_file, output_file, text_instructions)
