from flask import Flask
from runcrawler import start_crawl

app = Flask(__name__)


@app.route('/')
def run_crawl():
    start_crawl()
    return 'crawled successfully!'


#if __name__ == '__main__':
#    app.run()
