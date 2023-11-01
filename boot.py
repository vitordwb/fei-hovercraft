import network
import time

print('hello vitor')
print('running boot')

WIFI_SSID     = "raspi-webgui-02"
WIFI_PASSWORD = 'raspberrypi'
MAX_RETRIES = 50

def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.disconnect()
    wifi.connect(WIFI_SSID, WIFI_PASSWORD)
    return wifi

def wait_for_connection(wifi):
    retries = 0
    while not wifi.isconnected() and retries < MAX_RETRIES:
        print(f"{retries+1}/{MAX_RETRIES}")
        time.sleep(1)
        retries += 1

    return wifi.isconnected()

def main():
    wifi = connect_wifi()

    if wait_for_connection(wifi):
        print('Wifi Connected')
    else:
        print('ERROR | Não foi possível conectar')
        sys.exit()

# Conecta ao roteador WiFi
main()
