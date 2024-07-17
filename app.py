import subprocess
import pyautogui
import time
import pygetwindow as gw
from pyautogui import ImageNotFoundException
import random
import signal
import sys

# Rutas a los ejecutables de Chrome Portable (ajustado a 22)
chrome_paths = [
    r"C:\Users\rodig\OneDrive\Escritorio\Chrome\GoogleChromePortable1\GoogleChromePortable.exe",
    r"C:\Users\rodig\OneDrive\Escritorio\Chrome\GoogleChromePortable2\GoogleChromePortable.exe",
    r"C:\Users\rodig\OneDrive\Escritorio\Chrome\GoogleChromePortable3\GoogleChromePortable.exe",
    r"C:\Users\rodig\OneDrive\Escritorio\Chrome\GoogleChromePortable4\GoogleChromePortable.exe",
    r"C:\Users\rodig\OneDrive\Escritorio\Chrome\GoogleChromePortable5\GoogleChromePortable.exe",
    r"C:\Users\rodig\OneDrive\Escritorio\Chrome\GoogleChromePortable6\GoogleChromePortable.exe",
    r"C:\Users\rodig\OneDrive\Escritorio\Chrome\GoogleChromePortable7\GoogleChromePortable.exe",
    r"C:\Users\rodig\OneDrive\Escritorio\Chrome\GoogleChromePortable8\GoogleChromePortable.exe",
    r"C:\Users\rodig\OneDrive\Escritorio\Chrome\GoogleChromePortable9\GoogleChromePortable.exe",
    r"C:\Users\rodig\OneDrive\Escritorio\Chrome\GoogleChromePortable10\GoogleChromePortable.exe",
    r"C:\Users\rodig\OneDrive\Escritorio\Chrome\GoogleChromePortable11\GoogleChromePortable.exe",
    r"C:\Users\rodig\OneDrive\Escritorio\Chrome\GoogleChromePortable12\GoogleChromePortable.exe",
    r"C:\Users\rodig\OneDrive\Escritorio\Chrome\GoogleChromePortable13\GoogleChromePortable.exe",
    r"C:\Users\rodig\OneDrive\Escritorio\Chrome\GoogleChromePortable14\GoogleChromePortable.exe",
    r"C:\Users\rodig\OneDrive\Escritorio\Chrome\GoogleChromePortable15\GoogleChromePortable.exe",
    r"C:\Users\rodig\OneDrive\Escritorio\Chrome\GoogleChromePortable16\GoogleChromePortable.exe",
    r"C:\Users\rodig\OneDrive\Escritorio\Chrome\GoogleChromePortable17\GoogleChromePortable.exe",
    r"C:\Users\rodig\OneDrive\Escritorio\Chrome\GoogleChromePortable18\GoogleChromePortable.exe",
    r"C:\Users\rodig\OneDrive\Escritorio\Chrome\GoogleChromePortable19\GoogleChromePortable.exe",
    r"C:\Users\rodig\OneDrive\Escritorio\Chrome\GoogleChromePortable20\GoogleChromePortable.exe",
    r"C:\Users\rodig\OneDrive\Escritorio\Chrome\GoogleChromePortable21\GoogleChromePortable.exe",
    r"C:\Users\rodig\OneDrive\Escritorio\Chrome\GoogleChromePortable22\GoogleChromePortable.exe",
]

# Ubicaciones VPN correspondientes a las 22 instancias de Chrome
vpn_locations = [
    "Ashburn",
    "Atlanta",
    "Bend",
    "Boston",
    "Buf",
    "Charlotte",
    "Chicago",
    "Dallas",
    "Denver",
    "Detroit",
    "Houston",
    "Kansas City",
    "Latham",
    "Las Vegas",
    "Los Angeles",
    "Miami",
    "New York",
    "Phoenix",
    "Salt Lake City",
    "San Francisco",
    "San Jose",
    "Seattle",
]

# Solicitar la URL al usuario
def get_target_url():
    url = input("Ingrese la URL del sitio web: ")
    return url

# Diccionario para rastrear el estado de las ventanas (True si está en la página objetivo, False si está en Google)
window_states = {}

