import pandas as pd
import logging
from tqdm import tqdm
import concurrent.futures

df = pd.read_excel('Board_comparison_results.xlsx')

removed_items = df[df['Status'] == 'Removed Item'].copy()
new_items = df[df['Status'] == 'New Item'].copy()

replaced_items = []
def remove_matching_rows(input_excel):
    xls = pd.ExcelFile(input_excel)
    sheets_dict = pd.read_excel(xls, sheet_name=None)
    
    sheet1 = sheets_dict['Original Data']
    sheet2 = sheets_dict['Replaced Items']

    column_l_values = sheet1['Serial Number']

    for value in column_l_values:
        if (sheet2['Old Serial Number'] == value).any() or (sheet2['New Serial Number'] == value).any():
            sheet1 = sheet1[sheet1['Serial Number'] != value]

    with pd.ExcelWriter(input_excel, engine='openpyxl') as writer:
        for sheet_name, df_sheet in sheets_dict.items():
            if sheet_name == 'Original Data':
                sheet1.to_excel(writer, sheet_name=sheet_name, index=False)
            else:
                df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)

def clean_header(column_number):
    header = df.columns[column_number]
    parts = header.split()
    if len(parts) == 2 and parts[0] == "NEName":
        date = parts[1]
        return date
    else:
        return None

def check_values(row):
    global df
    for removed_row in removed_items.itertuples():
        if row[15] == "New Item" and (row[13] == removed_row[13] or row[14] == removed_row[13]):  
            if (row[3] == removed_row[4] and  
                row[4] == removed_row[5] and 
                row[5] == removed_row[6] and
                row[1] == removed_row[2]): 
                
                old_header = clean_header(12)
                new_header = clean_header(13 if row[13] == removed_row[13] else 14)
                
                replaced_items.append({
                    'NEName': removed_row[13],  
                    'Old Serial Number': removed_row[12],
                    'New Serial Number': row[11],
                    "Old Serial Date": old_header,
                    "New Serial Date": new_header,
                    'NEType': row[0],  
                    'Board Name': row[1],  
                    'Board Type': row[2],  
                    'Cabinet No.': row[3],  
                    'Subrack No.': row[4],  
                    'Slot No.': row[5],  
                    'PN(BOM Code/Item)': row[6],  
                    'Manufacturer Data': row[7],  
                    'Vendor Name': row[8],  
                    'Vendor Unit Family Type': row[9],  
                    'Hardware Version': row[10],  
                    'Status': 'Replaced',  
                })
                df = df[~df.index.isin([removed_row.index, row.index])]
                break

results = list(tqdm(concurrent.futures.ThreadPoolExecutor().map(check_values, new_items.itertuples(index=False)), total=len(new_items)))

writer = pd.ExcelWriter('Board_analysis_results.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Original Data', index=False)
replaced_df = pd.DataFrame(replaced_items)
replaced_df.to_excel(writer, sheet_name='Replaced Items', index=False)
writer._save()
remove_matching_rows('Board_analysis_results.xlsx')
