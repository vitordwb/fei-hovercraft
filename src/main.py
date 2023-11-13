# Codigo projeto embarcados :: hovercraft
# Autor: Vitor Watanabe
# github/vitordwb
# © MIT License

from machine import Pin, PWM
import network
import time
from time import sleep
from umqtt.robust import MQTTClient
import sys

print('running main')

#===============================================================
# MQTT
#===============================================================

CLIENT_NAME = 'vitor-teste'
MQTT_BROKER_URL = '10.3.141.1'

client = MQTTClient(CLIENT_NAME, MQTT_BROKER_URL)

try:
    client.connect()
    print('mqtt connected')
except Exception as e:
    print('ERROR | nao foi possivel conectar ao servidor MQTT {}{}'.format( type(e).__name__, e) )
    sys.exit()


#===============================================================
# Funcao callback
# Esta funcao eh executada quando algum dispositivo publica uma
# mensagem em um topico em que seu ESP esta inscrito.
# Altere a funcao abaixo para adicionar a logica ao seu programa,
# para que quando um dispositivo publicar uma mensagem em um
# topico que seu ESP esteja inscrito, voce possa executar uma funcao.
#===============================================================

def cb(topic, msg):
    print('received data:  TOPIC = {}, MSG = {}'.format( topic, msg ))
    # Para recepcao de dados do tipo numerico, eh necessario
    # converter o texto em numero
    # Recebendo os dados:
        #recieved_data = str(msg,'utf-8')
        #if recieved_data == "0":
        #    led.value(0)
        #if recieved_data == "1":
        #    led.value(1)
    if topic == b'motor_base/power':
        if msg == b'true':
            motors_base.value(1)
        else:
            motors_base.value(0)
        
    if topic == b'motor_direction/right':
        motor_right.duty( int( msg.decode() ) )
        
    if topic == b'motor_direction/left':
        motor_left.duty( int( msg.decode() ) )
        

# Pinos a utilizar para os LEDs com o ESP32
motors_base           = Pin(2, Pin.OUT)
MOTORS_BASE_TOPIC     = b'motor_base/power'

motor_direction_left  = Pin(15, Pin.OUT)
MOTOR_LEFT_TOPIC      = b'motor_direction/left'

motor_direction_right = Pin(4, Pin.OUT)
MOTOR_RIGHT_TOPIC     = b'motor_direction/right'

# Definindo PWM
motor_left  = PWM(motor_direction_left, freq=1000, duty=0)
motor_right = PWM(motor_direction_right, freq=1000, duty=0)

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
        client.check_msg()
#         client.publish( BTN_TOPIC, str(btn.value()).encode() )
        
    except: # Caso a conexao for perdida
        client.disconnect()
        sys.exit()