# Esperar a que la conexión VPN se establezca verificando la presencia del botón de desconexión
def wait_for_connection():
    while True:
        disconnect_button_location = pyautogui.locateCenterOnScreen('disconnect_pause.png', confidence=0.8)
        if disconnect_button_location is not None:
            print("Conexión VPN establecida.")
            return True
        time.sleep(2)  # Esperar 2 segundos antes de verificar nuevamente

# Navegar a la URL especificada y esperar el tiempo indicado
def navigate_to_url(chrome_window, url, wait_time):
    chrome_window.activate()
    pyautogui.hotkey('ctrl', 'l')  # Enfocar la barra de direcciones
    pyautogui.typewrite(url)
    pyautogui.press('enter')
    time.sleep(wait_time)  # Esperar después de navegar a la URL
    chrome_window.minimize()

# Abrir Chrome, conectar a VPN, y navegar a la URL deseada
def open_chrome_and_connect(chrome_path, location, connection_number, initial_state, target_url):
    print(f"Conectando instancia {connection_number} a la ubicación {location}...")
    # Abrir el ejecutable de Chrome
    proc = subprocess.Popen(chrome_path)
    time.sleep(5)  # Esperar a que Chrome se abra completamente

    # Buscar la ventana de Chrome abierta
    chrome_window = None
    for window in gw.getWindowsWithTitle('Google Chrome'):
        chrome_window = window
        break

    if chrome_window:
        # Maximizar y activar la ventana de Chrome
        chrome_window.maximize()
        time.sleep(1)
        chrome_window.activate()
        time.sleep(1)

        try:
            # Buscar y hacer clic en la extensión de Surfshark VPN
            vpn_extension_location = pyautogui.locateCenterOnScreen('surfshark.png', confidence=0.8)
            pyautogui.click(vpn_extension_location)
            time.sleep(3)

            # Escribir la ubicación en el recuadro de búsqueda
            search_box_location = pyautogui.locateCenterOnScreen('search.png', confidence=0.8)
            if search_box_location is not None:
                pyautogui.click(search_box_location)
                pyautogui.typewrite(location)
                pyautogui.press('enter')
            else:
                print("No se encontró el recuadro de búsqueda en la pantalla")
                return

            time.sleep(2)

            # Conectar a la ubicación especificada
            location_button_location = pyautogui.locateCenterOnScreen('location.png', confidence=0.8)
            if location_button_location is not None:
                pyautogui.click(location_button_location)
            else:
                print(f"No se encontró la ubicación {location} en la pantalla")
                return

            # Esperar a que la conexión VPN se establezca
            if not wait_for_connection():
                print(f"Error al conectar a la ubicación {location}")
                return
            
            # Navegar a la URL inicial (Página objetivo o Google)
            if initial_state:
                navigate_to_url(chrome_window, target_url, 15)
            else:
                navigate_to_url(chrome_window, "https://www.google.com", 3)
                
            window_states[chrome_path] = initial_state
        except ImageNotFoundException:
            try:
                # Si no se encuentra surfshark.png, buscar surfshark2.png
                vpn_extension2_location = pyautogui.locateCenterOnScreen('surfshark2.png', confidence=0.8)
                if vpn_extension2_location is not None:
                    if initial_state:
                        navigate_to_url(chrome_window, target_url, 15)
                    else:
                        navigate_to_url(chrome_window, "https://www.google.com", 3)
                    window_states[chrome_path] = initial_state
                else:
                    print("No se encontró la extensión de Surfshark VPN en la pantalla")
            except ImageNotFoundException:
                print("No se encontró ninguna de las extensiones de Surfshark VPN en la pantalla")
    else:
        print("No se encontró la ventana de Google Chrome")

# Diccionario para mantener el mapeo entre rutas de Chrome y ventanas
chrome_windows = {path: None for path in chrome_paths}

# Solicitar la URL de la página objetivo
target_url = get_target_url()

# Inicialmente cargar entre 16 y 22 ventanas viendo la página objetivo
initial_target_count = random.randint(16, 22)
print(f"Inicialmente {initial_target_count} ventanas verán la página objetivo y {22 - initial_target_count} verán Google.")

