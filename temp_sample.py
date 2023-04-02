from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import tempfile

# Set the start and end times for the interval in seconds
start_time = 30
end_time = 40

# Create a temporary file with the ".mp4" extension
with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_file:
    # Cut the interval from the input video file and save it to the temporary file
    ffmpeg_extract_subclip("alt_data.mp4", start_time, end_time, targetname=temp_file.name)


# The temporary file is automatically deleted when the with block ends
