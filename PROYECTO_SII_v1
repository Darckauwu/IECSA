from pymodbus.client import ModbusSerialClient as ModbusClient #Libreria necesaria para utilizar modbus
import time #Libreria necesaria para detener el código X segundos

client = ModbusClient( #Se formula el cliente
        port = '/dev/rs485', #Puerto a utilizar (rs485)
        baudrate = 9600, #El baudage de la conexión (9600)
        parity = 'N', #La paridad (None)
        stopbits = 1, #El bit de parada (1)
        bytesize = 8, #Tamaño de byte (8)
        timeout = 1 #Timeout para la conexión (1)
        )

if not client.connect(): #Sí al hacer la conexión hay un error, entra aquí
        print("ERROR AL CONECTAR") #log
        exit() #Cierra el script

def apagarPorError(): #Funcion para apagar el motor si no se ha podido leer/escribir una variable
        timeout = 0 #intentos
        while True: #Mantiene el código corriendo permanentemente hasta que decida que hacer
                escritura = client.write_coil(0,0,31) #Manda a apagar el motor
                if not escritura.isError(): #Sí no hubo errores entra aquí
                        print("##--## MOTOR APAGADO POR ERROR EN CONEXION ##--##")
                        break #Rompe el while para seguir con el código
                time.sleep(5) #Espera X segundos para volver a intentar a apagar el motor
        #Este código se mantiene ejecutado hasta que se pueda apagar el motor. Sí no se apaga el motor, se quedará aquí para siempre.

def leerDigital(direccion,esclavo): #funcion para leer digitales
        global errorDigitales
        timeout = 0 #intentos
        while True: #Mantiene el código corriendo permanentemente hasta que decida que hacer
                lectura = client.read_discrete_inputs(direccion,1,esclavo) #Lee la digital por medio de modbus
                if not lectura.isError(): #Sí la lectura no tuvo errores entra aquí
                        print("Direccion:",direccion," Valor:",lectura," Esclavo:",esclavo) #log
                        errorDigitales = False
                        return lectura.bits[0] #Regresa el valor de la digital
                #Sí hubo error en la lectura continúa aquí el código
                timeout += 1 #Se agrega un intento
                print("ERROR ",timeout," EN LA LECTURA") #log
                if timeout == 10: #Sí se cumplen 10 intentos entra aquí
                        apagarPorError() #Manda a apagar el motor por seguridad
                        errorDigitales = True
                        return False #Regresa un valor falso (0) para salir de la función
                time.sleep(5) #Espera X segundos para volver a intentar a leer la digital

def escribirSalida(direccion,valor,esclavo): #Funcion para encender/apagar una salida
        timeout = 0 #intentos
        while True: #Mantiene el código corriendo permanentemente hasta que decida que hacer
                escritura = client.write_coil(direccion,valor,esclavo) #Escribe la salida por medio de modbus
                if not escritura.isError(): #Sí la lectura no tuvo errores entra aquí
                        print("Direccion:",direccion," Valor:",escritura," Esclavo:",esclavo) #log
                        break #Rompe el while para salir de la función
                #Sí hubo error en la lectura continúa aquí el código
                timeout += 1 #Se agrega un intento
                print("ERROR ",timeout," EN LA ESCRITURA") #log
                if timeout == 10: #Sí se cumplen 10 intentos entra aquí
                        apagarPorError() #Manda a apagar el motor por seguridad
                        break #Rompe el while para salir de la función
                time.sleep(5)#Espera X segundos para volver a intentar a leer la digital

def leerSalida(direccion,esclavo): #funcion para leer el estado de la salida al motor
        timeout = 0 #intentos
        while True: #Mantiene el código corriendo permanentemente hasta que decida que hacer
                lectura = client.read_coils(direccion,1,esclavo) #Lee la salida por medio de modbus
                if not lectura.isError(): #Sí la lectura no tuvo errores entra aquí
                        print("Direccion:",direccion," Valor:",lectura," Esclavo:",esclavo) #log
                        return lectura.bits[0] #Regresa el valor de la digital
                #Sí hubo error en la lectura continúa aquí el código
                timeout += 1 #Se agrega un intento
                print("ERROR ",timeout," EN LA LECTURA") #log
                if timeout == 10: #Sí se cumplen 10 intentos entra aquí
                        apagarPorError() #Manda a apagar el motor por seguridad
                        return False #Regresa un valor falso (0) para salir de la función
                time.sleep(5) #Espera X segundos para volver a intentar a leer la digital

def automatizmoMotor(DI1,DI2): #funcion para decidir que hacer con el motor (encender/apagar)
        if not DI1 and not DI2: #Sí los flotadores están abajo (0,0) entra aquí
                print("--- Encender motor ---") #log
                return True #Regresa el valor para encender el motor
        elif DI2: #Sí los flotadores están arriba (1,1) entra aquí
                print("--- Apagar motor ---") #log
                return False #Regresa el valor para apagar el motor
        else: #Sí no se cumple lo anterior quiere decir que el agua está a la mitad (llenandose/vaciandose)
                print("--- Se queda igual ---") #log
                return leerSalida(0,31) #Regresa el valor actual del motor (no hay cambios en su estado)

try: #Intenta hacer el código, esto con la finalidad de manejar los errores que pudieran ocurrir
        errorDigitales = False
        while True: # Mantiene el código corriendo permanentemente
                print("########## Empezando lectura ##########") #log
                while True:
                        DI1 = leerDigital(0,32) #Lectura de la digital 1
                        if not errorDigitales:
                                break
                while True:
                        DI2 = leerDigital(1,32) #Lectura de la digital 2
                        if not errorDigitales:
                                break
                escribirSalida(0,automatizmoMotor(DI1,DI2),31) #Apaga o prende el motor con respecto a las digitales
                print("########## Esperando 5 segundos ##########") #log
                time.sleep(5) #Espera X segundos para hacer otra lectura

except Exception as e: #Sí hay algún error en el código lo muestra en pantalla.
        print(e)
finally: #Cierra la sesión con el puerto.
        client.close()
