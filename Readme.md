# GitHub Repo File Downloader

This Python script allows you to download the contents of all files in a GitHub repository.

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
pip install requirements.txt
```

## Usage

1. Run the script using the following command:
```python
python3 summarize_repo.py
```

2. The script will prompt you to enter the GitHub repository URL.

3. After entering the URL, the script will authenticate using the GitHub token stored in the `.env` file.

4. It will recursively fetch the contents of all files in the repository, excluding the ignored files specified in the `IGNORED_FILES` list.

5. The script will save the contents of the files to a text file. You will be prompted to select the destination path and provide a filename.

6. The text file will contain the file paths and their respective contents, separated by the "===============================" delimiter.

**Note:** Ensure that you have the necessary access permissions to the repository.

## License

This project is licensed under the [MIT License](LICENSE).
