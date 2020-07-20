import pandas as pd

xls = pd.ExcelFile("./data/Fulldata.xlsx")
data = pd.read_excel(xls)

print((data.columns))

#4204 site 1

for name in data["name"]:
    if name.find("4204") > 0:
        print((data[data["name"] == name]))
