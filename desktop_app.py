import webbrowser
import threading
from app import app

def run_flask():
    app.run(port=5000, debug=False)

if __name__ == '__main__':
    threading.Timer(1.0, lambda: webbrowser.open('http://localhost:5000')).start()
    run_flask()
