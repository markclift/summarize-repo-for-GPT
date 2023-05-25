# GitHub Repo Summarizer

The goal of this project is to be able to easily summarize a Github repo in a way that can be used as input to LLMs.

As of now, this Python application provides a KivyMD UI for selecting a repo, specifying file extensions to download and downloading and consolidating the files into one text file and displays the contained tokens. Most of the code and this readme file was produced by Chat-GPT.

## Installation

1. Clone this repository to your local machine: 
```python
https://github.com/markclift/summarize-repo-for-GPT.git
```

2. Install the required dependencies:
```python
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory of the project, and add your GitHub token in the following format:
```python
GITHUB_TOKEN='your_github_token_here'
```

4. Run:
```python
python summarize_repo.py
```

## Usage

Enter the URL of the GitHub repository you wish to download and summarize. The application will retrieve all file names from the repository, excluding certain predefined ignored files (see `github_utils.py` for the list of ignored files). 

You can select which file extensions you wish to retrieve. The app will display the total number of tokens in the downloaded content. 

Enter a filename to save the downloaded content as a .txt file.

**Note:** Ensure that you have the necessary access permissions to the repository.

## TODO:
1. Move ignore files from hard-coded to the UI
2. Move selection of ignore files & extensions to a savable settings menu
3. Add the option to split the output into something within a certain token limit
4. Add LLM-generated summarization capabilities!

## License

This project is licensed under the [MIT License](LICENSE).