from pymodbus.client import ModbusSerialClient as ModbusClient
import time

client = ModbusClient(
	port = '/dev/rs485',
	baudrate = 9600,
	parity = 'N',
	stopbits = 1,
	bytesize = 8,
	timeout = 1
	)

if not client.connect():
	print("ERROR AL CONECTAR")
	exit()

def apagarPorError():
	print("##--## MOTOR APAGADO POR ERROR EN CONEXION ##--##")
	escribirSalida(0,0,31)

def escribirSalida(direccion,valor,esclavo):
	lectura = client.write_coil(direccion,valor,esclavo)
	print("Direccion:",direccion," Valor:",valor," Esclavo:",esclavo)
	while lectura.isError():
		lectura = client.write_coil(direccion,valor,esclavo)
		timeout += 1
		print("ERROR ",timeout," EN LA ESCRITURA")
		if timeout == 10:
			apagarPorError()
			break
		time.sleep(5)

def leerDigital(direccion,esclavo):
	timeout = 0
	lectura = client.read_discrete_inputs(direccion,1,esclavo)
	while lectura.isError():
		lectura = client.read_discrete_inputs(direccion,1,esclavo)
		timeout += 1
		print("ERROR ",timeout," EN LA LECTURA")
		if timeout == 10:
			apagarPorError()
			break
		time.sleep(5)
	print("Direccion:",direccion," Valor:",lectura," Esclavo:",esclavo)
	return lectura.bits[0]

def leerSalida(direccion,esclavo):
	lectura = read_coils(direccion,esclavo)
	while lectura.isError():
		lectura = read_coils(direccion,esclavo)
		timeout += 1
		print("ERROR ",timeout," EN LA LECTURA")
		if timeout == 10:
			apagarPorError()
			break
		time.sleep(5)
	print("---",lectura.bits[0],"---")
	return lectura.bits[0]

def automatizmoMotor(DI1,DI2):
	if not DI1 and not DI2:
		print("--- Encender motor ---")
		return True
	elif DI1 and DI2:
		print("--- Apagar motor ---")
		return False
	else:
		print("--- Se queda igual ---")
		return leerSalida(0,31)



try:
	while True:
		print("########## Empezando lectura ##########")
		DI1 = leerDigital(0,32)
		DI2 = leerDigital(1,32)
		escribirSalida(0,automatizmoMotor(DI1,DI2),31)
		print("########## Esperando 5 segundos ##########")
		time.sleep(5)

except Exception as e:
	print(e)
finally:
	client.close()
