import os
import requests
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

IGNORED_FILES = ['.gitignore', 'package-lock.json', 'tsconfig.json', 'vercel.svg', 'favicon.ico', '.env', '.DS_Store', 'Dockerfile', '.dockerignore', '.prettierrc']
IGNORED_FOLDERS = ['.venv', '.vscode', '__pycache__', 'nginx', 'node_modules', 'public', 'build', 'dist', ]

def get_all_filepaths_in_local_dir(path: str):
    extensions = set()
    filepaths = []

    for root, dirs, files in os.walk(path):
        # Modifying dirs list in place will prune the subdirectories you'll visit
        dirs[:] = [d for d in dirs if d not in IGNORED_FOLDERS]

        for name in files:
            if name in IGNORED_FILES:
                continue
            
            item = Path(root, name)
            base, ext = os.path.splitext(str(item))
            
            if ext:
                extensions.add(ext)
                filepaths.append(str(item))
            else:
                extensions.add(item.name)
                filepaths.append(base)

    return filepaths, extensions

def get_all_filepaths_in_github_repo(repo, path=''):
    extensions = set()
    filepaths=[]
    contents = repo.get_contents(path)
    for content in contents:
        if content.type == 'dir':
            if content.name not in IGNORED_FOLDERS:
                new_filepaths, new_extensions = get_all_filepaths_in_github_repo(repo, content.path)
                extensions.update(new_extensions)
                filepaths.extend(new_filepaths)
        elif content.name not in IGNORED_FILES:
            extension = os.path.splitext(content.name)[-1]
            extensions.add(extension)
            filepaths.append(content.download_url)
    return filepaths, extensions

def get_all_file_contents_from_github(paths, selected_extensions):
    output=''
    for path in paths:
        _, ext = os.path.splitext(path)
        if ext in selected_extensions:
            output += "File path: " + path + '\nFile content:\n\n'
            output += download_file(path)
            output += "\n\n================\n\n"
    return output

def get_all_file_contents_from_directory(paths, selected_extensions):
    output = ''
    for path in paths:
        _, ext = os.path.splitext(path)
        if ext in selected_extensions:
            with open(path, 'r') as file:
                output += "File path: " + path + '\nFile content:\n\n'
                output += file.read()
                output += "\n\n================\n\n"
    return output

def download_file(file_url):
    response = requests.get(file_url)
    try:
        response.content.decode('utf-8')
    except UnicodeDecodeError:
        logger.error(f'Error while decoding content from {file_url}')
    else:
        return response.text