import webcolors

#doesnt work oops
def hex_to_color_name(hex_color):
    try:
        # Convert hex color code to the closest CSS3 color name
        color_name = webcolors.hex_to_name(hex_color, spec='css3')
    except ValueError:
        # If there is no exact match, find the closest color name
        rgb_color = webcolors.hex_to_rgb(hex_color)
        # Find the closest CSS3 color name
        color_name = webcolors.rgb_to_name(rgb_color, spec='css3')

    return color_name


# Example usage
hex_color = "#010101"
color_name = hex_to_color_name(hex_color)
print(f"Hex color {hex_color} is closest to color name {color_name}")
