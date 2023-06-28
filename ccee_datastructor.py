import openpyxl
import pandas

def lambda_handler(event, context):

    """Extract structured data from downloaded file from CCEE
    Payload exemple
    {
        "filepath"    : "/home/misteryoh/Coding/Git/ccee-infomercado/data",
        "filename"    : "InfoMercado.xlsx",
        "profile"     : "default",
        "params" : {
            "sheet_name" : "002 Usinas",
            "table_name" : "Tabela 001",
            "first_col"  : "Código do Ativo",
            "last_col"   : "Geração por Unit Commitment",
            "footer"     : "Topo"
        }
    }
    """

    filepath = event['filepath']
    filename = event['filename']
    profile = event['profile']
    params = event['params']

    workbook = openpyxl.load_workbook(filepath + "/" + filename, read_only=True)

    sheet = workbook[params['sheet_name']]

    title_cell = params['table_name']
    first_cell = params['first_col']
    last_cell = params['last_col']
    footer_cell = params['footer']

    title_range = None
    start_range = None
    last_range = None
    foot_range = None

    for row in sheet.iter_rows():
        for cell in row:
            if title_cell in str(cell.value):
                title_range = cell
            if first_cell in str(cell.value):
                start_range = cell
            if last_cell in str(cell.value):
                last_range = cell
            if footer_cell in str(cell.value):
                foot_range = cell
                break

    print("title_range  : " + title_range.coordinate)
    print("start_range  : " + start_range.coordinate)
    print("last_range  : " + last_range.coordinate)
    print("foot_range   : " + foot_range.coordinate)

    data_rows = []
    if title_range.value is not None:
        for row in sheet[f'{start_range.coordinate}':f'{last_range.column_letter + str(foot_range.row - 3)}']:
            data_cols = []
            for cell in row:
                data_cols.append(cell.value)
            data_rows.append(data_cols)
    else:
        print("Algo deu errado")

    df = pandas.DataFrame(data_rows)

    return df


payload = {
    "filepath"    : "/home/misteryoh/Coding/Git/ccee-infomercado/data",
    "filename"    : "InfoMercado.xlsx",
    "profile"     : "default",
    "params" : {
        "sheet_name" : "002 Usinas",
        "table_name" : "Tabela 001",
        "first_col"  : "Código do Ativo",
        "last_col"   : "Geração por Unit Commitment",
        "footer"     : "Topo"
    }
}

df = lambda_handler(event=payload, context=None)

print(df.head())