import pandas as pd # type: ignore
import json
from openpyxl import load_workbook
from PIL import Image, ImageDraw


# goal is to import ARC_input1, excel file that i manually coloured, in JSON format. write a function that solves it and then return a JSON output that I can open in excel

input_data=[]
starting_point = ""
BLUE = "FF0070C0"
RED = "FFD86DCD"
GREEN = "FF00B050"

# load the excel file
input_file = load_workbook('ARC_input1.xlsx')
sheet = input_file.active
# go through 10x10 cells (bc size is always 10x10 in this problem) and extract color codes
for row in sheet.iter_rows(1,10):
    for cell in row:
        color = cell.fill.start_color.index
        input_data.append({"id": cell.coordinate, "color": color})
        if color == BLUE:
            starting_point = cell.coordinate
#print(starting_point)

"""
next step is to solve the problem: startting from only blue(FF0070C0) cell going towards right until reaching red(FFD86DCD) or green(FF00B050) or a uncoloured border to stop. 
whhen reaching red direction changes to 90 degrees counterclockwise. when reaching green direction changes to 90 degrees clockwise. 
and colours of white(normally FFFFFFFF but in jsondata it is 00000000 for some reason) cells along the way changes to blue(FF0070C0). if it reaches blue, it keeps going in the same direction.
"""

# create 10x10 grid made of colors from input
grid = []
for i in range(10):
    grid_row = []
    for j in range(10):
        grid_row.append(input_data[i * 10 + j]["color"])
    grid.append(grid_row)

#print(grid)

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
direction = 0

# converts excel coordinate to row and column (makes it from 0 to 9)
start_row = int(''.join(filter(str.isdigit, starting_point))) - 1 
start_col = ord(''.join(filter(str.isalpha, starting_point))) - ord('A')

row = start_row
col = start_col

#move until reaching border, change direction when reached green or red
while 0 <= row < 10 and 0 <= col < 10:
    color = grid[row][col]
    if color == GREEN:
        direction = (direction + 1) % 4
    elif color == RED:
        direction = (direction - 1) % 4
    elif color == BLUE:
        direction = direction
    else:
        direction = direction
        grid[row][col] = BLUE

    #print(row, col)
    row_direction, col_direction = directions[direction]
    row += row_direction
    col += col_direction

#print(grid)

#i'll try an output version i found on stack overflow
image = Image.new('RGB', (1000, 1000), 'white')
width, height = image.size

rectangle_width = 100
rectangle_height = 100
draw_image = ImageDraw.Draw(image)
for i in range(10):
    for j in range(10):
        rectangle_x = i*rectangle_width
        rectangle_y = j*rectangle_height
    
        color = grid[j][i]

        if color == BLUE:
            rgb_color = (0, 112, 192)
        elif color == RED:
            rgb_color = (216, 109, 205)
        elif color == GREEN:
            rgb_color = (0, 176, 80)
        else:
            rgb_color = (255, 255, 255)

        rectangle_shape = [(rectangle_x, rectangle_y), (rectangle_x + rectangle_width - 1, rectangle_y + rectangle_height - 1)]
        draw_image.rectangle(rectangle_shape, fill=rgb_color, outline=(0, 0, 0))


image.save('output.png')

image.show()