# Abrir y conectar cada instancia de Chrome a la ubicación correspondiente
for i, (chrome_path, location) in enumerate(zip(chrome_paths, vpn_locations), start=1):
    initial_state = (i <= initial_target_count)
    open_chrome_and_connect(chrome_path, location, i, initial_state, target_url)
    # Actualizar el diccionario con la ventana abierta
    for window in gw.getWindowsWithTitle('Google Chrome'):
        if window not in chrome_windows.values():
            chrome_windows[chrome_path] = window
            break

print("Todas las instancias de Chrome están conectadas a las ubicaciones VPN correspondientes.")

# Funciones adicionales para cambiar a Google y volver a la página objetivo
def switch_to_google(chrome_window, instance_name):
    chrome_window.restore()
    chrome_window.activate()
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'l')
    pyautogui.typewrite("https://www.google.com")
    pyautogui.press('enter')
    time.sleep(3)
    chrome_window.minimize()
    print(f"{instance_name} ha cambiado a google.com")

def switch_to_target(chrome_window, instance_name):
    chrome_window.restore()
    chrome_window.activate()
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'l')
    pyautogui.typewrite(target_url)
    pyautogui.press('enter')
    time.sleep(15)
    chrome_window.minimize()
    print(f"{instance_name} ha vuelto a la página objetivo")

# Función para cerrar todas las ventanas de Chrome inmediatamente
def close_all_windows_immediately():
    for proc in subprocess.Popen(['tasklist'], stdout=subprocess.PIPE).communicate()[0].splitlines():
        if b"GoogleChromePortable" in proc:
            pid = int(proc.split()[1])
            subprocess.Popen(['taskkill', '/F', '/PID', str(pid)])

# Función para cerrar todas las ventanas de Chrome progresivamente
def close_all_windows_progressively():
    for path, window in chrome_windows.items():
        if window:
            window.close()
            print(f"Cerrando {path.split('\\')[-2]}")
            time.sleep(30)

# Señal de cierre
def signal_handler(sig, frame):
    print('Ctrl + C detectado.')
    choice = input('¿Deseas cerrar todas las ventanas de inmediato (i) o progresivamente (p)? ')
    if choice.lower() == 'i':
        print('Cerrando todas las ventanas de inmediato...')
        close_all_windows_immediately()
    elif choice.lower() == 'p':
        print('Cerrando todas las ventanas progresivamente...')
        close_all_windows_progressively()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Bucle principal para ajustar el número de ventanas viendo la página objetivo entre 16 y 22
while True:
    current_target_count = sum(window_states.values())
    if current_target_count < 16:
        windows_to_switch = random.sample([path for path, state in window_states.items() if not state], 1)
        for path in windows_to_switch:
            switch_to_target(chrome_windows[path], path.split("\\")[-2])
            window_states[path] = True
        print(f"Ahora hay {current_target_count + 1} ventanas viendo la página objetivo. Se aumentó una ventana.")
    elif current_target_count > 22:
        windows_to_switch = random.sample([path for path, state in window_states.items() if state], 1)
        for path in windows_to_switch:
            switch_to_google(chrome_windows[path], path.split("\\")[-2])
            window_states[path] = False
        print(f"Ahora hay {current_target_count - 1} ventanas viendo la página objetivo. Se disminuyó una ventana.")
    else:
        action = random.choice(['switch_to_google', 'switch_to_target'])
        number_of_windows = random.randint(1, 2)  # Variabilidad entre 1 y 2
        if action == 'switch_to_google':
            windows_to_switch = random.sample([path for path, state in window_states.items() if state], min(number_of_windows, current_target_count))
            for path in windows_to_switch:
                switch_to_google(chrome_windows[path], path.split("\\")[-2])
                window_states[path] = False
            print(f"Ahora hay {current_target_count - len(windows_to_switch)} ventanas viendo la página objetivo. Se cambiaron {len(windows_to_switch)} ventanas a Google.")
        elif action == 'switch_to_target':
            windows_to_switch = random.sample([path for path, state in window_states.items() if not state], min(number_of_windows, 22 - current_target_count))
            for path in windows_to_switch:
                switch_to_target(chrome_windows[path], path.split("\\")[-2])
                window_states[path] = True
            print(f"Ahora hay {current_target_count + len(windows_to_switch)} ventanas viendo la página objetivo. Se cambiaron {len(windows_to_switch)} ventanas a la página objetivo.")

    # Esperar 60 segundos antes de ajustar nuevamente
    time.sleep(60)