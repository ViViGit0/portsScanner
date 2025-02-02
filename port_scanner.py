import socket
import sys
import pyfiglet
from rich.console import Console
from rich.table import Table
from ports_manage import extract_json_data, threadpool_executer

console = Console()

class PSscan:
    DATA_PORTS = "./common_ports.json"

    def __init__(self):
        self.open_ports = []
        self.ports_info = {}
        self.remote_host = ""

    #Convert from str to int
    def get_ports_info(self):
        data = extract_json_data(PSscan.DATA_PORTS)
        self.ports_info = {int(k): v for (k,v) in data.items()}

    #Find IP adress
    @staticmethod
    def get_host_ip_addr(target):
        try:
            ip_addr = socket.gethostbyname(target)
        except socket.gaierror as è:
            print(f"Error: {è}")
            sys.exit()
        console.print(f"IP address acquired: [bold blue]{ip_addr}[/bold blue]")
        return ip_addr        

    def scanner_port(self, port):
        #IPV4/TCP
        sock = socket.socket()
        sock.settimeout(1.0)
        #Address connect
        conn_status = sock.connect_ex((self.remote_host, port))
        if conn_status == 0:
            self.open_ports.append(port)
        sock.close()

    #Ports table
    def show_completion_message(self):
        print()
        if self.open_ports:
            console.print("Scan Completed. Open ports: ", style="bold green")
            table = Table(show_header=True, header_style="bold green")
            table.add_column("PORTS", style="bold green")
            table.add_column("STATE",style="bold green", justify="center")
            table.add_column("SERVICE", style="bold green")
            for port in self.open_ports:
                table.add_row(str(port), "Open", self.ports_info[port])
            console.print(table)
        else:
            console.print("No open ports found on Target", style="bold magenta")

    #Title
    @staticmethod
    def show_startup_message():
       ascii_art = pyfiglet.figlet_format("PORT SCANNER")
       console.print(f"[bold green]{ascii_art}[/bold green]")
       console.print("#"*70, style="bold green")
       console.print("#"*21, "Simple Multitread TCP Port", "#"*21, style="bold green") 
       console.print("#"*70, style="bold green")
    
    #Mind
    def initialize(self):
        PSscan.show_startup_message()
        self.get_ports_info()
        try:
            target = input('Text the target: ')
        except KeyboardInterrupt:
            console.print("\nCopy...I'm exiting...", style="bold magenta")
            sys.exit()
        self.remote_host = self.get_host_ip_addr(target)
        try:
            input("\nPscan is ready. Press ENTER to run the scan")
        except KeyboardInterrupt:
            console.print("\nCopy...I'm exiting...", style="bold magenta")
            sys.exit()
        else:
            self.run()

    def run(self):
        threadpool_executer(self.scanner_port, self.ports_info.keys(), len(self.ports_info.keys()))
        self.show_completion_message()      

if __name__ == "__main__":
    pScan = PSscan()
    pScan.initialize()