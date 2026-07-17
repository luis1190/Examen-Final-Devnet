# vlan_rev.py
try:
    vlan = int(input("Ingrese el número de VLAN a consultar: "))
    
    if 1 <= vlan <= 1005:
        print(f"La VLAN {vlan} corresponde al Rango Normal (1 - 1005).")
    elif 1006 <= vlan <= 4094:
        print(f"La VLAN {vlan} corresponde al Rango Extendido (1006 - 4094).")
    else:
        print(f"El número {vlan} NO corresponde a una VLAN válida (Rango válido: 1 - 4094).")
except ValueError:
    print("Error: Por favor, ingrese un número entero válido.")
