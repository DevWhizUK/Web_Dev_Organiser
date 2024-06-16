import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import tkinter as tk
from tkinter import filedialog

class DownloadOrganizerHandler(FileSystemEventHandler):
    def __init__(self, folder_to_track, destination_folder):
        self.folder_to_track = folder_to_track
        self.destination_folder = destination_folder
        self.create_assets_folders()

    def create_assets_folders(self):
        media_folder = os.path.join(self.destination_folder, 'assets', 'media')
        self.img_folder = os.path.join(media_folder, 'img')
        self.vid_folder = os.path.join(media_folder, 'vid')
        self.ico_folder = os.path.join(media_folder, 'ico')

        for folder in [self.img_folder, self.vid_folder, self.ico_folder]:
            if not os.path.exists(folder):
                os.makedirs(folder)
                print(f"Created folder: {folder}")

    def on_modified(self, event):
        for filename in os.listdir(self.folder_to_track):
            source = os.path.join(self.folder_to_track, filename)
            if os.path.isfile(source):
                self.process_file(source, filename)

    def process_file(self, source, filename):
        extension = os.path.splitext(filename)[1].lower()
        if extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']:
            destination_folder = self.img_folder
        elif extension in ['.mp4', '.mov', '.avi', '.mkv', '.wmv']:
            destination_folder = self.vid_folder
        elif extension in ['.ico']:
            destination_folder = self.ico_folder
        else:
            return  # Skip files with extensions not in our list

        destination = os.path.join(destination_folder, filename)
        destination = self.handle_duplicates(destination)
        print(f"Moving {source} to {destination}")
        shutil.move(source, destination)

    def handle_duplicates(self, path):
        base, extension = os.path.splitext(path)
        counter = 1
        new_path = path
        while os.path.exists(new_path):
            new_path = f"{base}_{counter}{extension}"
            counter += 1
        return new_path

def select_destination_folder():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder_selected = filedialog.askdirectory(title="Select Destination Folder")
    return folder_selected

def main():
    downloads_folder = os.path.expanduser("~/Downloads")
    destination_folder = select_destination_folder()
    if not destination_folder:
        print("No destination folder selected. Exiting.")
        return

    event_handler = DownloadOrganizerHandler(downloads_folder, destination_folder)
    observer = Observer()
    observer.schedule(event_handler, downloads_folder, recursive=False)
    observer.start()

    print(f"Monitoring folder: {downloads_folder}")
    print(f"Destination folder: {destination_folder}")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print("Observer stopped.")

if __name__ == "__main__":
    main()
