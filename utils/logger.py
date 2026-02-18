import logging

logging.basicConfig(
    filename="threat.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def log_scan(ip, risk):
    logging.info(f"IP Scanned: {ip} | Risk: {risk}")
