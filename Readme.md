# Repo Summarizer

The goal of this project is to be able to easily summarize a code repo (either from Github or a local directory) in a way that can be used as input to LLMs.

This Python application provides a KivyMD UI for selecting a repo, specifying file extensions to include and then calling the OpenAI API to summarize each file and consolidate the summaries into a single text output file. Most of the code and this readme file was produced by Chat-GPT.

## Installation

1. Clone this repository to your local machine: 
```python
git clone https://github.com/markclift/summarize-repo-for-GPT.git
```

2. Install the required dependencies:
```python
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory of the project, and add your GitHub token and OpenAI keys in the following format:
```python
GITHUB_TOKEN='your_github_token_here'
OPENAI_API_KEY='key'
```

4. Run:
```python
python summarize_repo.py
```

## Usage

Enter the path of the local or remote repository you wish to summarize. The application will retrieve all file names from the repository, excluding certain predefined ignored files (see `utils.py` for the list of ignored files/folders). 

You can then select which file extensions you wish to include in the generated summary.

Enter a filename to save the downloaded content as a .txt file. The app will display the total number of tokens in the input vs output and the approximate cost incurred in the summarization.

**Note:** Ensure that you have the necessary access permissions to the repository.

## TODO:
1. Move ignore files/folders/extensions from hard-coded to a savable settings menu in the UI
2. Add the option to split the output into something within a certain token limit
3. Make the prompt better!

## License

This project is licensed under the [MIT License](LICENSE).