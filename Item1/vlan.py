def verificar_vlan():
    try:
        vlan = int(input("Ingrese el número de VLAN: "))

        if 1 <= vlan <= 1005:
            print(f"La VLAN {vlan} corresponde a un rango NORMAL de VLAN.")

        elif 1006 <= vlan <= 4094:
            print(f"La VLAN {vlan} corresponde a un rango EXTENDIDO de VLAN.")

        else:
            print(f"La VLAN {vlan} no corresponde a una VLAN válida.")

    except ValueError:
        print("Error: debe ingresar un número entero.")

if __name__ == "__main__":
    verificar_vlan()

