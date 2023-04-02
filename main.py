import os
import tempfile
from moviepy.editor import concatenate_videoclips, VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

from utils import video_to_dir, add_text_on_image, convert_jpg_to_mp4
from typing import List, Dict, Tuple

def add_text_to_video(input_file: str, output_file: str, text_instructions: List[Dict]):
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
    """
    video_clips = []

    for instruction in text_instructions:
        modified_subclip = process_subclip(input_file, instruction)
        video_clips.append(modified_subclip)

    concatenate_and_save_clips(video_clips, output_file)




def process_subclip(input_file: str, instruction: dict) -> str:
    """
    Processes a subclip from the input video by adding text to it.

    :param input_file: str
        Path to the input video file.
    :param instruction: dict
        Dictionary containing the following keys:
            - start: int, start time of the segment in seconds.
            - end: int, end time of the segment in seconds.
            - text: str, text to be added to the segment.
            - font_file_location: str, path to the font file
            - font_size: int, size of the font.

    :return: str
        Path to the modified subclip.
        """
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
                                  frame_file, 
                                  frame_file, 
                                  **{k: v for k, v in instruction.items() if k not in {"start", "end", "text", "font_file_location", "font_size"}})

            # Convert the frames with text back to a subclip and store it in subclip_output
            subclip_output = f"{tmp_frames_dir}_modified.mp4"
            convert_jpg_to_mp4(temp_subclip_file.name, subclip_output, tmp_frames_dir)
            # Return the path of the modified subclip
            return subclip_output

def concatenate_and_save_clips(video_clips: List[str], output_file: str) -> None:
    """
    Concatenates a list of video clips and saves the final video to the output file.

    :param video_clips: List[str]
        A list of paths to video clips that will be concatenated.
    :param output_file: str
        Path to the output video file.

    This function also cleans up the temporary video files after concatenation.
    """

    # Create moviepy clips from the file paths, concatenate them, and write the output video
    final_video = concatenate_videoclips([VideoFileClip(clip) for clip in video_clips])
    final_video.write_videofile(output_file)

    # Clean up temporary video files
    for clip in video_clips:
        os.remove(clip)

def main():
    input_file = 'output_video.mp4'
    output_file = 'output_video2.mp4'
    text_instructions = [
        {
            "start": 0,
            "end": 5,
            "text": "Intro",
            "font_file_location": "Roboto/Roboto-Regular.ttf",
            "font_size": 30,
            "text_body_position": (50, 50),
            "text_color": (255, 255, 255),
            "stroke": 2,
            "stroke_color": (0, 0, 0),
            "shadow": (4, 4),
            "shadow_color": (0, 0, 0)
        },
        {
            "start": 5,
            "end": 10,
            "text": "Intro Main Part",
            "font_file_location": "Roboto/Roboto-Regular.ttf",
            "font_size": 30,
            "text_body_position": (50, 50),
            "text_color": (255, 255, 255),
            "stroke": 2,
            "stroke_color": (0, 0, 0),
            "shadow": (4, 4),
            "shadow_color": (0, 0, 0)
        },
        {
            "start": 10,
            "end": 15,
            "text": "Intro Main Part Conclusion",
            "font_file_location": "Roboto/Roboto-Regular.ttf",
            "font_size": 30,
            "text_body_position": (50, 50),
            "text_color": (255, 255, 255),
            "stroke": 2,
            "stroke_color": (0, 0, 0),
            "shadow": (4, 4),
            "shadow_color": (0, 0, 0)
        }
    ]

    add_text_to_video(input_file, output_file, text_instructions)


if __name__ == '__main__':
    main()

