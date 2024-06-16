# Web Development Downloads Organizer

A Python script that helps organize your web development assets by monitoring the Downloads folder and sorting files into appropriate subfolders. The script provides a GUI to select the destination folder and creates an `assets` directory structure with `img`, `vid`, and `ico` subfolders.

## Features

- Monitors the Downloads folder for new files.
- Organizes files into `img`, `vid`, and `ico` folders based on file extensions.
- Handles duplicate files by appending a counter to the filename.
- Launches a GUI for selecting the destination folder.

## Prerequisites

- Python 3.x
- `watchdog` library
