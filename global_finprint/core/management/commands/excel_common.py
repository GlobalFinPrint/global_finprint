"""
Collection of functions used for working with openpyxl.
"""

from datetime import datetime
import openpyxl

def open_workbook(file_name, read_only=False):
    return openpyxl.load_workbook(file_name, data_only=True, read_only=read_only)

def get_cell_by_name_extractor(headers):
    extractor_func = lambda row, column_name: row[headers[column_name]]
    return extractor_func

def get_cell_value(cell):
    result = cell.value
    if result:
        result = result.strip()
    return result

def get_header_map(header_row):
    result = {}
    for idx, header in enumerate(header_row):
        if header.value:
            result[header.value.strip()] = idx
    return result

def get_float_from_cell(cell):
    result = None
    if isinstance(cell.value, str):
        result = float(cell.value)
    else:
        result = cell.value
    return result

def get_date_from_cell(cell):
    result = cell.value
    if isinstance(result, str):
        result = datetime.strptime(cell.value, '%d/%m/%Y')
    return result
    
def get_time_from_cell(cell, format_str='%H:%M:%S %p'):
    result = cell.value
    if isinstance(result, str):
        for format_string in ['%H:%M:%S %p', ':%M', '%M:%Ss', '%M:%S']:
            try:
                result = datetime.strptime(result, format_string).time()
                break
            except ValueError:
                pass
        else:
            raise ValueError('Unable to parse time: "{}"'.format(result))
    return result
