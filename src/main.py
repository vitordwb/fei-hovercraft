# Projeto de Sistemas Embarcados :: hovercraft
# Autor: Vitor Watanabe
# github/vitordwb
# © MIT License

#===============================================================
# BIBLIOTECAS
#===============================================================

from machine import Pin, PWM
import network
import time
from time import sleep
from umqtt.robust import MQTTClient
import sys
import network
import time

#===============================================================
# WIFI
#===============================================================

WIFI_SSID     = "raspi-webgui-02" # nome do wifi
WIFI_PASSWORD = 'raspberrypi'     # senha do wifi
MAX_RETRIES   = 50                # qtd de tentativas p/ conectar no wifi

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
        time.sleep(2)
        retries += 1

    return wifi.isconnected()

wifi = connect_wifi()

if wait_for_connection(wifi):
    print('SUCCESS | wifi connected')
else:
    print('ERROR | não foi possível conectar')
    sys.exit()

#===============================================================
# MQTT
#===============================================================

CLIENT_NAME = 'vitor-teste'    # nome do cliente
MQTT_BROKER_URL = '10.3.141.1' # url do broker do mqtt

client = MQTTClient(CLIENT_NAME, MQTT_BROKER_URL) # conexao com broker

time.sleep(3) # espera 3 segundos p/ conectar no mqtt

while True:
    try:
        client.connect()
        print('SUCCESS | mqtt connected')
        break  # sai do loop se a conexão for bem-sucedida
    except Exception as e:
        time.sleep(2)  # espera 2 segundos antes de tentar novamente

#===============================================================
# Funcao Callback
# esta funcao é executada quando algum dispositivo publica uma
# mensagem em um topico em que seu ESP esta inscrito
#===============================================================

def cb(topic, msg):
    print('received data:  TOPIC = {}, MSG = {}'.format( topic, msg ))

    if topic == b'motors_base/power':
        motors_base.duty( int( msg.decode() ) )
        
    if topic == b'motor_direction/right':
        motor_right.duty( int( msg.decode() ) )
        
    if topic == b'motor_direction/left':
        motor_left.duty( int( msg.decode() ) )
        

# Pinos a utilizar para os LEDs com o ESP32
base                  = Pin(2)
MOTORS_BASE_TOPIC     = b'motors_base/power'

motor_direction_left  = Pin(15)
MOTOR_LEFT_TOPIC      = b'motor_direction/left'

motor_direction_right = Pin(4)
MOTOR_RIGHT_TOPIC     = b'motor_direction/right'

# Definindo PWM
motor_left  = PWM(motor_direction_left, freq=1000, duty=0)
motor_right = PWM(motor_direction_right, freq=1000, duty=0)
motors_base = PWM(base, freq=1000, duty=0)


# Funcao Callback
client.set_callback(cb)

# Inscricao nos topicos
client.subscribe(MOTORS_BASE_TOPIC)
client.subscribe(MOTOR_LEFT_TOPIC)
client.subscribe(MOTOR_RIGHT_TOPIC)

#===============================================================
# Função
#===============================================================

while True:
    try:
        client.check_msg() # verifica mensagens
        
    except: # caso a conexao for perdida
        client.disconnect()
        sys.exit()
