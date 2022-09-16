import os
from prometheus_client import start_http_server
from datetime import datetime
from dotenv import load_dotenv
from nutanixMetrics import NutanixMetrics
import urllib3
from bcolors import bcolors

load_dotenv()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    """Main entry point"""

    print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [INFO] Getting environment variables...{bcolors.RESET}")
    polling_interval_seconds = int(os.getenv("POLLING_INTERVAL_SECONDS", "30"))
    app_port = int(os.getenv("APP_PORT", "9440"))
    exporter_port = int(os.getenv("EXPORTER_PORT", "8000"))

    print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [INFO] Initializing metrics class...{bcolors.RESET}")
    nutanix_metrics = NutanixMetrics(
        app_port=app_port,
        polling_interval_seconds=polling_interval_seconds,
        prism=os.getenv('PRISM'),
        user = os.getenv('PRISM_USERNAME'),
        pwd = os.getenv('PRISM_SECRET'),
        prism_secure=bool(os.getenv("PRISM_SECURE", False)),
    )
    
    print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [INFO] Starting http server on port {exporter_port}{bcolors.RESET}")
    start_http_server(exporter_port)
    nutanix_metrics.run_metrics_loop() # Is there a way to close this gracefully?

if __name__ == "__main__":
    main()