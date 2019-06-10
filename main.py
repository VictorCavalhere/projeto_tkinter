from database import DB
# from temperatura_aleatoria import temps
from tkinter import *
from tkinter import messagebox
from random import randint
from datetime import datetime, timezone
from threading import Lock, Thread
import time
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)



db = DB()
data = datetime.now()
nome_cliente = input(str("Digite o nome do cliente: "))
nome_operador = input(str("Digite o nome do operador: "))
numero_serie_maq = int(input("Digite o numero de série da maquina: "))
db.insert_cliente(nome_cliente,data)
db.insert_operador(nome_operador,data)
id_cl = db.select_id_cliente(nome_cliente)[0]
id_op = db.select_id_operador(nome_operador)[0]
db.insert_maquina(numero_serie_maq,data,id_op,id_cl)
num = db.select_id_maquina(numero_serie_maq)[0]
db.insert_capsula(0,data,num)
x=0
print("Argudando entrada")
while True:
    if GPIO.input(23) == 1:
       x+=1
       db.update_capsula(x,data,num)
       GPIO.output(18,GPIO.HIGH)
       time.sleep(1)
       capsulas = db.view_capsula(num)[0]
       operador = db.select_id_operador(nome_operador)[1]
       print("| Cliente: "+nome_cliente+"| Operador: "+operador+"| Quantiade de Capsulas: "+str(capsulas)+"| Maquina: "+str(num))
       GPIO.output(18,GPIO.LOW)
       print("Aguardando Entrada")
