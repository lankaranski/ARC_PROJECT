import pandas as pd
import json
from openpyxl import load_workbook

# goal is to import ARC_input1, excel file that i manually coloured, in JSON format. write a function that solves it and then return a JSON output that I can open in excel

data=[]

# load the excel file
workbook = load_workbook('ARC_input1.xlsx')
sheet = workbook.active
# go through 10x10 cells (bc size is always 10x10 in this problem) and extract color codes
for row in sheet.iter_rows(1,10):
    for cell in row:
        color = cell.fill.start_color.index
        data.append({"id": cell.coordinate, "color": color})


print(data)