from pyModbusTCP.client import ModbusClient
import time
import keyboard

SERVER_HOST = "localhost"
SERVER_PORT = 502

c = ModbusClient()

# define modbus server host, port
c.host(SERVER_HOST)
c.port(SERVER_PORT)

toggle = True

while True:
    # open or reconnect TCP to server
    if not c.is_open():
        if not c.open():
            print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))

    # if open() is ok, write coils (modbus function 0x01)
    if c.is_open():
        vIn = 0
        canoIn = False
        vOut = 0
        canoOut = False
        aux = 0
        nivel = 50
        ledAlarm = False
        while(1):
            # Valve Control
            if(keyboard.is_pressed('q')):
                aux = vIn - 10
                vIn = 0 if (aux<10) else aux
                pass
            elif (keyboard.is_pressed('w')):
                aux = vIn + 10
                vIn = 100 if (aux>90) else aux
                pass
            elif (keyboard.is_pressed('o')):
                aux = vOut - 10
                vOut = 0 if (aux<10) else aux
                pass
            elif (keyboard.is_pressed('p')):
                aux = vOut + 10
                vOut = 100 if (aux>90) else aux
                pass

            #System
            canoIn = True if (vIn>0) else False
            canoOut = True if (vOut>0) else False

            aux = nivel + vIn/10 - vOut/10
            nivel = 100 if (aux > 99) else (0 if (aux<1) else aux)
            
            ledAlarm = True if (nivel >= 75) else False
            vIn = 0 if (nivel==100) else vIn
            
            # Sending Data to ScadaBr
            c.write_single_register(0, vIn)
            c.write_single_register(1, vOut)
            c.write_single_register(2, nivel)
            c.write_single_coil(3, canoIn)
            c.write_single_coil(4, canoOut)
            c.write_single_coil(5, ledAlarm)
            
            # Terminal Data Printing
            print("vIn: %d" %vIn)
            print("vOut: %d" %vOut)
            print("Nivel: %d" %nivel)

            # Waiting Time    
            time.sleep(0.2)    