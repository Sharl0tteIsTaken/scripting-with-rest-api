"""
This script is designed to create issues based on the provided template,
and replace the placeholders with the replacements in placeholder.json.

The `.env` file should contain the following variables and values:
 - ENDPOINT=/repos/{owner}/{repo}/issues
 - NAME=Your_GitHub_UserName
 - TOKEN=Your_GitHub_Fine_Grained_Personal_Access_Token
 - DATA_FOLDER=assets
 - TEMPLATE_FNAME_1=template-create_issue-angle.txt
 - TEMPLATE_FNAME_2=template-create_issue-format.txt
 - PLACEHOLDER=placeholder-create_issue.json
"""

import json
import os
import time
from pathlib import Path
from typing import Literal

# Note: All the comments around the line `import requests` are to
# suppress static type checker warnings (unused import).
# pylint: disable-next=unused-import
import requests  # pyright: ignore[reportUnusedImport],  # noqa: F401

# Custom types
type Cases = Literal["case 1", "case 2"]
type FileTypes = Literal["README", "cli tool tutorials"]
type IssueTarget = Literal["angle bracket", "format"]
type PlaceholderType = dict[str, list[dict[str, str]]]


# Dash Board (To run the script for different settings, modify here)
# !==========================================!
FILE_TYPE: FileTypes = "cli tool tutorials"
PURPOSE: IssueTarget = "format"
# !==========================================!

# Script Enum
ISSUE: dict[Cases, IssueTarget] = {
    "case 1": "angle bracket",
    "case 2": "format",
}
FILE: dict[Cases, FileTypes] = {
    "case 1": "README",
    "case 2": "cli tool tutorials",
}

# Final product (issue) related constant
TITLE_1 = "Fix angle brackets within HTML <pre> tag in {language} translation"
TITLE_2 = "Fix formatting problem in the {language} translation"
TITLE = TITLE_1 if PURPOSE == ISSUE["case 1"] else TITLE_2

LABELS = ['documentation', 'help wanted', 'good first issue', 'enhancement']
FNAME = FILE_TYPE


# Error message
ERRMSG = "Environment variable `{var}` don't exist, check `.env` file."

# Script related constant
SELECTED_SETTING = FILE_TYPE + " - " + PURPOSE

DATA_FOLDER = os.getenv("DATA_FOLDER")
TEMPLATE_FNAME_1 = os.getenv("TEMPLATE_FNAME_1")
TEMPLATE_FNAME_2 = os.getenv("TEMPLATE_FNAME_2")
PLACEHOLDER = os.getenv("PLACEHOLDER")
assert isinstance(DATA_FOLDER, str), ERRMSG.format(var="DATA_FOLDER")
assert isinstance(TEMPLATE_FNAME_1, str), ERRMSG.format(var="TEMPLATE_FNAME_1")
assert isinstance(TEMPLATE_FNAME_2, str), ERRMSG.format(var="TEMPLATE_FNAME_2")
assert isinstance(PLACEHOLDER, str), ERRMSG.format(var="PLACEHOLDER")

SUB_DIR = TEMPLATE_FNAME_1 if PURPOSE == ISSUE["case 1"] else TEMPLATE_FNAME_2
PATH_TEMPLATE = os.path.join(DATA_FOLDER, SUB_DIR)
PATH_PLACEHOLDER = os.path.join(DATA_FOLDER, PLACEHOLDER)


# GitHub Rest API related constant
ENDPOINT = os.getenv("ENDPOINT")
NAME = os.getenv("NAME")
TOKEN = os.getenv("TOKEN")
assert isinstance(ENDPOINT, str), ERRMSG.format(var="ENDPOINT")
assert isinstance(NAME, str), ERRMSG.format(var="NAME")
assert isinstance(TOKEN, str), ERRMSG.format(var="TOKEN")

HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": TOKEN,
    "Content-Type": "application/json",
    "User-Agent": NAME,
    "X-GitHub-Api-Version": "2022-11-28",
}


# Other constans
ENCODE = "UTF-8"
OUTPUT = "previews"  # output folder directory


Path(OUTPUT).mkdir(exist_ok=True)
params: dict[str, str | list[str]] = {}
with open(PATH_PLACEHOLDER, encoding=ENCODE) as file:
    placeholders: dict[str, list[dict[str, str]]] = json.load(file)

for placeholder in placeholders[SELECTED_SETTING]:
    placeholder['file'] = FNAME

    time.sleep(3)  # Prevents secondary rate limiting [^1]_

    params["title"] = TITLE.format(**placeholder)
    with open(PATH_TEMPLATE, encoding=ENCODE) as template:
        text = template.read()
        params['body'] = text.format(**placeholder)
    params["labels"] = LABELS

    # For testing, output to a file instead of actually creating
    # pylint: disable-next=invalid-name
    fname = f"{SELECTED_SETTING} - {placeholder.get("language")}"
    save_dir = os.path.join(os.getcwd(), OUTPUT, fname + ".md")
    print(f"processing file: {fname}")
    with open(save_dir, mode="w", encoding=ENCODE) as save_file:
        save_file.write(
            "<!--" + "\n"  # type: ignore[operator]
            + params["title"] + "\n"
            + "labels: " + ", ".join(params["labels"]) + "\n" + "-->" + "\n\n"
            + params["body"]
        )
    # Note: Title and labels was commented out for easier preview.
    # Markdown can be used in the GitHub web interface, and markdown
    # support HTML comments. So HTML comment syntax was used here.

    # Uncomment the following lines to actually create issues
    # response = requests.post(
    #     url=ENDPOINT, auth=(NAME, TOKEN), headers=HEADERS, json=params,
    #     timeout=10
    #     )
    # response.raise_for_status()

    # print("="*20)
    # print(f"{response.headers=}")
    # print(f"{response.text=}")
    # print(f"{response.status_code=}")
    # print("="*20 + "\n")


# pylint: disable-next=pointless-string-statement
"""
Footnotes:
[^0]: GitHub: PyGithub
    Source: https://github.com/PyGithub/PyGithub
    Usage:
     - What parameters to use in requests
     - What value to pass into parameters in requests
[^1]: docs.github.com: REST API
    Source:   https://docs.github.com/en/rest
    Document: Best practices for using the REST API
    Chapter:  Pause between mutative requests
"""
