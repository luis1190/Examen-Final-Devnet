from ncclient import manager

# Datos de conexion al CSR1000v
HOST = "192.168.56.101"
PORT = 830
USER = "cisco"
PASS = "cisco123!"

def configurar_router():
    print("--- CONECTANDO AL ROUTER VIA NETCONF (SSH:830) ---")
    try:
        with manager.connect(
            host=HOST,
            port=PORT,
            username=USER,
            password=PASS,
            hostkey_verify=False,
            device_params={'name': 'csr'}
        ) as m:
            print(" Conexión exitosa mediante NETCONF!\n")

          
            nuevo_hostname = "Luis-Bustos"
            
            hostname_xml = f"""
            <config>
              <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                <hostname>{nuevo_hostname}</hostname>
              </native>
            </config>
            """
            
            print(f"Cambiando el hostname del router a: {nuevo_hostname}...")
            m.edit_config(target='running', config=hostname_xml)
            print(" Hostname cambiado con éxito.\n")

            # 2. Crear Interfaz Loopback 11 con IP 11.11.11.11/32
            loopback_xml = """
            <config>
              <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                <interface>
                  <Loopback>
                    <name>11</name>
                    <description>Loopback 11 creada via NETCONF - Examen Devnet</description>
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
            
            print("Creando la interfaz Loopback 11 (11.11.11.11/32)...")
            m.edit_config(target='running', config=loopback_xml)
            print(" Loopback 11 creada con éxito.\n")

    except Exception as e:
        print(f" Error al conectar o aplicar configuracion: {e}")

if __name__ == "__main__":
    configurar_router()
