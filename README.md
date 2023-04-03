# README.md

## Video Text Overlay

This Python script allows you to add text overlays to specific segments of a video. Unlike Textwrap, you can append to the text on the current screen and the position of the original text will remain constant. You can provide multiple text instructions to add text to different parts of the video.

# Video Text Overlay

This Python script allows you to add text overlays to specific segments of a video. You can provide multiple text instructions to add text to different parts of the video.

## Requirements

- Python 3.6+
- MoviePy
- Pillow
- OpenCV

## Installation

1. Install the required packages using pip:

```
python -m venv venv
activate
pip install requirements.txt
```


2. Download the `main.py` and `utils.py` files.

## Usage

1. Edit the `main()` function in the script to provide the input video file, output video file, and text instructions.

2. Text instructions are a list of dictionaries, each containing the following keys:
   - `start`: int, start time of the segment in seconds.
   - `end`: int, end time of the segment in seconds.
   - `text`: str, text to be added to the segment.
   - `font_file_location`: str, path to the font file.
   - `font_size`: int, size of the font.
   - `text_body_position`: tuple, the position of the text on the frame (x, y).
   - `text_color`: tuple, RGB color of the text.
   - `stroke`: int, width of the stroke around the text.
   - `stroke_color`: tuple, RGB color of the stroke.
   - `shadow`: tuple, the shadow offset (x, y).
   - `shadow_color`: tuple, RGB color of the shadow.

3. Run the script:

```bash
python main.py
```