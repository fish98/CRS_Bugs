# python 3.10-4

# Github Commits for Runc

import random
import json

mode = "Sample" # Filtered Collection

root_dir = "{ROOT_DIR}"

key_words = ["fix", "defect", "error", "bug", "issue", "mistake", "incorrect", "fault",  "flaw"]
filter_words = ['merge','pr ','pr-', 'pull request', 'Merge']
filter_files = ['.cirrus.yml', '.github/']

class FilterResult():
    def __init__(self, keywords):
        # self.counter = 0
        self.keywords = keywords
        self.keywords_distribution = {}
        self.time_result_commit = []
        self.result_commit = []

        # for filtered commits
        self.filter_keyword_commit = []
        self.filter_file_commit = []
        self.final_commit = []

    # todo: fix unified update result
    def update_result(self, commit):
        if commit not in self.result_commit:
            self.result_commit.append(commit)

    def update_keyword(self, commit):
        for kw in self.keywords:
            if(kw in commit['title']):
                if kw in self.keywords_distribution:
                    self.keywords_distribution[kw] = self.keywords_distribution[kw] + 1
                else:
                    self.keywords_distribution[kw] = 1
                self.update_result(commit)

    def filter_keyword(self, commit):
        for kw in filter_words:
            if(kw in commit['title']):
                if commit not in self.filter_keyword_commit:
                    self.filter_keyword_commit.append(commit)
            # else:
            #     if commit not in self.final_commit_1:
            #         self.final_commit_1.append(commit)

    def filter_file(self, commit):
        for kw in filter_files:
            if(kw in str(commit['changed_files'])):
                if commit not in self.filter_file_commit:
                    self.filter_file_commit.append(commit)
            # else:
            #     if commit not in self.final_commit_2:
            #         self.final_commit_2.append(commit)
    
    def get_final(self):
        for commit in self.result_commit:
            if commit not in self.filter_file_commit and commit not in self.filter_keyword_commit:
                self.final_commit.append(commit)
    
    def save_result(self):
        json_result = json.dumps(self.final_commit)
        with open(f'{root_dir}/{mode}/{query_type}_{project_name}_filter.json', 'w') as p:
            p.write(json_result)

    def update_time(self, commit, limit_time_d, limit_time_u):
        if commit['time'] >  limit_time_d and commit['time'] < limit_time_u:
            if commit not in self.time_result_commit:
                self.time_result_commit.append(commit)

if __name__ == '__main__':
    
    FR = FilterResult(key_words)

    with open(f'{root_dir}/config.json', 'r') as jf:
        config_data = json.load(jf)

    project_name = config_data['project_name']
    project_author = config_data['project_author']
    query_type = config_data['query_type']

    limit_time_u = config_data['limit_time_u']
    limit_time_d = config_data['limit_time_d']
    # Select full json
    with open(f"{root_dir}/Collection/{query_type}_{project_name}_full_result.json", 'r') as rf:
        commit_data = json.load(rf)
    
    # Add Time Select Feature
    for commit in commit_data:
        FR.update_time(commit, limit_time_d, limit_time_u)
    print(f"The remained commit number is {len(FR.time_result_commit)} / {len(commit_data)}")

    # Select with Keywords 
    for commit in FR.time_result_commit:
        # print(len(FR.time_result_commit))
        FR.update_keyword(commit)

    for commit in FR.result_commit:
        FR.filter_keyword(commit)
        FR.filter_file(commit)
    
    FR.get_final()

    # Print out the result
    print(FR.keywords_distribution)
    print(f"The total selected keywords number is {len(FR.result_commit)} / {len(commit_data)}")
    print(f"The total filtered keywords number is {len(FR.final_commit)} / {len(commit_data)}")

    # Save Result to Filter
    FR.save_result()