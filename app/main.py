import argparse
import getpass
from prometheus_client import start_http_server
from nutanixMetrics import NutanixMetrics
import urllib3
import message

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    """Main entry point"""
    # Get data from parser
    parser = argparse.ArgumentParser(description='Nutanix Exporter Prometheus')
    parser.add_argument('-H', '--host-prism', type=str, help='Host of the prism', default='localhost:9440')
    parser.add_argument('-p', '--exporter-port', type=int, help='Port on which you want to expose prometheus', default=8000)
    parser.add_argument('-i', '--polling-interval', type=int, help='Time to wait in seconds between two polling', default=30)
    parser.add_argument('-U', '--username', type=str, help='Username of prism account', default='admin')
    parser.add_argument('-P', '--password', type=str, help='Password of prism account')
    parser.add_argument('-s', '--secure', type=str, help='Is the connection with Prism secure?', default=False)

    args = parser.parse_args()
    password= args.password if args.password else getpass.getpass() 

    # Prepare for get nutanix data
    message.info("Initializing metrics class...")
    nutanix_metrics = NutanixMetrics(
        host_prism=args.host_prism,
        polling_interval_seconds=args.polling_interval,
        user = args.username,
        pwd = password,
        prism_secure=args.secure,
    )
    
    # Get Nutanix Data and expose them to prometheus format
    message.info(f"Starting http server on http://localhost:{args.exporter_port}")
    start_http_server(args.exporter_port)
    nutanix_metrics.run_metrics_loop() # Is there a way to close this gracefully?

if __name__ == "__main__":
    main()