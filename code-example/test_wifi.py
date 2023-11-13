import network

# Defina o nome da sua rede (SSID) e a senha
SSID = 'nome_da_sua_rede'
PASSWORD = 'sua_senha'

# Ativa a interface Wi-Fi
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

# Conecta à rede Wi-Fi
sta_if.connect(SSID, PASSWORD)

# Aguarda até que a conexão seja estabelecida
while not sta_if.isconnected():
    pass

# Quando conectado, imprime informações sobre a conexão
print('Conectado à rede Wi-Fi')
print('Endereço IP:', sta_if.ifconfig()[0])