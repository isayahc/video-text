import argparse
import os
import shutil
import tempfile
from moviepy.editor import VideoFileClip, concatenate_videoclips

def extract_frames_and_create_video(video_file, output_file):
    # create a temporary directory to store the frames
    temp_dir = tempfile.mkdtemp()

    # read the video file using MoviePy
    video_clip = VideoFileClip(video_file)

    # extract each frame of the video and save it to the temporary directory
    for i, frame in enumerate(video_clip.iter_frames()):
        frame_file = os.path.join(temp_dir, f"{i}.png")
        with open(frame_file, "wb") as f:
            f.write(frame)

    # close the video file
    video_clip.reader.close()

    # create a new video clip from the frames in the temporary directory
    frame_files = sorted([os.path.join(temp_dir, f) for f in os.listdir(temp_dir)])
    frame_duration = video_clip.duration / len(frame_files)
    frames_clip = [VideoFileClip(frame_file, duration=frame_duration) for frame_file in frame_files]
    final_clip = concatenate_videoclips(frames_clip)

    # write the new video clip to a file
    final_clip.write_videofile(output_file)

    # remove the temporary directory and its contents
    shutil.rmtree(temp_dir)

if __name__ == "__main__":
    # create the argument parser
    parser = argparse.ArgumentParser(description="Extract frames from a video file and create a new video file from them.")

    # add the input file argument
    parser.add_argument("input_file", type=str, help="the path to the input video file")

    # add the output file argument
    parser.add_argument("output_file", type=str, help="the path to the output video file")

    # parse the command-line arguments
    args = parser.parse_args()

    # call the function with the input and output file paths
    extract_frames_and_create_video(args.input_file, args.output_file)
