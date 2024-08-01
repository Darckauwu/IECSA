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

def escribirSalida(direccion,valor,esclavo):
	client.write_coil(direccion,valor,esclavo)

def leerDigital(direccion,esclavo):
	timeout = 0
	lectura = client.read_discrete_inputs(direccion,1,esclavo)
	error = lectura.isError()
	while error:
		time.sleep(5)
		lectura = leerDigital(direccion,esclavo)
		error = lectura.isError()
		timeout += 1
		print("ERROR ",timeout," EN LA LECTURA")
		if timeout == 10:
			escribirSalida(0,0,32)
			escribirSalida(1,0,32)
	return lectura.bits[0]

def leerSalida(direccion,esclavo):
	lectura = read_coils(direccion,esclavo)
	return lectura.bits[0]

def automatizmoMotor(DI1,DI2):
	if not DI1 and not DI2:
		return true
	elif D1 and DI2:
		return false
	else:
		return leerSalida(0,31)



try:
	while True:
		DI1 = leerDigital(0,32)
		DI2 = leerDigital(1,32)
		escribirSalida(0,automatizmoMotor(DI1,DI2),31)
		time.sleep(5)

print(leerD(2))
except Exception as e:
	raise e
finally:
	client.close()