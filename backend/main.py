import logging
from monitor.scheduler import start_monitoring
from web.views import app

logging.basicConfig(filename="logs/events.log", level=logging.INFO)

if __name__ == "__main__":
    start_monitoring()
    app.run(host='0.0.0.0', port=5000)
