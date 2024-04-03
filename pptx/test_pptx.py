from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation()
title_only_slide_layout = prs.slide_layouts[5]
slide = prs.slides.add_slide(title_only_slide_layout)
shapes = slide.shapes

shapes.title.text = 'Adding a Table'

item_ = ['OSD 操作介面','SYS 系統行為', 'Audio 爆音異音', 'PQ 畫質相關', 'Video 畫異、閃屏','待處理', 'Total' ]
number_ = [10, 25, 2, 4, 1, 3, 41]

cols = len(item_)
rows = 2
left = top = Inches(2.0)
width = Inches(6.0)
height = Inches(0.8)

table = shapes.add_table(rows, cols, left, top, width, height).table

# set column widths
# table.columns[0].width = Inches(2.0)
# table.columns[1].width = Inches(4.0)

for i in range(0,len(item_)):
    table.columns[i].width = Inches(1.2)
    table.cell(0, i).text = item_[i]

for i in range(0,len(item_)):
    table.cell(1, i).text = str(number_[i])


prs.save('test.pptx')