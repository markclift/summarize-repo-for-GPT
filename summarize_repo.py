#!/usr/bin/env python3

import os
import tkinter as tk
from tkinter import simpledialog, filedialog
from github import Github
import requests
from dotenv import load_dotenv

ROOT = tk.Tk()
ROOT.withdraw()

load_dotenv()

USER_TOKEN = os.getenv('GITHUB_TOKEN')

IGNORED_FILES=['.gitignore', 'package-lock.json', 'tsconfig.json', 'vercel.svg', 'favicon.ico']

def get_all_files_recursive(repo, path=''):
    output = ''
    contents = repo.get_contents(path)

    for content in contents:
        if content.type == 'dir':
            output += get_all_files_recursive(repo, content.path)
        else:
            if content.name not in IGNORED_FILES:
                output += "File path: " + content.path + '\nFile content:\n\n'
                output += get_content_of_file(content.download_url)
                output += "\n\n===============================\n\n"

    return output

def get_content_of_file(file_url):
    response = requests.get(file_url)

    # Try to decode the content to text
    try:
        response.content.decode('utf-8')
    except UnicodeDecodeError:
        # If decoding fails, it's likely a binary file, so return an empty string
        return ''
    else:
        # If decoding succeeds, it's likely a text file, so return the content
        return response.text


def main():
    repo_url = simpledialog.askstring(title="Github Repo",
                                      prompt="Please enter the Github Repo URL:")

    repo_name = repo_url.split('https://github.com/')[-1]
    g = Github(USER_TOKEN)
    repo = g.get_repo(repo_name)

    output = get_all_files_recursive(repo)

    file_path = filedialog.asksaveasfilename(defaultextension='.txt', 
                                             filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')])

    with open(file_path, 'w') as f:
        f.write(output)

if __name__ == "__main__":
    main()