from main import add_text_to_video
text_1 = "The West Indies is a subregion of North America, surrounded by the North Atlantic Ocean and the Caribbean Sea, which comprises 13 independent island countries, 18 dependencies, and three archipelagos: the Greater Antilles, the Lesser Antilles, and the Lucayan Archipelago. "
text_2 =  text_1 + "The subregion includes all the islands in the Antilles, plus The Bahamas and the Turks and Caicos Islands, which are in the North Atlantic Ocean. "
text_3 = text_2 + (
        "Nowadays, the term West Indies is often interchangeable with the term Caribbean. "
        "However, the term Caribbean may also include some Central and South American mainland nations which have Caribbean coastlines, such as Belize, French Guiana, Guyana, and Suriname, as well as the Atlantic island nations of Barbados, Bermuda, and Trinidad and Tobago. "
        "These countries are geographically distinct from the three main island groups, but culturally related.")


input_file = 'input_video.mp4'
output_file = 'output_video2.mp4'

font_file = 'assets\Roboto\Roboto-Bold.ttf'
font_size = 50
stroke_width = 1

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

add_text_to_video(input_file, output_file, text_instructions,overwrite=True)