from ncclient import manager

# Credenciales y datos del Router
ROUTER_IP = "192.168.56.105"
USERNAME = "cisco"
PASSWORD = "cisco"
PORT = 830

# Payload XML con los requerimientos del examen
config_xml = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname>Julio_Martinez</hostname>
    <interface>
      <Loopback>
        <name>11</name>
        <ip>
          <address>
            <primary>
              <address>11.11.11.11</address>
              <mask>255.255.255.255</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
    </interface>
  </native>
</config>
"""

def main():
    print(f"Conectando al router {ROUTER_IP} por SSH usando NETCONF (Puerto {PORT})...")
    try:
        # Iniciando sesión con el router
        with manager.connect(host=ROUTER_IP, port=PORT, username=USERNAME, password=PASSWORD, hostkey_verify=False) as m:
            print("Conexión exitosa. Aplicando configuración...")
            # Enviando la configuración XML
            respuesta = m.edit_config(target='running', config=config_xml)
            print("¡Configuración aplicada correctamente!")
            print(respuesta)
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == '__main__':
    main()
