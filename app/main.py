import os
from prometheus_client import start_http_server
from dotenv import load_dotenv
from nutanixMetrics import NutanixMetrics
import urllib3
import message

load_dotenv()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    """Main entry point"""

    message.ok("Getting environment variables...")
    polling_interval_seconds = int(os.getenv("POLLING_INTERVAL_SECONDS", "30"))
    app_port = int(os.getenv("APP_PORT", "9440"))
    exporter_port = int(os.getenv("EXPORTER_PORT", "8000"))

    message.ok("Initializing metrics class...")
    nutanix_metrics = NutanixMetrics(
        app_port=app_port,
        polling_interval_seconds=polling_interval_seconds,
        prism=os.getenv('PRISM'),
        user = os.getenv('PRISM_USERNAME'),
        pwd = os.getenv('PRISM_SECRET'),
        prism_secure=bool(os.getenv("PRISM_SECURE", False)),
    )
    
    message.ok(f"Starting http server on http://localhost:{exporter_port}")
    start_http_server(exporter_port)
    nutanix_metrics.run_metrics_loop() # Is there a way to close this gracefully?

if __name__ == "__main__":
    main()