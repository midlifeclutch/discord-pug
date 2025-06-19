#!/usr/bin/env python3
import os
import sys
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RestartOnChange(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = None
        self.start_bot()

    def start_bot(self):
        print("🔁 Starting bot...")
        self.process = subprocess.Popen(self.command)

    def stop_bot(self):
        if self.process:
            print("🛑 Stopping bot...")
            self.process.terminate()
            self.process.wait()

    def restart_bot(self):
        self.stop_bot()
        self.start_bot()

    def on_any_event(self, event):
        if event.src_path.endswith(".py"):
            print(f"📦 Change detected in {event.src_path}, restarting bot...")
            self.restart_bot()

if __name__ == "__main__":
    command = [sys.executable, "-m", "bot"]  # replace "bot" with your entry module/package
    path_to_watch = "bot/"  # or "bot/", or whatever your code dir is

    event_handler = RestartOnChange(command)
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)

    try:
        observer.start()
        print(f"👀 Watching for file changes in {path_to_watch}...")
        while True:
            pass  # Keep main thread alive
    except KeyboardInterrupt:
        observer.stop()
        event_handler.stop_bot()
    observer.join()
