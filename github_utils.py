import os
import requests
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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
            logger.info("Found file: " + content.path)
            output += "File path: " + content.path + '\nFile content:\n\n'
            output += get_content_of_file(content.download_url)
            output += "\n\n================\n\n"
    return output, extensions

def get_content_of_file(file_url):
    response = requests.get(file_url)
    try:
        response.content.decode('utf-8')
    except UnicodeDecodeError:
        logger.error(f'Error while decoding content from {file_url}')
    else:
        return response.text