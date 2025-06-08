import threading, time
from monitor.checker import check_http, check_tcp
#from monitor.alerter import alert_telegram
import yaml, logging

with open("config.yaml") as f:
    config = yaml.safe_load(f)

def monitor_endpoint(ep):
    while True:
        if ep["type"] == "http":
            status, result = check_http(ep["url"], ep["timeout"])
            if not status or status >= 400:
                msg = f"[{ep['name']}] FAIL: {result}"
                #alert_telegram(msg, config["alerts"]["telegram"]["token"], config["alerts"]["telegram"]["chat_id"])
                logging.warning(msg)
            else:
                logging.info(f"[{ep['name']}] OK: {status} in {result}s")

        elif ep["type"] == "tcp":
            ok, err = check_tcp(ep["host"], ep["port"], ep["timeout"])
            if not ok:
                msg = f"[{ep['name']}] TCP FAIL: {err}"
                #alert_telegram(msg, config["alerts"]["telegram"]["token"], config["alerts"]["telegram"]["chat_id"])
                logging.warning(msg)
            else:
                logging.info(f"[{ep['name']}] TCP OK")
        time.sleep(ep["interval"])

def start_monitoring():
    for ep in config["endpoints"]:
        t = threading.Thread(target=monitor_endpoint, args=(ep,))
        t.daemon = True
        t.start()
