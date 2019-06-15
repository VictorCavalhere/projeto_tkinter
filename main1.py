from database import DB
# from temperatura_aleatoria import temps
from tkinter import *
from tkinter import messagebox
from random import randint
from datetime import datetime, timezone
from threading import Lock, Thread
import time
import RPi.GPIO as GPIO

db = DB()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


running = False

def get_selected_row(event):
    global selected_tuple
    index = list1.curselection()[0]
    selected_tuple = list1.get(index)
    e1.delete(0, END)
    e1.insert(END, selected_tuple[0])
    e2.delete(0, END)
    e2.insert(END, selected_tuple[1])
    e3.delete(0, END)
    e3.insert(END, selected_tuple[2])


def add_command():
    data = datetime.now()
    db.insert_operador(operador.get(),data)
    db.insert_cliente(cliente.get(),data)
    id_cliente = db.select_id_cliente(cliente.get())[0]
    id_operador = db.select_id_operador(operador.get())[0]
    db.insert_maquina(numero_maquina.get(),data,id_operador,id_cliente)
    id_maq = db.select_id_maquina(numero_maquina.get())[0]
    db.insert_capsula(0,id_maq)
    list1.delete(0, END)
    #list1.insert(END, (operador.get(),data))


def view_command():
    list1.delete(0, END)
    for row in db.view():
        list1.insert(END, row)


def search_command():
    list1.delete(0, END)
    for row in db.search(title_text.get(), author_text.get(), isbn_text.get()):
        list1.insert(END, row)

def delete_command():
    db.delete(selected_tuple[0])


def update_command():
    db.update(selected_tuple[0], title_text.get(), author_text.get(), isbn_text.get())

def view_temp():
    list2.delete(0, END)
    list3.delete(0, END)
    list4.delete(0, END)
    id_ = db.select_id(title_text.get(), author_text.get(),isbn_text.get())
    for row in db.view_temp(id_):
        list2.insert(END, row)
    for row in db.view_pressao(id_):
        list3.insert(END, row)
    for row in db.view_batimento(id_):
        list4.insert(END, row)

def relatorio():
    id_maq = db.select_id_maquina(numero_maquina.get())[0]
    result = db.relatorio(id_maq)
    print(result)


def start_medicao():
    
    GPIO.output(18,GPIO.LOW)
    if GPIO.input(23) == 1:
        data = datetime.now()
        id_maq = db.select_id_maquina(numero_maquina.get())[0]
        print(id_maq)
        x = db.view_capsula(id_maq)[0]
        x+=1
        db.insert_capsula(x,id_maq)
        GPIO.output(18,GPIO.HIGH)
        time.sleep(1)
        capsulas = db.view_capsula(id_maq)[0]
        list2.delete(0, END)
        list2.insert(END, "| Cliente: "+str(cliente.get())+"| Operador: "+str(operador.get())+"| Quantiade de Capsulas: "+str(capsulas)+"| Maquina: "+str(id_maq))
        if GPIO.wait_for_edge(23, GPIO.FALLING, timeout=50000):
            GPIO.output(18,GPIO.LOW)
        print("Aguardando Entrada")
    window.after(100,start_medicao)

def start():
    global running
    print("aguardando")
    running = True

def stop():
    global running
    running = False

window = Tk()

window.geometry("1000x400") #You want the size of the app to be 500x500


window.title("Maquina recicladora de capsula de café")



def on_closing():
    dd = db
    if messagebox.askokcancel("Quit", "Você gostaria de sair?"):
        window.destroy()
        del dd


window.protocol("WM_DELETE_WINDOW", on_closing)  # handle window closing




l1 = Label(window, text="Operador")
l1.grid(row=0, column=0)

operador = StringVar()
e1 = Entry(window, textvariable=operador)
e1.grid(row=0, column=1)

l2 = Label(window, text="Cliente")
l2.grid(row=1, column=0)

cliente = StringVar()
e2 = Entry(window, textvariable=cliente)
e2.grid(row=1, column=1)

l3 = Label(window, text="Numero maquina")
l3.grid(row=2, column=0)

numero_maquina = StringVar()
e3 = Entry(window, textvariable=numero_maquina)
e3.grid(row=2, column=1)

l4 = Label(window, text="Cadastros")
l4.grid(row=4, column=0)

list1 = Listbox(window, height=6, width=35)
list1.grid(row=4, column=0, rowspan=6, columnspan=2)

sb1 = Scrollbar(window)
sb1.grid(row=4, column=2, rowspan=6)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

list1.bind('<<ListboxSelect>>', get_selected_row)

l5 = Label(window, text="Registros")
l5.grid(row=1, column=5)

list2 = Listbox(window, height=3, width=60)
list2.grid(row=0, column=5, rowspan=6, columnspan=2)

l6 = Label(window, text="Relatorio")
l6.grid(row=1, column=5)


b1 = Button(window, text="Consultar todos", width=18, command=view_command)
b1.grid(row=2, column=3)

b2 = Button(window, text="Procurar entrada", width=18, command=search_command)
b2.grid(row=3, column=3)

b3 = Button(window, text="Adicionar entrada", width=18, command=add_command)
b3.grid(row=4, column=3)

b4 = Button(window, text="Atualizar selecionado", width=18, command=update_command)
b4.grid(row=5, column=3)

b5 = Button(window, text="Deletar selecionado", width=18, command=delete_command)
b5.grid(row=6, column=3)

b6 = Button(window, text="Fechar", width=18, command=window.destroy)
b6.grid(row=7, column=3)

b6 = Button(window, text="Gerar relatorio", width=18, command=relatorio)
b6.grid(row=8, column=3)


window.after(100, start_medicao)
window.mainloop()
