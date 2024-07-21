import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import time

root_dir = "{ROOT_DIR}"

mode = "Sample"

sheet_name = "ISSTA2024 CRS Empirical Study"

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

key_words = ["fix", "defect", "error", "bug", "issue", "mistake", "incorrect", "fault",  "flaw"]

if __name__ == '__main__':

    with open(f'{root_dir}/config.json', 'r') as jf:
        config_data = json.load(jf)

    project_name = config_data['project_name']
    query_type = config_data['query_type']

    # Read filtered json 
    with open(f"{root_dir}/{mode}/{query_type}_{project_name}_filter.json", 'r') as rf:
        data = json.load(rf)

    # Read Google doc excel
    credentials = ServiceAccountCredentials.from_json_keyfile_name(f"{root_dir}/test_google_api.json", scopes)
    file = gspread.authorize(credentials)
  
    sheet = file.open(sheet_name)
    
    #########################################
    #### Remember to Change this Config #####
    sheet_id = config_data['google_doc_sheet']
    worksheet = sheet.get_worksheet(sheet_id-1)
 
    print(worksheet)
    # print(f'Read Google Doc Sheet {sheet_id} Successful')
    #########################################