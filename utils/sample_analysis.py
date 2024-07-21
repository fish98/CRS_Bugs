# python 3.10-4

import json
import random

if __name__ == '__main__':

#   File name specifications
    project_name = "runc" # "runc"
    project_author = "opencontainers" # "opencontainers"
    query_type = "commits" # pulls # issues # commits

    sample_number = 1718

    sample_commits = []

    with open(f'./{query_type}_{project_name}_result.json', 'r') as p:
        data = json.loads(p.read())
    
    selected = []
    for i in range(sample_number):
        selectIdx = random.randint(0, sample_number)
        while(1):
            # selected.append(selected)
            # if (selected in selecte)
            if selectIdx not in selected:
                selected.append(selectIdx)
                break
            else:
                selectIdx = random.randint(0, sample_number)
        sample_commits.append(data[selectIdx])
    
    with open(f'./sample_{sample_number}_{query_type}_{project_name}_result.json', 'w') as pw:
        pw.write(json.dumps(sample_commits))

        