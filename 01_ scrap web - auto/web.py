from flask import Flask, render_template, request
import modules.scrap_kit as sk
import subprocess
import json
from time import time, sleep
from pprint import pprint
import argparse
import webbrowser
import threading
import socket
import os
import glob



parser = argparse.ArgumentParser(epilog='thanks for the semester. we sorry for you lost')

parser.add_argument('-m', '--mode', required=True, choices=['a','t'], help='choose what news you want to show. whether it actually or technology')
args = parser.parse_args()

app = Flask(__name__)

@app.context_processor
def utility_processor():
    return dict(fix_hebrew_english_mix=sk.fix_hebrew_english_mix)

def get_articles() -> list:
    try:
        result = subprocess.run(['python3', 'modules/scrap_actual.py'] if args.mode == 'a' else ['python3', 'modules/scrap_geek.py'], capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            print(f"Error running scraper: {result.stderr}")
            return []
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Error in get_articles: {str(e)}")
        return []

def open_browser():
    sleep(2)
    # Wait until the server is accessible
    while True:
        try:
            # Attempt to establish a socket connection to the server
            with socket.create_connection(("127.0.0.1", 5000), timeout=1):
                break
        except OSError:
            sleep(1)
    webbrowser.open_new('http://127.0.0.1:5000/')


def delete_images():
    image_files = glob.glob('static/images/*')
    for image in image_files:
        try:
            os.remove(image)
            print(f"Deleted {image}")
        except Exception as e:
            print(f"Error deleting {image}: {e}")

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        delete_images()
        exit()
    func()

@app.route('/')
def home():
    articles = get_articles()
    return render_template('home.html', articles=articles)

if __name__ == '__main__':
    # Start the browser thread
    if not os.environ.get("WERKZEUG_RUN_MAIN"):  # Check if it's the main process
        threading.Thread(target=open_browser).start()
    # Run the Flask app
    app.run(debug=True)
