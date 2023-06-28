import openpyxl
import pandas

workbook = openpyxl.load_workbook('/home/misteryoh/Coding/Git/ccee-infomercado/data/InfoMercado.xlsx', read_only=True)

sheet = workbook['002 Usinas']

first_col_identifier = "Código do Ativo"
last_col_identifier = "Geração por Unit Commitment"
foot_row_identifier = "Topo"

start_cell = None
last_cell = None
foot_cell = None

for row in sheet.iter_rows():
    for cell in row:
        if first_col_identifier in str(cell.value):
            start_cell = cell
        if last_col_identifier in str(cell.value):
            last_cell = cell
        if foot_row_identifier in str(cell.value):
            foot_cell = cell
            break

print("start_cell  : " + start_cell.coordinate)
print("last_cell   : " + last_cell.column_letter + str(foot_cell.row - 3))

data_rows = []
for row in sheet[f'{start_cell.coordinate}':f'{last_cell.column_letter + str(foot_cell.row - 3)}']:
    data_cols = []
    for cell in row:
        data_cols.append(cell.value)
    data_rows.append(data_cols)

df = pandas.DataFrame(data_rows)

df.columns = df.iloc[0]
df = df[1:]

print(df.head())