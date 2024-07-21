import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

root_dir = "{ROOT_DIR}"

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
    with open(f"{root_dir}/Filtered/{query_type}_{project_name}_filter.json", 'r') as rf:
        commit_data = json.load(rf)

    # Read Google doc excel
    credentials = ServiceAccountCredentials.from_json_keyfile_name(f"{root_dir}/test_google_api.json", scopes)
    file = gspread.authorize(credentials)
    sheet = file.open("Container_Study_Results_Revised")
    
    #########################################
    #### Remember to Change this Config #####
    selectedsheet = sheet.sheet1 # For runc #
    #########################################

    # Analysis of each commit
    useful_keyword = {}
    bad_keyword = {}

    sha_values = selectedsheet.col_values(2)

    for index, col in enumerate(selectedsheet.col_values(1)):
        if col == 'Non':
            sha_value = sha_values[index]
            for commit in commit_data:
                if sha_value == commit["sha"]:
                    for kw in key_words:
                        if kw in commit['title']:
                            if kw in bad_keyword:
                                bad_keyword[kw] += 1
                            else: 
                                bad_keyword[kw] = 1
            print(f"Parse Bad keyword {index} OK")
        else: 
            sha_value = sha_values[index]
            for commit in commit_data:
                if sha_value == commit["sha"]:
                    for kw in key_words:
                        if kw in commit['title']:
                            if kw in useful_keyword:
                                useful_keyword[kw] += 1
                            else: 
                                useful_keyword[kw] = 1
            print(f"Parse Useful keyword {index} OK")

    print(f"The useful keywords: {useful_keyword}")
    print(f"The bad keywords: {bad_keyword}")

    