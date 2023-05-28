# Video Text Overlay

This Python script allows you to add text overlays to specific segments of a video. Unlike Textwrap, you can append to the text on the current screen and the position of the original text will remain constant. You can provide multiple text instructions to add text to different parts of the video.

## Requirements

- Python 3.6+
- MoviePy
- Pillow
- OpenCV

## Installation

1. Install the required packages using pip:

```python
python -m venv venv
activate
pip install -r requirements.txt
```

## Usage

## Parameters for `add_text_to_video`

- `input_file`: str
    Path to the input video file.

- `output_file`: str
    Path to the output video file.

- `text_instructions`: list
    List of dictionaries containing the following keys:
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
    Each instruction dictionary can contain the same arguments as the `add_text_on_image` function.

- `overwrite`: bool, optional
    If `True`, overwrite the output file if it already exists. Default is `False`.

## Example

```python
# Importing the add_text_to_video function from the main module
from main import add_text_to_video

# Defining the input and output video file paths
input_file = 'input_video.mp4'
output_file = 'output_video.mp4'

# Defining the font file path, font size, and stroke width
font_file = 'assets\Roboto\Roboto-Bold.ttf'
font_size = 50
stroke_width = 1

text_1 = "The West Indies is a subregion of North America, surrounded by the North Atlantic Ocean and the Caribbean Sea, which comprises 13 independent island countries, 18 dependencies, and three archipelagos: the Greater Antilles, the Lesser Antilles, and the Lucayan Archipelago. "
text_2 =  text_1 + "The subregion includes all the islands in the Antilles, plus The Bahamas and the Turks and Caicos Islands, which are in the North Atlantic Ocean. "
text_3 = text_2 + (
        "Nowadays, the term West Indies is often interchangeable with the term Caribbean. "
        "However, the term Caribbean may also include some Central and South American mainland nations which have Caribbean coastlines, such as Belize, French Guiana, Guyana, and Suriname, as well as the Atlantic island nations of Barbados, Bermuda, and Trinidad and Tobago. "
        "These countries are geographically distinct from the three main island groups, but culturally related.")

# Defining the text instructions as a list of dictionaries
text_instructions = [
    {
        "start": 0,
        "end": 5,
        "text": text_1,
        "font_file_location": font_file,
        "font_size": font_size,
        "text_body_position": (50, 50),
        "text_color": (0, 0, 0),
        "stroke": stroke_width,
        "stroke_color": (0, 0, 0),
        "shadow": (4, 4),
        "shadow_color": (0, 0, 0)
    },
    {
        "start": 5,
        "end": 10,
        "text": text_2,
        "font_file_location": font_file,
        "font_size": font_size,
        "text_body_position": (50, 50),
        "text_color": (0, 0, 0),
        "stroke": stroke_width,
        "stroke_color": (0, 0, 0),
        "shadow": (4, 4),
        "shadow_color": (0, 0, 0)
    },
    {
        "start": 10,
        "end": 15,
        "text": text_3,
        "font_file_location": font_file,
        "font_size": font_size,
        "text_body_position": (50, 50),
        "text_color": (0, 0, 0),
        "stroke": stroke_width,
        "stroke_color": (0, 0, 0),
        "shadow": (4, 4),
        "shadow_color": (0, 0, 0)
    }
]

# Calling the add_text_to_video function with the input parameters and setting the overwrite parameter to True
add_text_to_video(input_file, output_file, text_instructions,overwrite=True)

````

![Alt Text](https://github.com/isayahc/video-text/blob/main/assets/screenshots/cap1.PNG)
![Alt Text](https://github.com/isayahc/video-text/blob/main/assets/screenshots/cap2.PNG)
![Alt Text](https://github.com/isayahc/video-text/blob/main/assets/screenshots/cap3.png)
