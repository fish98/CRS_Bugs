<p align="center">

  <h1 align="center">Bugs in Pods: Understanding Bugs in Container Runtime Systems</h1>
  <div>This repository contains all the data collection, commit extraction, and analysis code used in the study of bugs in Container Runtime Systems, detailed in the paper "Bugs in Pods: Understanding Bugs in Container Runtime Systems". The paper is accepted at The 33rd ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA 2024)</div>
    <br>
  <div>Authors: Jiongchi Yu, Xiaofei Xie, Cen Zhang, Sen Chen, Yuekang Li, Wenbo Shen</div>

  <p align="center">
  <br>
    <a href="https://sites.google.com/view/understand-bugs-in-crs"><strong>Project Page</strong></a>
    |
    <a href="https://2024.issta.org/details/issta-2024-papers/109/Bugs-in-Pods-Understanding-Bugs-in-Container-Runtime-Systems"><strong>Paper</strong></a>
  </p>
</p>

---

The code is designed to facilitate the analysis of open-source projects. The instructions provided below are provided to help reproduce the results of RQ1-RQ3 from the paper. Note that the code can be easily adapted for analyzing other open-source projects with minimal modifications to the configuration file.

## Overview

<div>
<img src="./img/Methodology.png     ">
</div>

## Requirements

To run scripts locally, it is suggested to prepare `Python 3.8` and `Go 1.21.5` (or newer version) on the system.

```bash
git clone https://github.com/fish98/container_bugs.git
cd container_bugs
mkdir Source_Code Test Sample Collection # For storing experiment data
pip install -r requirements.txt
```

## Experiment Instructions

1. **Replace ALL the placeholder `{ROOT_DIR}` in the source with the path to the source code of this project.** (e.g., `root_dir = "/root/container_bugs`)

2. The config file for the project could be changed for analyzing different open-source project. The example is shown below:
```json
{
    "access_token": "ghp_xxxxxxxxxxxxxxxxxx",  // Github personal access token.
    "project_author": "opencontainers",  // Github project author/organization name.
    "project_name": "runc",   // Github project name.
    "query_type": "commits",  // Collect commit data on Github. Could support PRs and Issues on Github.
    "page_num": 1,  // The number of the starting page for collecting the data.  
    "per_page": 100,  // The number of commits to display on a page.
    "google_doc_sheet": 7,  // The number of sheet of the google sheet would be updated.
    "limit_time_d": "2021-06-01",  // The collected data would be later than this date.
    "limit_time_u": "2023-06-01"   // The collected data would be earlier than this date.
}   
```

### Data Collection

To collect all the commit information from Github:

1. Change the project config in the `config.json`, especially for the Github Access Token config `"access_token": "ghp_xxxxxxxxxxxxxxxxxx"`. [How to get Github personal access token?](https://docs.github.com/en/enterprise-server@3.9/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

2. Run the following command:
```bash
python src/collect_github_commits.py
```

**As the collecting speed is subject to the Github api accesss limit.** For the convenienance of reproducing our expereimetn data, you can directly download the result of the collected commits data from [our anoymous Google Drives](https://drive.google.com/file/d/1jPStGOg3HYCtqdNmznVzMDqHucGneK0N/view?usp=sharing), and Extracted the content into the `Collection` directory for further analysis.

### Filter Commit

1. Run the following command:
```bash
python src/filter_commits.py
```

### Extract Tests

1. Replace the `repoName` (e.g., runc) in `AST/extract_ast.go` with the corresponding project name.
2. Pull the project source code with Git into `Source_Code/{project_name}`
3. Run the following command:
```bash
python -u AST/bug2test.py 1 > bug2test-{project_name}.log 2>&1
```
* Note that `{project_name}` is just the placeholder for the real project name.

## Tools

### Tool for Manual Analysis

1. Run the following command:
```bash
python read_sample_commits.py
```

### Updating Google Sheet
1. Change `sheet_name` in `src/update_gdoc.py` and prepare the google API account
2. Set the shared user permission of google API, and prepare the Google Sheet Number with the official json file (e.g., test_google_api.json)
3. Replace the `google_doc_sheet` as the google sheet id in `config.json`
4. Run the following command:
```bash
python src/update_gdoc.py
```

# Citation

Cite as below if you find this repository is helpful to your project:

```
@inproceedings {yu2024bugs,
    title      = {Bugs in Pods: Understanding Bugs in Container Runtime Systems},
    author     = {Jiongchi Yu and Xiaofei Xie and Cen Zhang and Sen Chen and Yuekang Li and Wenbo Shen},
    booktitle  = {Proceedings of the 33rd ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA)},
    year       = {2024}
}