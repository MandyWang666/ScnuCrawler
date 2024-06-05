from flask import Flask
from runcrawler import start_crawl, read_analysis_save
import os

app = Flask(__name__)


@app.route('/start_crawl')
def run_crawl():
    start_crawl()
    return 'crawled successfully!'


@app.route('/display')
def run_display():
    command = "streamlit run webui.py"
    os.system(command)


@app.route('/text_analysis')
def run_display():
    read_analysis_save('data/result.csv')
    return 'crawled successfully!'


if __name__ == '__main__':
    app.run()
