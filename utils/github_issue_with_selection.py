# python 3.10-4

# Github Commits for Runc
# Total Commits: 6120
# Records: 2158 Commits: 1730


from urllib import response
import requests
import json

key_words = ["fix", "defect", "error", "bug", "issue", "mistake", "incorrect", "fault",  "flaw"]

if __name__ == '__main__':
    
    result_commits = []

    project_name = "containerd" # "runc"
    project_author = "containerd" # "opencontainers"
    page_num = 1
    per_page = 100
    query_type = "commits" # pulls # issues # commits
    
    access_token = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxx"
    heads = {"Authorization": "token " + access_token}

    while(1):

        site = f"https://api.github.com/repos/{project_author}/{project_name}/{query_type}?page={page_num}&per_page={per_page}"
        try:
            response = requests.get(site, headers=heads)
        except Exception as e:
            print(e)

        data = response.json()

        if(data == []):
            print("All commits parsed")
            break
        if query_type == "commits":
            for commit_data in data:
                # Check Messages contain key words
                for kw in key_words:
                    if kw in commit_data['commit']['message']:
                        result_commits.append({kw: commit_data['sha'], "title": commit_data['commit']['message']}) # result_commits.append({kw: commit_data['sha']}+'\n')
                        break
            print("Parse page {} Down".format(page_num))
        elif query_type == 'issues':
            for commit_data in data:
                # Check Messages contain key words
                for kw in key_words:
                    if kw in commit_data['title']:
                        result_commits.append((commit_data['url'], kw))
                        break
            print("Parse page {} Down".format(page_num))
        elif query_type == 'pulls':
            for commit_data in data:
                # Check Messages contain key words
                for kw in key_words:
                    if kw in commit_data['title']:
                        result_commits.append((commit_data['url'], kw))
                        break
            print("Parse page {} Down".format(page_num))

        page_num = page_num + 1
        
    print(len(result_commits))

    json_result = json.dumps(result_commits)
    with open(f'./{query_type}_{project_name}_result.json', 'w') as p:
        p.write(json_result)
