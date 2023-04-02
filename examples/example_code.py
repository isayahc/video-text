import main

input_file = './output_video.mp4'
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

main.add_text_to_video(input_file, output_file, text_instructions)