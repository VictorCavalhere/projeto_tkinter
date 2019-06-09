from database import DB
# from temperatura_aleatoria import temps
from tkinter import *
from tkinter import messagebox
from random import randint
import time

db = DB()



running = False

def get_selected_row(event):
    global selected_tuple
    index = list1.curselection()[0]
    selected_tuple = list1.get(index)
    e1.delete(0, END)
    e1.insert(END, selected_tuple[1])
    e2.delete(0, END)
    e2.insert(END, selected_tuple[2])
    e3.delete(0, END)
    e3.insert(END, selected_tuple[3])
    e14.delete(0, END)
    e14.insert(END, selected_tuple[4])
    e15.delete(0, END)
    e15.insert(END, selected_tuple[5])
    e16.delete(0, END)
    e16.insert(END, selected_tuple[6])


def view_command():
    list1.delete(0, END)
    for row in db.view():
        list1.insert(END, row)


def search_command():
    list1.delete(0, END)
    for row in db.search(title_text.get(), author_text.get(), isbn_text.get()):
        list1.insert(END, row)


def add_command():
    db.insert(title_text.get(), author_text.get(), isbn_text.get(),endereco.get(),data_nasc.get(),data_entrada.get() )
    list1.delete(0, END)
    list1.insert(END, (title_text.get(), author_text.get(), isbn_text.get(),endereco.get(),data_nasc.get(),data_entrada.get() ))


def delete_command():
    db.delete(selected_tuple[0])


def update_command():
    db.update(selected_tuple[0], title_text.get(), author_text.get(), isbn_text.get())

def view_temp():
    list2.delete(0, END)
    list3.delete(0, END)
    list4.delete(0, END)
    id_ = db.select_id(title_text.get(), author_text.get(),isbn_text.get())
    print(id_)
    for row in db.view_temp(id_):
        list2.insert(END, row)
    for row in db.view_pressao(id_):
        list3.insert(END, row)
    for row in db.view_batimento(id_):
        list4.insert(END, row)

def temps(x_temp,y_temp,x_pressao,y_pressao,x_batimento,y_batimento):
    return randint(x_temp,y_temp), randint(x_pressao,y_pressao), randint(x_batimento,y_batimento)


def start_medicao():
    if running:
        id_ = db.select_id(title_text.get(), author_text.get(), isbn_text.get())
        if int(temp[0]) > temp_normal.get(): 
            db.insert_temp(str(temp[0])+"ºC",x,temp_normal.get(),int(id_[0]))
        if int (temp[1]) > pressao_normal.get():
            db.insert_pressao(str(temp[1]) +"PAS",x,pressao_normal.get(),int(id_[0]))
        if int(temp[2]) > batimento_normal.get():
            db.insert_batimento(str(temp[2])+"FC",x,batimento_normal.get(),int(id_[0]))

    window.after(100,start_medicao)

def start():
    global running
    running = True

def stop():
    global running
    running = False

window = Tk()

window.geometry("1000x400") #You want the size of the app to be 500x500


window.title("Maquina recicladora")



def on_closing():
    dd = db
    if messagebox.askokcancel("Quit", "Você gostaria de sair?"):
        window.destroy()
        del dd


window.protocol("WM_DELETE_WINDOW", on_closing)  # handle window closing




l1 = Label(window, text="Operador")
l1.grid(row=0, column=0)

title_text = StringVar()
e1 = Entry(window, textvariable=title_text)
e1.grid(row=0, column=1)

list1 = Listbox(window, height=6, width=50)
list1.grid(row=6, column=0, rowspan=6, columnspan=2)

sb1 = Scrollbar(window)
sb1.grid(row=5, column=2, rowspan=6)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

list1.bind('<<ListboxSelect>>', get_selected_row)


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


window.after(100, start_medicao)
window.mainloop()



