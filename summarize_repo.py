#!/usr/bin/env python3

# Standard library imports
import os
import threading
from urllib.parse import urlparse
from pathlib import Path

# Third-party imports
from dotenv import load_dotenv
import tiktoken
from github import Github, RateLimitExceededException
from github.GithubException import UnknownObjectException
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivy.logger import Logger
from kivymd.uix.selectioncontrol import MDCheckbox

# Local imports
from utils import get_all_filepaths_in_local_dir, get_all_filepaths_in_github_repo, get_all_file_contents_from_github, get_all_file_contents_from_directory

# Initialize the local logger
import logging
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()
Window.size = (350, 500)

USER_TOKEN = os.getenv('GITHUB_TOKEN')

# Verify GitHub token
if not USER_TOKEN:
    raise ValueError("GitHub token not found in environment variables")

KV = '''
BoxLayout:
    orientation: 'vertical'
    padding: '8dp'

    MDTopAppBar:
        title: 'Repo Summarizer'
        md_bg_color: app.theme_cls.primary_color
        background_palette: 'Primary'
        elevation: 10
        left_action_items: [['menu', lambda x: '']]

    ScreenManager:
        id: screen_manager

        Screen:
            name: 'enter_repo_page'

            BoxLayout:
                orientation: 'vertical'
                size_hint: 1, None
                pos_hint: {'center_y': 0.5}
                padding: '8dp'
                spacing: '20dp'

                MDLabel:
                    text: 'Enter the Github Repo URL or local directory:'
                    halign: 'center'
                    size_hint_y: None

                MDTextField:
                    id: repo_input
                    helper_text: 'e.g. https://github.com/username/repo'
                    helper_text_mode: 'persistent'
                    pos_hint: {'center_x': 0.5}
                    size_hint_x: None
                    width: 600
                    multiline: False
                    size_hint_y: None
                    on_text_validate: app.submit()

                MDRaisedButton:
                    id: submit_button
                    text: 'Submit'
                    pos_hint: {'center_x': 0.5}
                    size_hint_y: None
                    on_release: app.submit()

        Screen:
            name: 'extensions_select_page'

            MDBoxLayout:
                orientation: 'vertical'
                padding: '20dp'

                MDLabel:
                    id: extensions_label
                    text: ''
                    halign: 'center'
                    size_hint_y: None

                ScrollView:
                    MDList:
                        id: extension_list
                        spacing: -25

                BoxLayout:
                    size_hint_y: None
                    height: self.minimum_height
                    size_hint_x: None
                    width: self.minimum_width
                    pos_hint: {'center_x': 0.5}
                    spacing: '10dp'
                    MDRaisedButton:
                        id: back_button
                        text: 'Back'
                        on_release: app.back_to_home()
                    MDRaisedButton:
                        id: ok_button
                        text: 'Ok'
                        on_release: app.on_extension_selection()

        Screen:
            name: 'filename_input_page'
            
            BoxLayout:
                orientation: 'vertical'
                size_hint: 1, None
                pos_hint: {'center_y': 0.5}
                padding: '8dp'
                spacing: '20dp'

                MDLabel:
                    id: token_count_txt
                    text: 'The amount of tokens in the text is: '
                    halign: 'center'
                    size_hint_y: None
                
                MDTextField:
                    id: filename_input
                    hint_text: 'Enter filename'
                    pos_hint: {'center_x': 0.5}
                    size_hint_x: None
                    default_txt: 'output.txt'
                    helper_text: 'e.g. output.txt'
                    helper_text_mode: 'persistent'
                    width: 600
                    multiline: False
                    size_hint_y: None

                BoxLayout:
                    size_hint_y: None
                    height: self.minimum_height
                    size_hint_x: None
                    width: self.minimum_width
                    pos_hint: {'center_x': 0.5}
                    spacing: '10dp'
                    MDRaisedButton:
                        id: cancel_button
                        text: 'Back'
                        on_release: app.back_to_extensions()
                    MDRaisedButton:
                        id: ok_button
                        text: 'Ok'
                        on_release: app.on_filename_input()
'''

