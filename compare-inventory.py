import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

compare_serial = 'SN(Bar Code)'

def clean_ne_name(ne_name):
    if ne_name.startswith("MBTS_"):
        ne_name = ne_name.replace('MBTS_', '')
    if ne_name.startswith('U'):
        ne_name = ne_name[1:]
    if ne_name.startswith('DBTS_'):
        ne_name = ne_name.replace('DBTS_', '')
    if ne_name.startswith('L'):
        ne_name = ne_name[1:]
    if ne_name.startswith('D'):
        ne_name = ne_name[1:]
    if 'X' in ne_name:
        index = ne_name.index('X')
        ne_name = ne_name[:index+1]
    
    return ne_name

def get_additional_info(sn_barcode, file):
    rows = file[file[compare_serial] == sn_barcode]
    if len(rows) > 0:
        row = rows.iloc[0]
        return {key: row[key] for key in row.index if key not in [compare_serial, 'NEName']}
    else:
        return {}

def get_status(ne_name1, ne_name2, ne_name3):
    if ((ne_name1 != "N/A" and ne_name2 != "N/A" and ne_name1 != ne_name2) or
          (ne_name2 != "N/A" and ne_name3 != "N/A" and ne_name2 != ne_name3) or 
          (ne_name1 != "N/A" and ne_name3 != "N/A" and ne_name1 != ne_name3)):
        return 'Swap Item'
    if ne_name3 != 'N/A' and (ne_name1 == 'N/A' and ne_name2 == 'N/A'):
        return 'New Item'
    if ne_name3 != 'N/A' and (ne_name1 == 'N/A' and ne_name2 != 'N/A'):
        return 'New Item'
    if ne_name3 != 'N/A' and ne_name1 == 'N/A' and ne_name2 != 'N/A' and (ne_name2 == ne_name3):
        return 'New Item'
    elif ne_name1 != 'N/A' and ne_name2 != 'N/A' and ne_name3 == 'N/A':
        return 'Removed Item'
    elif ne_name1 != 'N/A' and ne_name2 == 'N/A' and ne_name3 == 'N/A':
        return 'Removed Item'
    elif ne_name1 != 'N/A' and ne_name2 != 'N/A' and (ne_name1 != ne_name2 or ne_name2 != ne_name3):
        return 'Moved Item'
    else:
        return 'Others'

item = "Board"
RDate3 = "22_06_2024"
RDate2 = "04_05_2024"
RDate1 = "27_04_2024"


Date1 = f"NEName {RDate1}"
Date2 = f"NEName {RDate2}"
Date3 = f"NEName {RDate3}"

file1 = pd.read_csv(f'{RDate1}/Huawei_Inventory_{item}.csv', low_memory=False)
file2 = pd.read_csv(f'{RDate2}/Huawei_Inventory_{item}.csv', low_memory=False)
file3 = pd.read_csv(f'{RDate3}/Huawei_Inventory_{item}.csv', low_memory=False)

file1.columns = file1.columns.str.strip()
file2.columns = file2.columns.str.strip()
file3.columns = file3.columns.str.strip()

file1['NEName'] = file1['NEName'].apply(clean_ne_name)
file2['NEName'] = file2['NEName'].apply(clean_ne_name)
file3['NEName'] = file3['NEName'].apply(clean_ne_name)

sn_barcode_set_file1 = set(file1[compare_serial])
sn_barcode_set_file2 = set(file2[compare_serial])
sn_barcode_set_file3 = set(file3[compare_serial])

nenames_file1 = dict(zip(file1[compare_serial], file1['NEName']))
nenames_file2 = dict(zip(file2[compare_serial], file2['NEName']))
nenames_file3 = dict(zip(file3[compare_serial], file3['NEName']))

comparison_results = []

def fetch_info_and_update(sn_barcode):
    additional_info = {}
    ne_name_file1 = nenames_file1.get(sn_barcode, 'N/A')
    ne_name_file2 = nenames_file2.get(sn_barcode, 'N/A')
    ne_name_file3 = nenames_file3.get(sn_barcode, 'N/A')
    
    status = get_status(ne_name_file1, ne_name_file2, ne_name_file3)
    
    if ne_name_file1 != ne_name_file2 or ne_name_file1 != ne_name_file3:
        if sn_barcode in sn_barcode_set_file1:
            additional_info = get_additional_info(sn_barcode, file1)
        elif sn_barcode in sn_barcode_set_file2:
            additional_info = get_additional_info(sn_barcode, file2)
        else:
            additional_info = get_additional_info(sn_barcode, file3)
        
        additional_info['Serial Number'] = sn_barcode
        additional_info[Date1] = ne_name_file1
        additional_info[Date2] = ne_name_file2
        additional_info[Date3] = ne_name_file3
        additional_info['Status'] = status
        comparison_results.append(additional_info)

with ThreadPoolExecutor() as executor:
    list(tqdm(executor.map(fetch_info_and_update, sn_barcode_set_file1.union(sn_barcode_set_file2).union(sn_barcode_set_file3)), total=len(sn_barcode_set_file1.union(sn_barcode_set_file2).union(sn_barcode_set_file3)), desc="Fetching Additional Info"))

comparison_df = pd.DataFrame(comparison_results)
comparison_df.to_excel(f'{item}_comparison_results.xlsx', index=False)
