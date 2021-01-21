#cython: language_level=3
import time 
from watchdog.observers import Observer 
from watchdog.events import FileSystemEventHandler 
import multiprocessing
import sys
import subprocess
import config.config
import libs.colors
def current_url():
    if config.config.PORT == 80:
        print(f"{libs.colors.colors.bold}{libs.colors.colors.fg.cyan}Server address: {libs.colors.colors.fg.orange}http://localhost/{libs.colors.colors.reset}")
    else:
        print(f"{libs.colors.colors.bold}{libs.colors.colors.fg.cyan}Server address: {libs.colors.colors.fg.orange}http://localhost:{str(config.config.PORT)}/{libs.colors.colors.reset}")

all_processes = []
def restart_server():
    kill_processes()
    start_server()



def start_server():
    global all_processes
    process = subprocess.Popen(['python3', 'main.py', 'server_no_watchdog'])
    all_processes.append(process) 

def kill_processes():
    global all_processes
    for process in all_processes: 
        process.kill() 
    all_processes = []
class OnMyWatch: 
    # Set the directory on watch 
    watchDirectory = "pages"
  
    def __init__(self): 
        self.observer = Observer() 
  
    def run(self): 
        event_handler = Handler() 
        self.observer.schedule(event_handler, self.watchDirectory, recursive = True) 
        self.observer.start() 
        try: 
            while True: 
                time.sleep(5) 
        except: 
            self.observer.stop() 
        self.observer.join() 
class Handler(FileSystemEventHandler):  
    @staticmethod
    def on_any_event(event): 
        if event.is_directory: 
            return None
  
        elif event.event_type == 'created': 
            pass
        elif event.event_type == 'modified':
            restart_server()
if __name__ == '__main__': 
    if len(sys.argv) < 2:
        start_server()
        print(f"{libs.colors.colors.bold}{libs.colors.colors.fg.yellow}Starting Watchdog{libs.colors.colors.reset}")
        current_url()
        watch = OnMyWatch() 
        watch.run() 
    else:
        if sys.argv[1] == "server_no_watchdog":
            import lemon.lemon
        else:
            print("Error: This is not a useless run")
            sys.exit("Shutting Down")