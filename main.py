import pandas as pd
from scraper import principal
import xlwt
from xlwt import Workbook

principal()

"""
#vreau sa testez xlwt
wb=xlwt.Workbook()
sheet1=wb.add_sheet("sheet1", cell_overwrite_ok=False)
sheet1.write(1,1, "ceva text")
wb.save("test.xlsx")
"""