class RightCheckbox(IRightBodyTouch, MDCheckbox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.active = True

class ExtensionListItem(OneLineAvatarIconListItem):
    divider = None

    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.add_widget(RightCheckbox())

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Blue'
        self.filename = None
        self.root = Builder.load_string(KV)
        self.repo_input = self.root.ids.repo_input
        self.repo_input.focus = True
        self.filename_input = self.root.ids.filename_input
        self.filename_input.text = "output.txt"  # Set the default value
        return self.root
    
    def get_all_filepaths(self, g):
        if os.path.isdir(self.repo_name):
            self.files_to_download, all_extensions = get_all_filepaths_in_local_dir(self.repo_name)
            # Move UI updates back to the main thread
            Clock.schedule_once(lambda dt: self.dialog.dismiss())
            Clock.schedule_once(lambda dt: self.populate_extensions(all_extensions))
        
        else:
            try:
                self.repo = g.get_repo(self.repo_name)
                self.files_to_download, all_extensions = get_all_filepaths_in_github_repo(self.repo)

            except RateLimitExceededException:
                Clock.schedule_once(lambda dt: toast("GitHub API rate limit exceeded. Please wait a while before retrying."))
                Clock.schedule_once(lambda dt: self.dialog.dismiss(), 0.5)  # dismiss after a short delay
            except UnknownObjectException:
                Clock.schedule_once(lambda dt: toast("Invalid repository URL. Please check and try again."))
                Clock.schedule_once(lambda dt: self.dialog.dismiss(), 0.5)  # dismiss after a short delay
            except Exception as e:
                Clock.schedule_once(lambda dt, error=e: toast(f"An error occurred: {str(error)}"))
                logger.error(f'Error in get_all_filepaths_in_github_repo: {e}')
                Clock.schedule_once(lambda dt: self.dialog.dismiss(), 0.5)  # dismiss after a short delay
            else:
                # Move UI updates back to the main thread
                Clock.schedule_once(lambda dt: self.dialog.dismiss())
                Clock.schedule_once(lambda dt: self.populate_extensions(all_extensions))

    def submit(self):
        self.repo_url = self.root.ids.repo_input.text

        if not self.repo_url.strip():
            toast("Please enter a URL or local directory path")
            return

        parsed_url = urlparse(self.repo_url)
        if os.path.isdir(self.repo_url):
            self.repo_name = self.repo_url
        elif all([parsed_url.scheme, parsed_url.netloc, parsed_url.path]) and parsed_url.netloc in ['github.com', 'www.github.com']:
            self.repo_name = parsed_url.path.lstrip('/')
        else:
            toast("Invalid URL or local directory path")
            return

        g = Github(USER_TOKEN) if not os.path.isdir(self.repo_url) else None

        self.dialog = MDDialog(title=f"Reading {self.repo_name} repo...", auto_dismiss=False,)
        self.dialog.open()

        threading.Thread(target=self.get_all_filepaths, args=(g,), daemon=True).start()

    def populate_extensions(self, extensions):
        self.root.ids.extensions_label.text = f"Select the file extensions you wish to retrieve from the {self.repo_name} repo"
        self.root.ids.screen_manager.current = 'extensions_select_page'
        
        extension_list = self.root.ids.extension_list
        extension_list.clear_widgets()

        self.check_vars = {}

        for ext in sorted(extensions):
            list_item = ExtensionListItem(text=ext)
            self.check_vars[ext] = list_item.children[0].children[0]  # store CheckBox instance for later reference
            extension_list.add_widget(list_item)

    def back_to_home(self):
        self.root.ids.screen_manager.current = 'enter_repo_page'
        self.root.ids.extension_list.clear_widgets()
        self.repo_input.focus = True

    def back_to_extensions(self):
        self.root.ids.screen_manager.current = 'extensions_select_page'
    
    def close_dialog(self, instance):
        self.dialog.dismiss()
        if hasattr(self, 'repo_input'):
            self.repo_input.text = ''
        if hasattr(self, 'filename_input'):
            self.filename_input.text = ''

    def on_extension_selection(self):
        selected_extensions = {ext for ext, checkbox in self.check_vars.items() if checkbox.active}

        self.dialog = MDDialog(title=f"Downloading files from the {self.repo_name} repo...")
        self.dialog.open()

        threading.Thread(target=self.get_files_with_selected_extensions, args=(selected_extensions,), daemon=True).start()

    def get_files_with_selected_extensions(self, selected_extensions):
        if os.path.isdir(self.repo_name):
            self.output = get_all_file_contents_from_directory(self.files_to_download, selected_extensions)
            Clock.schedule_once(lambda dt: self.show_filename_input_screen())
            Clock.schedule_once(lambda dt: self.dialog.dismiss())
        else:    
            try:
                self.output = get_all_file_contents_from_github(self.files_to_download, selected_extensions)
                Clock.schedule_once(lambda dt: self.show_filename_input_screen())
            except Exception as e:
                Clock.schedule_once(lambda dt, error=e: toast(f"An error occurred: {str(error)}"))
                logger.error(f'Error in get_files_with_selected_extensions: {e}')
            finally:
                # Close the dialog after the work is done
                Clock.schedule_once(lambda dt: self.dialog.dismiss())

    def show_filename_input_screen(self):
        token_count = self.num_tokens_from_string(self.output, "cl100k_base")
        self.root.ids.token_count_txt.text = f"The amount of tokens in the text is: {token_count}\n\nEnter filename to save output to:"
        self.root.ids.screen_manager.current = 'filename_input_page'
        self.filename_input.focus = True

    def num_tokens_from_string(self, string: str, encoding_name: str) -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens
    
    def on_filename_input(self):
        self.filename = self.filename_input.text
        self.manager_open()

    def manager_open(self):
        self.manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            search='dirs',
            preview=False,
        )
        desktop_path = os.path.expanduser("~/Desktop")
        self.manager.show(desktop_path)

    def exit_manager(self, *args):
        self.manager.close()
        self.back_to_home()

    def select_path(self, path):
        filename = f'{self.filename}'
        full_path = os.path.join(path, filename)
        with open(full_path, 'w') as f:
            f.write(self.output)
        self.exit_manager()
        toast('File saved successfully!')

if __name__ == "__main__":
    MainApp().run()