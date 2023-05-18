# GitHub Repo File Downloader

This Python script allows you to download the contents of specific types of files in a GitHub repository.

## Prerequisites

- Python 3.x
- `tkinter` module
- `github` module
- `requests` module
- `dotenv` module

## Installation

1. Clone the repository or download the script directly.
2. Install the required dependencies by running the following command:
```python
pip install -r requirements.txt
```

## Usage

1. Run the script using the following command:
```python
python3 summarize_repo.py
```

2. The script will prompt you to enter the GitHub repository URL.

3. After entering the URL, the script will authenticate using the GitHub token stored in the `.env` file.

4. It will recursively go through the repository to gather all distinct file extensions (excluding those in the IGNORED_FILES list).

5. A GUI will be opened listing all file extensions in the repository. All extensions will be ticked by default. You can select which file types you want to include in the download by ticking or unticking the boxes next to the extensions.

6. Once you confirm your selection, the script will fetch the contents of only the files of the selected types.

7. You will be prompted to select the destination path and provide a filename. The contents of the files will then be saved to a text file at the chosen location.

8. The text file will contain the file paths and their respective contents, separated by the "===============================" delimiter.

**Note:** Ensure that you have the necessary access permissions to the repository.

## License

This project is licensed under the [MIT License](LICENSE).
