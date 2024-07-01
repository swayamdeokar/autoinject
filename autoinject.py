import nmap
import os
import socket

# Definir variables de color
AMARILLO = "\033[93m"
BLANCO = "\033[97m"
CYAN = "\033[96m"
VERDE = "\033[92m"
ROJO = "\033[91m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

def cabecera():
    print(ROJO + title + RESET)
    print(divider)

title = """

 █████╗ ██╗   ██╗████████╗ ██████╗ ██╗███╗   ██╗     ██╗███████╗ ██████╗████████╗
██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗██║████╗  ██║     ██║██╔════╝██╔════╝╚══██╔══╝
███████║██║   ██║   ██║   ██║   ██║██║██╔██╗ ██║     ██║█████╗  ██║        ██║   
██╔══██║██║   ██║   ██║   ██║   ██║██║██║╚██╗██║██   ██║██╔══╝  ██║        ██║   
██║  ██║╚██████╔╝   ██║   ╚██████╔╝██║██║ ╚████║╚█████╔╝███████╗╚██████╗   ██║   
╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚════╝ ╚══════╝ ╚═════╝   ╚═╝                                                                                                                                      
Nmap & SQL injection automation tool                                  < xploitnation >"""

divider = """---------------------------------------------------------------------------------
"""

# Mostrar cabecera
cabecera()

def escanear_puertos(ip):
    nm = nmap.PortScanner()
    print(VERDE + "[*] Scanning ports on " + ip + RESET)
    try:
        nm.scan(ip)
    except KeyboardInterrupt:
        print(ROJO + "\n[!] Ports Scan Interrupted by User" + RESET)
        return
    except:
        print(ROJO + "[!] Error while scanning ports." + RESET)
        return
    for host in nm.all_hosts():
        print(VERDE+ "[*] Host : %s (%s)" % (host, nm[host].hostname()) + RESET)
        print(VERDE + "[*] Status : %s" % nm[host].state() + RESET)
        for proto in nm[host].all_protocols():
            print(VERDE + "[*] Protocol : %s" % proto + RESET)
            lport = nm[host][proto].keys()
            for port in sorted(lport):
                if nm[host][proto][port]['state'] == 'open':
                    print(VERDE + "[*] Port : %s Status : %s" % (port, nm[host][proto][port]['state']) + RESET)
                else:
                    print(ROJO + "[*] Port : %s Status : %s" % (port, nm[host][proto][port]['state']) + RESET)

def escanear_servicios(ip):
    print(VERDE + "[*] scanning services on " + ip + RESET)
    try:
        for port in range(1, 65536):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "unknown"
                print(VERDE + "[*] Port : %s Service : %s" % (port, service) + RESET)
            sock.close()
    except KeyboardInterrupt:
        print(ROJO + "\n[!] Service scan interrupted by user." + RESET)
        return
    except:
        print(ROJO + "[!] Error Scanning Services." + RESET)
        return

def inyeccion_sql(url):
    print(VERDE + "[*] Scanning for SQL vulnerabilities in " + url + RESET)
    try:
        os.system("sqlmap -u " + url)
    except KeyboardInterrupt:
        print(ROJO + "\n[!] Sql injection scan interrupted by user." + RESET)
        return
    except:
        print(ROJO + "[!] Error scanning for sql injection vulnerabilites" + RESET)
        return

def main():
    while True:
        print(CYAN + "[+] ¿What do you want to Audit?" + RESET)
        print("1. Port Scanning")
        print("2. Services Scanning")
        print("3. SQL injection Scanning")
        print("4. Exit")
        opcion = input(VERDE + "> " + RESET)
        if opcion == "1":
            ip = input(CYAN + "[*] Enter the Ip or Domain to Scan: " + RESET)
            escanear_puertos(ip)
            input("\nPress Enter to continue...")
            os.system("clear")
            cabecera()
        elif opcion == "2":
            ip = input(CYAN + "[*] Enter the Ip or Domain to Scan: " + RESET)
            escanear_servicios(ip)
            input("\nPress Enter to continue..")
            os.system("clear")
            cabecera()
        elif opcion == "3":
            url = input(CYAN + "[*] Enter the url to perform SQl injection Testing: " + RESET)
            inyeccion_sql(url)
            input("\nPress Enter to continue... ")
            os.system("clear")
            cabecera()
        elif opcion == "4":
            print(ROJO + "[*] Exiting the program..." + RESET)
            print(VERDE + "[+] Happy hacking ;)" + RESET)
            exit()
        else:
            print(ROJO + "[!] Invalid Option." + RESET)

if __name__ == "__main__":
    main()
