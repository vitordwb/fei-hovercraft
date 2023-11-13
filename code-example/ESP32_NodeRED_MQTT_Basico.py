# Codigo projeto embarcados :: hovercraft
# Ele esta dividido em blocos identificados para facilitar o seu entendimento

# Antes de enviar o código, use Ctrl+C no shell para garantir que o ESP
# não esteja executando o codigo e aguarde ate que apareca o simbolo ">>"
# no shell.
# Direitos reservados:.

#===============================================================
# Bibliotecas
#===============================================================

from machine import Pin
import network
import time
from time import sleep
from umqtt.robust import MQTTClient # necessaria para a comunicacao com o servidor MQTT
import sys


#===============================================================
# Wi-Fi e Node-Red
#===============================================================

# Modifique os dados abaixo para a rede WiFi que o ESP deve se conectar
WIFI_SSID     = 'LUSH.5G'
WIFI_PASSWORD = 'Lush2022!'

mqtt_client_id = bytes('cliente_'+'12321', 'utf-8') # um ID de cliente aleatorio

# Altere a variavel para o endereco IP do seu Raspberry Pi, de forma que
# ele se conecte ao broker MQTT
MQTT_IO_URL = '127.0.0.1:1883'

# Caso o servidor MQTT exija usuario e senha
# MQTT_USERNAME   = 'usuario'
# MQTT_IO_KEY     = 'senha'


#===============================================================
# Leds, botao e variaveis
#===============================================================

# Pinos a utilizar para os LEDs com o ESP32
lampCozinha = Pin(2, Pin.OUT) # Led ligado ao pino D2
lampSuite   = Pin(4, Pin.OUT) # Led ligado ao pino D4
botao       = Pin(5, Pin.OUT) # Botao ligado ao pino D5
btn = Pin(0)

# Guarda a informacao se alguem tocou a campainha
campainha = False

# Contador de tempo para a campainha
ini_tempo = 0

#===============================================================
# Conecta o ESP ao roteador, nao alterar
#===============================================================

def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.disconnect()
    wifi.connect(WIFI_SSID,WIFI_PASSWORD)
    if not wifi.isconnected():
        print('Conectando...')
        timeout = 0
        while (not wifi.isconnected() and timeout < 10):
            print(10 - timeout)
            timeout = timeout + 1
            time.sleep(1) 
    if(wifi.isconnected()):
        print('Conectado')
    else:
        print('Nao conectado')
        sys.exit()

# Conecta ao roteador WiFi
connect_wifi()

# Caso o servidor MQTT nao exija usuario e senha
client = MQTTClient(client_id=mqtt_client_id, 
                    server=MQTT_IO_URL)

# Caso o servidor MQTT exija usuario e senha
# client = MQTTClient(client_id=mqtt_client_id, 
#                     server=MQTT_IO_URL, 
#                     user=MQTT_USERNAME, 
#                     password=MQTT_IO_KEY,
#                     ssl=False)

# Conecta ao cliente
try:
    client.connect()
except Exception as e:
    print('Nao foi possivel conectar ao servidor MQTT {}{}'.format(type(e).__name__, e))
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
    print('Received Data:  Topic = {}, Msg = {}'.format(topic, msg))
    # Para recepcao de dados do tipo numerico, eh necessario
    # converter o texto em numero
    # Recebendo os dados:
        #recieved_data = str(msg,'utf-8')
        #if recieved_data == "0":
        #    led.value(0)
        #if recieved_data == "1":
        #    led.value(1)
    # Caso a mensagem seja um texto, nenhuma conversao eh necessaria
    # Para o topico da lampada da cozinha
    if topic == b'casa/cozinha/lampada':
        if msg == b'troca':
            print('Alterando o estado da lampada da cozinha')
            # Alterna o estado da lampada da cozinha
            lampCozinha.value(not lampCozinha.value())
    # Para o topico da lampada da suite
    if topic == b'casa/suite/lampada':
        if msg == b'troca':
            print('Alterando o estado da lampada da suite')
            # Alterna o estado da lampada da suite
            lampSuite.value(not lampSuite.value())


#===============================================================
# Assinar ou assinar novamente um topico
# Voce pode se inscrever em mais tópicos (para controlar
# mais LEDs neste exemplo)
#===============================================================

# Funcao Callback
client.set_callback(cb)

# Inscricao nos topicos
client.subscribe(b'casa/cozinha/lampada')
client.subscribe(b'casa/suite/lampada')
client.subscribe(b'casa/hall/campainha')


#===============================================================
# Sua funcao
#===============================================================

while True:
    try:
        #==================================
        # Wi-Fi - Funcao que verifica o recebimento de novas mensagens
        client.check_msg()
        #print("Verificando a mensagem...")
        #==================================
        # Monitora o botao da campainha do hall
        # Se o botao da campainha for pressionado:
        if botao.value() and not campainha:
            print('Campainha tocando...')
            client.publish(b'casa/hall/campainha', b'Campainha tocando')
            campainha = True
            ini_tempo = time.ticks_ms()
        # Se o botao da campainha nao for pressionado:
        if (time.ticks_diff(time.ticks_ms(), ini_tempo) > 5000) and campainha:
            print('Aguardando visita...')
            client.publish(b'casa/hall/campainha', b'Aguardando visita')
            campainha = False
            ini_tempo = time.ticks_ms()
    except: # Caso a conexao for perdida
        client.disconnect()
        sys.exit()
