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

IGNORED_FILES = ['.gitignore', 'package-lock.json', 'tsconfig.json', 'vercel.svg', 'favicon.ico']

def get_all_files_recursive(repo, path='', selected_extensions=None):
    output = ''
    extensions = set()
    contents = repo.get_contents(path)

    for content in contents:
        if content.type == 'dir':
            new_output, new_extensions = get_all_files_recursive(repo, content.path, selected_extensions)
            output += new_output
            extensions.update(new_extensions)
        elif content.name not in IGNORED_FILES:
            extension = os.path.splitext(content.name)[-1]
            extensions.add(extension)
            if selected_extensions is not None and extension not in selected_extensions:
                continue
            output += "File path: " + content.path + '\nFile content:\n\n'
            output += get_content_of_file(content.download_url)
            output += "\n\n================\n\n"

    return output, extensions

def get_content_of_file(file_url):
    response = requests.get(file_url)

    try:
        response.content.decode('utf-8')
    except UnicodeDecodeError:
        return ''
    else:
        return response.text

def extension_selection_dialog(extensions):
    window = tk.Toplevel()
    window.title("Select file extensions")
    check_vars = {ext: tk.BooleanVar(window, True) for ext in extensions}  # default to True
    for ext, var in check_vars.items():
        tk.Checkbutton(window, text=ext, variable=var).pack()
    tk.Button(window, text="OK", command=window.destroy).pack()
    window.wait_window()  # wait for window to be destroyed
    return {ext for ext, var in check_vars.items() if var.get()}  # get selected extensions

def main():
    repo_url = simpledialog.askstring(title="Github Repo", prompt="Please enter the Github Repo URL:")

    repo_name = repo_url.split('https://github.com/')[-1]
    g = Github(USER_TOKEN)
    repo = g.get_repo(repo_name)

    _, all_extensions = get_all_files_recursive(repo)
    selected_extensions = extension_selection_dialog(all_extensions)

    output, _ = get_all_files_recursive(repo, selected_extensions=selected_extensions)

    file_path = filedialog.asksaveasfilename(defaultextension='.txt', 
                                             filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')])

    with open(file_path, 'w') as f:
        f.write(output)

if __name__ == "__main__":
    main()