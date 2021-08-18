'''
Autores:
Daniel grazzina
Ricardo Sanchez

Correo:
danielaugustogra@gmail.com
rikygabriel13@gmail.com

Intrefaz Grafica: Tkinter
Programacion Logica: Python
Base de Datos: SQLite3

Version 2.2 Estable
Fecha de Lanzamiento: 20/04/2021
'''

from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from tkinter import PhotoImage
from idlelib.tooltip import Hovertip
from datetime import datetime
import webbrowser
import time
import sys
import os
import sqlite3

tu_clave=[]
seleccion=""
op_producto=9
op_cliente=9
op_pedido=9
clean_total=0
resultado=[]
now = datetime.now()
str_now = now.strftime("%d/%m/%Y")

#Consigue la ruta absoluta de los archivos
def resolver_ruta(ruta_relativa):
    try:
        ruta_base = sys._MEIPASS
    except Exception:
        ruta_base = os.path.abspath(".")

    return os.path.join(ruta_base, ruta_relativa)

def manual():
    ruta_pdf = resolver_ruta('Informe_Proyecto_Base_De_Datos.pdf')
    webbrowser.open_new(ruta_pdf)

#Si la base de datos no existe la crea
def crear_base():
    nombre_base = resolver_ruta('inventario.db')
    conn = sqlite3.connect(nombre_base)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='producto'")
    result = cursor.fetchone()
    if result == None:
        cursor.execute("CREATE TABLE producto( ID_PRODUCTO VARCHAR(15) NOT NULL PRIMARY KEY, PRECIO_COSTO REAL NOT NULL, PRECIO_VENTA REAL NOT NULL, CANTIDAD_PRODUCTO INTEGER NOT NULL)")

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cliente'")
    result = cursor.fetchone()
    if result == None:
        cursor.execute("CREATE TABLE cliente( CI_CLIENTE VARCHAR(10) NOT NULL PRIMARY KEY, NOMBRE VARCHAR(20) NOT NULL, APELLIDO VARCHAR(20) NOT NULL, TELEFONO VARCHAR(15) NOT NULL, DIRECCION VARCHAR(50) NOT NULL, DEUDA REAL NOT NULL)")

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pedido'")
    result = cursor.fetchone()
    if result == None:
        cursor.execute("CREATE TABLE pedido( ID_PEDIDO INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, CI_CLIENTE VARCHAR(10) NOT NULL, ID_PRODUCTO VARCHAR(15) NOT NULL, CANTIDAD_PEDIDO INTEGER NOT NULL, FECHA VARCHAR(10) NOT NULL)")
    conn.commit()
    conn.close()

crear_base()

#Realiza la mayoria de los query en el programa
def base_datos(op_BD, tabla, tu_clave = [], seleccion="", op_producto=9, op_cliente=9, op_pedido=9, clean_total=0):
    # conexion base de datos
    nombre_base = resolver_ruta('inventario.db')
    miconexion=sqlite3.connect(nombre_base)
    micursor=miconexion.cursor()
    
    if op_BD == 0:
        # consultar
        if tabla ==  0:
            # tabla producto
            if op_producto == 0:
                #id_producto
                micursor.execute("SELECT * FROM producto WHERE ID_PRODUCTO = ?",(seleccion, ))
                resultado=micursor.fetchone()
                return resultado   
            elif op_producto == 1:
                # precio_costo
                micursor.execute("SELECT * FROM producto WHERE PRECIO_COSTO = ?",seleccion)
                resultado=micursor.fetchone()
                return resultado
            elif op_producto == 2:
                # precio_venta
                micursor.execute("SELECT * FROM producto WHERE PRECIO_VENTA = ?",seleccion)
                resultado=micursor.fetchone()
                return resultado
            elif op_producto == 3:
                # cantidad_pro
                micursor.execute("SELECT * FROM producto WHERE CANTIDAD_PRODUCTO = ?",seleccion)
                resultado=micursor.fetchone()
                return resultado
            elif op_producto == 4:
                micursor.execute("SELECT * FROM producto ORDER BY ID_PRODUCTO DESC")
                resultado=micursor.fetchall()
                return resultado
        elif tabla == 1:
            # tabla cliente
            if op_cliente == 0:
                # Cedula
                micursor.execute("SELECT * FROM cliente WHERE CI_CLIENTE = ?",(seleccion,))
                resultado=micursor.fetchone()
                return resultado
            elif op_cliente == 1:
                # nombre
                micursor.execute("SELECT * FROM cliente WHERE NOMBRE = ?",(seleccion, ))
                resultado=micursor.fetchall()
                return resultado
            elif op_cliente == 2:
                #apellido
                micursor.execute("SELECT * FROM cliente WHERE APELLIDO = ?",seleccion)
                resultado=micursor.fetchone()
                return resultado
            elif op_cliente == 3:
                #telefono
                micursor.execute("SELECT * FROM cliente WHERE TELEFONO = ?",seleccion)
                resultado=micursor.fetchone()
                return resultado
            elif op_cliente == 4:
                #direccion
                micursor.execute("SELECT * FROM cliente WHERE DIRECCION = ?",seleccion)
                resultado=micursor.fetchone()
                return resultado
            elif op_cliente == 5:
                #deuda
                micursor.execute("SELECT * FROM cliente WHERE DEUDA = ?",seleccion)
                resultado=micursor.fetchone()
                return resultado
            elif op_cliente == 6:
                micursor.execute("SELECT * FROM cliente ORDER BY NOMBRE DESC")
                resultado=micursor.fetchall()
                return resultado
        elif tabla == 2:
            # tabla pedido
            if op_pedido == 0:
                # id_pedido
                micursor.execute("SELECT * FROM pedido WHERE ID_PEDIDO = ?",(seleccion, ))
                resultado=micursor.fetchone()
                return resultado
            elif op_pedido == 1:
                # ci_cliente
                micursor.execute("SELECT * FROM pedido WHERE CI_CLIENTE = ?",(str(seleccion),))
                resultado=micursor.fetchall()
                return resultado
            elif op_pedido == 2:
                # id_pedido
                micursor.execute("SELECT * FROM pedido WHERE ID_PRODUCTO = ?",seleccion)
                resultado=micursor.fetchone()
                return resultado
            elif op_pedido == 3:
                # cantidad_ped
                micursor.execute("SELECT * FROM pedido WHERE CANTIDAD_PEDIDO = ?",seleccion)
                resultado=micursor.fetchone()
                return resultado
            elif op_pedido == 4:
                # fecha
                micursor.execute("SELECT * FROM pedido WHERE FECHA = ?",(seleccion, ))
                resultado=micursor.fetchall()
                return resultado
            elif op_pedido == 5:
                micursor.execute("SELECT * FROM pedido ORDER BY FECHA DESC")
                resultado=micursor.fetchall()
                return resultado
    elif op_BD ==  1:
        #crear nuevo
        if tabla == 0:
            # productos
            micursor.execute("INSERT INTO producto VALUES(?, ?, ?, ?)",tu_clave)
            miconexion.commit()
        elif tabla == 1:
            # cliente
            micursor.execute("INSERT INTO cliente VALUES(?, ?, ?, ?, ?, ?)",tu_clave)
            miconexion.commit()
        elif tabla == 2:
            # pedido 
            micursor.execute("INSERT INTO pedido VALUES(NULL, ?, ?, ?, ?)",tu_clave)
            miconexion.commit()
    elif op_BD == 2:
        #actualizar
        if tabla == 0:
            # productos
            row0=tu_clave[0]
            row1=tu_clave[1]
            row2=tu_clave[2]
            row3=tu_clave[3]
            
            micursor.execute("UPDATE producto SET PRECIO_COSTO = ? , PRECIO_VENTA = ?, CANTIDAD_PRODUCTO = ? WHERE ID_PRODUCTO = ?",(row1,row2,row3,row0))
            miconexion.commit()
        elif tabla == 1:
            # cliente
            row0=tu_clave[0]
            row1=tu_clave[1]
            row2=tu_clave[2]
            row3=tu_clave[3]
            row4=tu_clave[4]
            row5=tu_clave[5]
            
            micursor.execute("UPDATE cliente SET NOMBRE = ?, APELLIDO = ?, TELEFONO = ?, DIRECCION = ?, DEUDA = ? WHERE CI_CLIENTE = ?",(row1,row2,row3,row4,row5,row0))
            miconexion.commit()
        elif tabla == 2:
            # pedido
            row0=tu_clave[0]
            row1=tu_clave[1]
            row2=tu_clave[2]
            row3=tu_clave[3]
            
            micursor.execute("UPDATE producto SET CI_CLIENTE = ? , ID_PRODUCTO = ?, CANTIDAD_PEDIDO = ?, FECHA = ? WHERE ID_PEDIDO = ?",(row1,row2,row3,row0))
            miconexion.commit() 

    elif op_BD == 3:
        #eliminar
        if tabla == 0:
            # productos
            if clean_total == 0:
                row0=tu_clave[0]
                micursor.execute("DELETE FROM producto WHERE ID_PRODUCTO = ?",(row0,))
                miconexion.commit()
            else:
                micursor.execute("DELETE FROM producto WHERE ID_PRODUCTO = ID_PRODUCTO")
                miconexion.commit()
        elif tabla == 1:
            # cliente
            if clean_total == 0:
                row0=tu_clave[0]
                micursor.execute("DELETE FROM cliente WHERE CI_CLIENTE = ?",(row0,))
                miconexion.commit()
            else:
                micursor.execute("DELETE FROM cliente WHERE CI_CLIENTE = CI_CLIENTE")
                miconexion.commit()
        elif tabla == 2:
            # pedido
            if clean_total == 0:
                row0=tu_clave[0]
                micursor.execute("DELETE FROM pedido WHERE ID_PEDIDO = ?",(row0,))
                miconexion.commit()
            else:
                micursor.execute("DELETE FROM pedido WHERE ID_PEDIDO = ID_PEDIDO")
                miconexion.commit()
    miconexion.close()

#Cierra la aplicacion
def salirApp():
    if messagebox.askyesno("ADVERTENCIA","¿Seguro desea salir de la aplicacion?"):
        wind.destroy()

#Relacion entre todas las funciones de borrar
def borrarTODO():
    if messagebox.askyesno("CUIDADO", "Se limpiaran toda de la BASE DE DATOS, ¿Desea continuar?"):
        clientes()
        windclientes.iconify()
        pedido()
        windpedido.iconify()
        wind.deiconify()
        borrarCLIENTES()
        borrarPEDIDO()
        borrarPRODUCTO()
        windclientes.destroy()
        windpedido.destroy()

#Busca dependiendo el radiobutton seleccionado
def buscar_pantallas():
    global windbuscar
    global tree1
    global tree3
    global lbuscar, linstruccion, v, ebuscar
    op_producto = 9
    op_cliente = 9
    op_pedido = 9
    if len(ebuscar.get()) != 0 and v.get() != 0:
        if v.get() == 1:
            op_BD = 0
            tabla = 0
            op_producto = 0
            seleccion = ebuscar.get()
            resultado = [base_datos(op_BD, tabla, tu_clave, seleccion, op_producto)]
            if resultado != [None]:
                view = tree.get_children() 
                for elementos in view:
                    tree.delete(elementos)
                for row in resultado:
                    tree.insert("", 0, text = "", values = (row[0], row[1], row[2], row[3]))
                wind.deiconify()
                windclientes.destroy()
                windpedido.destroy()
                windbuscar.destroy()
            else:
                messagebox.showerror("ERROR", "El PRODUCTO que busca no ha sido encontrado. Error: 001")

        elif v.get() == 2:
            op_BD = 0
            tabla = 1
            op_cliente = 0
            seleccion = ebuscar.get()
            resultado = [base_datos(op_BD, tabla, tu_clave, seleccion, op_producto, op_cliente)]
            if resultado != [None]:
                view = tree1.get_children() 
                for elementos in view:
                    tree1.delete(elementos)
                for row in resultado:
                    tree1.insert("", 0, text = "", values = (row[0], row[1], row[2], row[3], row[4], row[5]))
                windclientes.deiconify()
                windpedido.destroy()
                windbuscar.destroy()
            else:
                messagebox.showerror("ERROR", "El CLIENTE con la CEDULA que busca no ha sido encontrado. Error: 002")

        elif v.get() == 3:
            op_BD = 0
            tabla = 2
            op_pedido = 0
            seleccion = ebuscar.get()
            resultado = [base_datos(op_BD, tabla, tu_clave, seleccion, op_producto, op_cliente, op_pedido)]
            if resultado != [None]:
                view = tree3.get_children() 
                for elementos in view:
                    tree3.delete(elementos)
                for row in resultado:
                    tree3.insert("", 0, text = "", values = (row[0], row[1], row[2], row[3], row[4]))
                windpedido.deiconify()
                windclientes.destroy()
                windbuscar.destroy()
            else:
                messagebox.showerror("ERROR", "El PEDIDO con el ID que busca no ha sido encontrado. Error: 003")

        elif v.get() == 4:
            op_BD = 0
            tabla = 1
            op_cliente = 1
            seleccion = ebuscar.get()
            resultado = (base_datos(op_BD, tabla, tu_clave, seleccion, op_producto, op_cliente))
            existe = list(resultado)
            if len(existe) != 0:
                view = tree1.get_children() 
                for elementos in view:
                    tree1.delete(elementos)
                for row in resultado:
                    tree1.insert("", 0, text = "", values = (row[0], row[1], row[2], row[3], row[4], row[5]))
                windclientes.deiconify()
                windpedido.destroy()
                windbuscar.destroy()
            else:
                messagebox.showerror("ERROR", "El CLIENTE con el NOMBRE que busca no ha sido encontrado. Error: 004")

        elif v.get() == 5:
            op_BD = 0
            tabla = 1
            op_cliente = 1
            seleccion = ebuscar.get()
            resultado = (base_datos(op_BD, tabla, tu_clave, seleccion, op_producto, op_cliente))
            list_resultado = list(resultado)
            len_resultado = len(list_resultado)
            if len_resultado != 0:
                j = 0
                for i in range(len_resultado):
                    op_BD = 0
                    tabla = 2
                    op_pedido = 1
                    seleccion = resultado[j][0]
                    resultado1 = (base_datos(op_BD, tabla, tu_clave, seleccion, op_producto, op_cliente,op_pedido))
                    j += 1
                    if j == 1:
                        view = tree3.get_children()
                        for elementos in view:
                            tree3.delete(elementos)
                    for row in resultado1:
                        tree3.insert("", 0, text = "", values = (row[0], row[1], row[2], row[3], row[4]))
                windpedido.deiconify()
                windclientes.destroy()
                windbuscar.destroy()
            else:
                messagebox.showerror("ERROR", "El CLIENTE con el NOMBRE que busca no ha sido encontrado. Error: 005")

        elif v.get() == 6:
            op_BD = 0
            tabla = 2
            op_pedido = 4
            seleccion = ebuscar.get()
            resultado = (base_datos(op_BD, tabla, tu_clave, seleccion, op_producto, op_cliente, op_pedido))
            existe=list(resultado)
            if len(existe) != 0:
                view = tree3.get_children() 
                for elementos in view:
                    tree3.delete(elementos)
                for row in resultado:
                    tree3.insert("", 0, text = "", values = (row[0], row[1], row[2], row[3], row[4]))
                windpedido.deiconify()
                windclientes.destroy()
                windbuscar.destroy()
            else:
                messagebox.showerror("ERROR", "El CLIENTE con el NOMBRE que busca no ha sido encontrado. Error: 006")
    else:
        messagebox.showerror("ERROR", "Debe colocar la opcion y la palabra clave a buscar. Error: 007")

#Cambia los label de buscar segun el,radiobutton seleccionado
def label_buscar():
    global lbuscar, linstruccion, v
    if v.get() == 1:
        lbuscar['text'] = "Ha seleccionado la opcion ID PRODUCTO"
        linstruccion['text'] = "Ingrese el ID del PRODUCTO que desea buscar"
        linstruccion.place(x = 198, y = 135)
    elif v.get() == 2:
        lbuscar['text'] = "Ha seleccionado la opcion CEDULA CLIENTE"
        linstruccion['text'] = "Ingrese la CI del CLIENTE que desea buscar"
        linstruccion.place(x = 210, y = 135)
    elif v.get() == 3:
        lbuscar['text'] = "Ha seleccionado la opcion NUMERO FACTURA"
        linstruccion['text'] = "Ingrese el NUMERO de la FACTURA que desea buscar"
        linstruccion.place(x = 175, y = 135)
    elif v.get() == 4:
        lbuscar['text'] = "Ha seleccionado la opcion NOMBRE CLIENTE"
        linstruccion['text'] = "Ingrese el NOMBRE del CLIENTE que desea buscar"
        linstruccion.place(x = 188, y = 135)
    elif v.get() == 5:
        lbuscar['text'] = "Ha seleccionado la opcion NOMBRE CLIENTE FACTURA"
        linstruccion['text'] = "Ingrese el NOMBRE del CLIENTE que desea buscar en PEDIDOS"
        linstruccion.place(x = 160, y = 135)
    elif v.get() == 6:
        lbuscar['text'] = "Ha seleccionado la opcion FECHA"
        linstruccion['text'] = "Ingrese la FECHA del PEDIDO que desea buscar\n   Formato: DD/MM/YYYY"
        linstruccion.place(x = 190, y = 135)

#Funciones para los btones para moverse entre ventanas de buscar
def abrir_principal():
    wind.deiconify()
    windclientes.destroy()
    windpedido.destroy()
    windbuscar.destroy()

def abrir_pedido():
    windpedido.deiconify()
    windclientes.destroy()
    windbuscar.destroy()

def abrir_cliente():
    windclientes.deiconify()
    windpedido.destroy()
    windbuscar.destroy()

def abono_buscar():
    windclientes.destroy()
    windpedido.destroy()
    windbuscar.destroy()
    abono_deuda()

#Ventana de buscar
def buscar():
    global windbuscar
    global lbuscar, linstruccion, v, ebuscar
    global rb_producto, rb_cliente, rb_pedido, rb_nombre, rb_fecha
    windbuscar = Toplevel()
    windbuscar.resizable(width = 0, height = 0)
    windbuscar.geometry("500x250")
    windbuscar.iconbitmap('archivo.ico')

    windbuscar.title("Aplicacion de Inventario (BUSCAR)")
    lbuscar = Label(windbuscar, text = "Selecciones lo que desea buscar")
    lbuscar.place(x = 10, y = 10)

    ebuscar = Entry(windbuscar, width = 30)
    ebuscar.place(x = 230, y = 65)

    bbuscar = ttk.Button(windbuscar, text = "Buscar", width = 29, command = lambda: buscar_pantallas())
    bbuscar.place(x = 230, y = 100)

    nombre_image = resolver_ruta('principal.png')
    img1 = PhotoImage(file = nombre_image)
    babrir_principal = Button(windbuscar, width = 35, height = 35, command = lambda: abrir_principal())
    babrir_principal.image_names = img1
    babrir_principal.config(image = img1)
    babrir_principal.place(x = 260, y = 185)
    Hovertip(babrir_principal, text = "Pantalla Principal", hover_delay = 100)

    nombre_image = resolver_ruta('pedidos.png')
    img2 = PhotoImage(file = nombre_image)
    babrir_pedido = Button(windbuscar, width = 35, height = 35, command = lambda: abrir_pedido())
    babrir_pedido.image_names = img2
    babrir_pedido.configure(image = img2)
    babrir_pedido.place(x = 370, y = 185)
    Hovertip(babrir_pedido, text = "Pedidos", hover_delay = 100)

    nombre_image = resolver_ruta('cliente.png')
    img3 = PhotoImage(file = nombre_image)
    babrir_cliente = Button(windbuscar, width = 35, height = 35, command = lambda: abrir_cliente())
    babrir_cliente.image_names = img3
    babrir_cliente.configure(image = img3)
    babrir_cliente.place(x = 315, y = 185)
    Hovertip(babrir_cliente, text = "Clientes", hover_delay = 100)

    "Agrege el boton de abono deuda"
    nombre_image = resolver_ruta('abono_deuda.png')
    img4 = PhotoImage(file = nombre_image)
    babono_deuda = Button(windbuscar, width = 35, height = 35, command = lambda: abono_buscar())
    babono_deuda.image_names = img4
    babono_deuda.configure(image = img4)
    babono_deuda.place(x = 425, y = 185)
    Hovertip(babono_deuda, text = "Abono Deuda", hover_delay = 100)

    linstruccion = Label(windbuscar, text = "")
    linstruccion.place(x = 160, y = 135)

    v = IntVar()
    rb_producto = Radiobutton(windbuscar, text = "ID PRODUCTO", value = 1, variable = v, command = lambda: label_buscar())
    rb_producto.place(x = 20, y = 50)
    rb_cliente = Radiobutton(windbuscar, text = "CEDULA CLIENTE", value = 2, variable = v, command = lambda: label_buscar())
    rb_cliente.place(x = 20, y = 80)
    rb_pedido = Radiobutton(windbuscar, text = "NUMERO FACTURA", value = 3, variable = v, command = lambda: label_buscar())
    rb_pedido.place(x = 20, y = 110)
    rb_nombre = Radiobutton(windbuscar, text = "NOMBRE CLIENTE", value = 4, variable = v, command = lambda: label_buscar())
    rb_nombre.place(x = 20, y = 140)
    rb_nombre = Radiobutton(windbuscar, text = "NOMBRE CLIENTE FACTURA", value = 5, variable = v, command = lambda: label_buscar())
    rb_nombre.place(x = 20, y = 170)
    rb_fecha = Radiobutton(windbuscar, text = "FECHA", value = 6, variable = v, command = lambda: label_buscar())
    rb_fecha.place(x = 20, y = 200)

    clientes()
    windclientes.iconify()
    pedido()
    windpedido.iconify()
    wind.iconify()

#Vacia la tabla clientes
def borrarCLIENTES():
    op_BD = 3
    tabla = 1
    clean_total = 1
    base_datos(op_BD, tabla, tu_clave, seleccion, op_producto, op_cliente, op_pedido, clean_total)
    clean1()
    obt_clientes()

#Valida que los campos de cliente no esten vacios 
def validacion1():
    global ci_cliente, nombre, apellido, telefono, direccion, deuda
    return len(ci_cliente.get()) != 0 and len(nombre.get()) != 0 and len(apellido.get()) != 0 and len(telefono.get()) != 0 and len(direccion.get()) != 0 and len(deuda.get()) != 0

#Rellena el treview de clientes
def obt_clientes():
    global tree1
    view = tree1.get_children()
    for elementos in view:
        tree1.delete(elementos)
    op_BD=0
    tabla=1
    op_cliente=6
    resultado=(base_datos(op_BD,tabla,tu_clave,seleccion,op_producto,op_cliente))
        
    for row in resultado:
        tree1.insert("", 0, text = "", values = (row[0], row[1], row[2], row[3], row[4], row[5]))

#Actualiza el treview de clientes
def actualizar_tabla2():
    global b_guardar, b_actualizar, b_eliminar, ci_cliente
    obt_clientes()
    b_guardar["state"] = "normal"
    b_actualizar["state"] = "disable"
    b_eliminar["state"] = "disable"
    ci_cliente["state"] = "normal"
    clean1()
    Hovertip(ci_cliente, text = "", hover_delay = 360000)

#Añade un cliente
def agregar_cliente():
    global ci_cliente, nombre, apellido, telefono, direccion, deuda
    if validacion1():
        tu_clave = []
        op_BD=0
        tabla=1
        op_cliente = 6
        resultado1 = (base_datos(op_BD, tabla, tu_clave, seleccion, op_producto, op_cliente))
        len_resultado = len(resultado1)
        j = 0
        aux = 0
        for i in range(len_resultado):
            if ci_cliente.get() != resultado1[j][0]:
                aux += 1            
        if aux == len_resultado:
            if ci_cliente.get()[0] == 'V' or ci_cliente.get()[0] == 'E' or ci_cliente.get()[0] == 'J':
                if ci_cliente.get()[1] == '-':
                    if ci_cliente.get()[2:11].isdigit() and nombre.get().isalpha() and apellido.get().isalpha() and deuda.get().isdigit():
                        if len(ci_cliente.get()) <= 11 and len(ci_cliente.get()) > 3 and len(nombre.get()) < 20 and len(apellido.get()) < 20 and len(telefono.get()) <= 15 and len(direccion.get()) < 50:
                            if telefono.get()[0] == '+' and telefono.get()[1:14].isdigit() or telefono.get()[0:14].isdigit(): 
                                tu_clave.append(ci_cliente.get())
                                tu_clave.append(nombre.get())
                                tu_clave.append(apellido.get())
                                tu_clave.append(telefono.get())
                                tu_clave.append(direccion.get())
                                tu_clave.append(deuda.get())
                                op_BD=1
                                tabla=1
                                base_datos(op_BD,tabla,tu_clave)
                                messagebox.showinfo("BASE DE DATOS", "Se guardaron correctamente los campos")
                                clean1()
                            else:
                                messagebox.showerror("ERROR", "La TELEFONO puede comenzar con un numero o un +. Error: 008")
                        else:
                            messagebox.showerror("ERROR", "La CEDULA debe tener entre 3 y 10 numeros, el NOMBRE y el APELLIDO 20 caracteres, el TELEFONO maximo 15 y la DIRECCION maximo 50. Error: 009")     
                    else:
                        messagebox.showerror("ERROR", "La CEDULA debe comenzar con V, E o J y continuar con numeros, la DEUDA debe ser numerica, y los demas campos textos. Error: 010")
                else:
                    messagebox.showerror("ERROR", "Debe colocar un guion (-) despues de V, E o J. Error: 011")
            else:
                messagebox.showerror("ERROR", "La CEDULA debe comenzar con V, E o J mayuscula. Error: 012")
        else:
            messagebox.showerror("ERROR", "La CEDULA del CLIENTE ya existe no puede volver agregarla. Error: 013")
    else:
        messagebox.showerror("ERROR", "No puede haber campos en blanco. Error: 014")
    obt_clientes()

#Edita un cliente
def editar_cliente():
    global ci_cliente, nombre, apellido, telefono, direccion, deuda
    tu_clave=[]
    if validacion1():
        try:
            float(deuda.get())
            if nombre.get().isalpha() and apellido.get().isalpha():
                if len(nombre.get()) < 20 and len(apellido.get()) < 20 and len(telefono.get()) <= 15 and len(direccion.get()) < 50:
                    if telefono.get()[0] == '+' and telefono.get()[1:14].isdigit() or telefono.get()[0:14].isdigit():
                        tu_clave.append(ci_cliente.get())
                        tu_clave.append(nombre.get())
                        tu_clave.append(apellido.get())
                        tu_clave.append(telefono.get())
                        tu_clave.append(direccion.get())
                        tu_clave.append(deuda.get())
                        op_BD=2
                        tabla=1
                        base_datos(op_BD,tabla,tu_clave)
                        messagebox.showinfo("BASE DE DATOS", "Se actualizaron correctamente los campos")
                        ci_cliente.configure(state = 'normal')
                        clean1()
                        b_guardar["state"] = "normal"
                        b_actualizar["state"] = "disable"
                        b_eliminar["state"] = "disable"
                    else:
                        messagebox.showerror("ERROR", "La TELEFONO puede comenzar con un numero o un +. Error: 015")
                else:
                    messagebox.showerror("ERROR", "El NOMBRE y el APELLIDO 20 caracteres, el TELEFONO maximo 15 y la DIRECCION maximo 50. Error: 016")
            else:
                messagebox.showerror("ERROR", "La DEUDA debe ser numerica, y los demas campos textos. Error: 017")
        except:
            messagebox.showerror("ERROR", "La DEUDA debe ser numerica, y los demas campos textos. Error: 018")
    else:
        messagebox.showerror("ERROR", "No pueden haber campos en blanco. Error: 019")
    obt_clientes()
    Hovertip(ci_cliente, text = "", hover_delay = 360000)

#Elimina un cliente
def eliminar_cliente():
    global ci_cliente, b_guardar, b_actualizar, b_eliminar
    tu_clave=[]
    if len(ci_cliente.get()) != 0:
        tu_clave.append(ci_cliente.get())
        op_BD=3
        tabla=1
        base_datos(op_BD,tabla,tu_clave)
        messagebox.showinfo("BASE DE DATOS", "Se eliminaron correctamente los campos")
    else:
        messagebox.showerror("ERROR", "El campo CI CLIENTE no puede estar vacio. Error: 020")
    ci_cliente.configure(state = 'normal')
    clean1()
    obt_clientes()
    b_guardar["state"] = "normal"
    b_actualizar["state"] = "disable"
    b_eliminar["state"] = "disable"
    Hovertip(ci_cliente, text = "", hover_delay = 360000)

#Resetea los campos de cliente
def clean1():
    global ci_cliente, nombre, apellido, telefono, direccion, deuda
    ci_cliente.delete(0, END)
    nombre.delete(0, END)
    apellido.delete(0, END)
    telefono.delete(0, END)
    direccion.delete(0, END)
    deuda.delete(0, END)

#Seleccionar haciendo doble click en cliente
def seleccionar1_click(event):
    global tree1, ci_cliente, nombre, apellido, telefono, direccion, deuda, b_guardar, b_actualizar, b_eliminar
    try:
        clean1()
        selected = tree1.focus()
        values = tree1.item(selected, 'values')
        ci_cliente.insert(0, values[0])
        nombre.insert(0, values[1])
        apellido.insert(0, values[2])
        telefono.insert(0, values[3])
        direccion.insert(0, values[4])
        deuda.insert(0, values[5])
        ci_cliente.configure(state = 'disable')
        b_guardar["state"] = "disable"
        b_actualizar["state"] = "normal"
        b_eliminar["state"] = "normal"
        Hovertip(ci_cliente, text = "No puede actualizar la cedula de un usuario existente", hover_delay = 100)
    except:
        messagebox.showerror("ERROR", "Debe hacer doble click sobre un cliente. Error: 021")

#Funciones de los botones para navegar entre las ventanas de cliente
def buscar_cliente():
    global windclientes
    windclientes.destroy()
    buscar()

def principal_cliente():
    global windclientes
    windclientes.destroy()
    wind.deiconify()

def pedido_cliente():
    global windclientes
    windclientes.destroy()
    pedido()

def abono_clientes():
    global windclientes
    windclientes.destroy()
    abono_pedido()

#Ventana clientes
def clientes():
    global windclientes
    wind.iconify()
    windclientes = Toplevel()
    windclientes.resizable(width=0,height=0)
    windclientes.geometry("900x570")
    windclientes.iconbitmap('archivo.ico')
    windclientes.title("Aplicacion de Inventario (CLIENTES)")

    global tree1, ci_cliente, nombre, apellido, telefono, direccion, deuda
    global b_guardar, b_eliminar, b_actualizar, bpsearch, bprin_cliente, bpedido1, bactualizar_cliente
    tree1 = ttk.Treeview(windclientes)
    tree1['columns'] = ("CI_CLIENTE", "NONMBRE", "APELLIDO", "TELEFONO","DIRECCION", "DEUDA")
    tree1.place(x = 0, y = 270)
    tree1.column('#0', width = 0, stretch = NO)
    tree1.column('#1', minwidth = 150, width=150,  anchor = CENTER)
    tree1.column('#2', minwidth = 150, width=150, anchor = CENTER)
    tree1.column('#3', minwidth = 150, width=150, anchor = CENTER)
    tree1.column('#4', minwidth = 150, width=150, anchor = CENTER)
    tree1.column('#5', minwidth = 150, width=150, anchor = CENTER)
    tree1.column('#6', minwidth = 150, width=150, anchor = CENTER)
    tree1.heading('#1', text = 'CEDULA', anchor = CENTER)
    tree1.heading('#2', text = 'NOMBRE', anchor = CENTER)
    tree1.heading('#3', text = 'APELLIDO', anchor = CENTER)
    tree1.heading('#4', text = 'TELEFONO', anchor = CENTER)
    tree1.heading('#5', text = 'DIRECCION', anchor = CENTER)
    tree1.heading('#6', text = 'DEUDA', anchor = CENTER)
    tree1.bind("<Double-Button-1>", seleccionar1_click)
    obt_clientes()

    l_title = Label(windclientes, text = "Agregue un cliente")
    l_title.place(x = 400, y = 10)

    l_ci_cedula = Label(windclientes, text = "Cedula Cliente:")
    l_ci_cedula.place(x = 290, y = 40)
    l_formato = Label(windclientes, text = "Formato: V-00000000")
    l_formato.place(x = 650, y = 40)
    ci_cliente = Entry(windclientes, width = 40)
    ci_cliente.focus()
    ci_cliente.place(x = 390, y = 40)

    l_nombre = Label(windclientes, text = "Nombre Cliente:")
    l_nombre.place(x = 282, y = 70)
    nombre = Entry(windclientes, width = 40)
    nombre.place(x = 390, y = 70)

    l_apellido = Label(windclientes, text = "Apellido Cliente:")
    l_apellido.place(x = 282, y = 100)
    apellido = Entry(windclientes, width = 40)
    apellido.place(x = 390, y = 100)

    l_telefono = Label(windclientes, text = "Telefono Cliente:")
    l_telefono.place(x = 280, y = 130)
    telefono = Entry(windclientes, width = 40)
    telefono.place(x = 390, y = 130)

    l_direccion = Label(windclientes, text = "Direccion Cliente:")
    l_direccion.place(x = 276, y = 160)
    direccion = Entry(windclientes, width = 40)
    direccion.place(x = 390, y = 160)

    l_deuda = Label(windclientes, text = "Deuda Cliente:")
    l_deuda.place(x = 291, y = 190)
    deuda = Entry(windclientes, width = 40)
    deuda.place(x = 390, y = 190)

    b_guardar = ttk.Button(windclientes, text = "Guardar cliente", width = 70, command = lambda: agregar_cliente())
    b_guardar.place(x = 205, y = 225)

    b_eliminar = ttk.Button(windclientes, text = "Eliminar cliente", width = 70, command = lambda: eliminar_cliente())
    b_eliminar.place(x = 435, y = 510)
    b_eliminar['state'] = 'disable'

    b_actualizar = ttk.Button(windclientes, text = "Actualizar cliente", width = 70, command = lambda: editar_cliente())
    b_actualizar.place(x = 30, y = 510)
    b_actualizar['state'] = 'disable'

    nombre_image = resolver_ruta('buscar.png')
    img1 = PhotoImage(file = nombre_image)
    bpsearch = Button(windclientes, width = 35, height = 35, command = lambda: buscar_cliente())
    bpsearch.image_names = img1
    bpsearch.config(image = img1)
    bpsearch.place(x = 15, y = 15)
    Hovertip(bsearch, text = "Buscar")
    Hovertip(bpsearch, text = "buscar", hover_delay = 100)

    nombre_image = resolver_ruta('principal.png')
    img2 = PhotoImage(file = nombre_image)
    bprin_cliente = Button(windclientes, width = 35, height = 35, command = lambda: principal_cliente())
    bprin_cliente.image_names = img2
    bprin_cliente.config(image = img2)
    bprin_cliente.place(x = 15, y = 65)
    Hovertip(bprin_cliente, text = "Pantalla Principal", hover_delay = 100)

    "Agrege el boton de pedido"
    nombre_image = resolver_ruta('pedidos.png')
    img3 = PhotoImage(file = nombre_image)
    bpedido1 = Button(windclientes, width = 35, height = 35, command = lambda: pedido_cliente())
    bpedido1.image_names = img3
    bpedido1.configure(image = img3)
    bpedido1.place(x = 15, y = 115)
    Hovertip(bpedido1, text = "Pedidos", hover_delay = 100)

    "Acabo de agregar el boton actualizar"
    nombre_image = resolver_ruta('actualizar_tree.png')
    img4 = PhotoImage(file = nombre_image)
    bactualizar_cliente = Button(windclientes, image = img4, width = 18, height = 18, command = lambda: actualizar_tabla2())
    bactualizar_cliente.place(x = 640, y = 225)
    bactualizar_cliente.image_names = img4
    bactualizar_cliente.config(image = img4)
    Hovertip(bactualizar_cliente, text = "Actualizar Lista", hover_delay = 100)

    "Agrege el boton de abono deuda"
    nombre_image = resolver_ruta('abono_deuda.png')
    img5 = PhotoImage(file = nombre_image)
    babono_deuda = Button(windclientes, width = 35, height = 35, command = lambda: abono_clientes())
    babono_deuda.image_names = img5
    babono_deuda.configure(image = img5)
    babono_deuda.place(x = 15, y = 165)
    Hovertip(babono_deuda, text = "Abono Deuda", hover_delay = 100)

    menuvar = Menu(windclientes)
    menuDB = Menu(menuvar, tearoff = 0)
    menuDB.add_command(label = "Limpiar Base De Datos", command = lambda: borrarTODO())
    menuDB.add_command(label = "Salir", command = lambda : salirApp())
    menuvar.add_cascade(label = "Inicio", menu = menuDB)

    ayudamenu = Menu(menuvar, tearoff = 0)
    ayudamenu.add_command(label = "Resetear Campos", command = lambda: clean1())
    ayudamenu.add_command(label = "Manual de Usuario", command = lambda: manual())
    menuvar.add_cascade(label = "Ayuda", menu = ayudamenu)

    windclientes.config(menu = menuvar)

#Vacia la tabla pedido
def borrarPEDIDO():
    op_BD = 3
    tabla = 2
    clean_total = 1
    base_datos(op_BD, tabla, tu_clave, seleccion, op_producto, op_cliente, op_pedido, clean_total)
    clean_pedido()
    obt_pedidos()

#Valida que los campos de pedido no esten vacios
def validacion_pedido():
    global tree3, enumero_factura, ecant, eci, eid_pro
    return len(eci.get()) != 0 and len(eid_pro.get()) != 0 and len(ecant.get()) != 0

#Rellena el treview de pedidos
def obt_pedidos():
    global tree3, enumero_factura, ecant, eci, eid_pro
    view = tree3.get_children()
    for elementos in view:
        tree3.delete(elementos)
    op_BD = 0
    tabla = 2
    op_pedido = 5
    resultado = (base_datos(op_BD, tabla, tu_clave, seleccion, op_producto, op_cliente, op_pedido))
    for row in resultado:
        tree3.insert("", 0, text = "", values = (row[0], row[1], row[2], row[3], row[4]))

#Actualiza el treview de pedidos
def actualizar_tabla1():
    global bgpedido, bepedido, bpsearch, bprin_pedido, bpedido, bactualizar_pedido
    obt_pedidos()
    eci.configure(state = 'normal')
    eid_pro.configure(state = 'normal')
    ecant.configure(state = 'normal')
    bgpedido["state"] = "normal"
    bepedido["state"] = "disable"
    enumero_factura.configure(state = 'normal')
    clean_pedido()
    enumero_factura.configure(state = 'disable')
    Hovertip(eci, text = "", hover_delay = 360000)
    Hovertip(eid_pro, text = "", hover_delay = 360000)
    Hovertip(ecant, text = "", hover_delay = 360000)

#Añade un pedido
def agregar_pedido():
    global tree3, enumero_factura, ecant, eci, eid_pro
    if validacion_pedido():
        tu_clave = []
        seleccion = eid_pro.get()
        op_BD=0
        tabla=0
        op_producto = 0
        resultado1 = (base_datos(op_BD, tabla, tu_clave, seleccion, op_producto))
        seleccion = eci.get()
        op_BD=0
        tabla=1
        op_cliente = 0
        resultado = (base_datos(op_BD, tabla, tu_clave, seleccion, op_producto, op_cliente))
        if resultado == None:
            if messagebox.askyesno("ADVERTENCIA", "El cliente con la CI que ingreso no existe, ¿Desea agregarlo?"):
                windpedido.destroy()
                clientes()
            return
        if resultado1 == None:
            if messagebox.askyesno("ADVERTENCIA", "El producto con el ID que ingreso no existe, ¿Desea agregarlo?"):
                windpedido.destroy()
                wind.deiconify()
            return
        try:
            int(ecant.get())
            if int(ecant.get()) <= int(resultado1[3]):
                disminuir_inventario = int(resultado1[3]) - int(ecant.get())
                tu_clave = []
                tu_clave.append(resultado1[0])
                tu_clave.append(resultado1[1])
                tu_clave.append(resultado1[2])
                tu_clave.append(disminuir_inventario)
                op_BD = 2
                tabla = 0
                seleccion = eid_pro.get()
                base_datos(op_BD, tabla, tu_clave, seleccion)
                sumar_deuda = (int(ecant.get()) * float(resultado1[2])) + resultado[5]
                tu_clave = []
                tu_clave.append(resultado[0])
                tu_clave.append(resultado[1])
                tu_clave.append(resultado[2])
                tu_clave.append(resultado[3])
                tu_clave.append(resultado[4])
                tu_clave.append(resultado[5])
                tu_clave.remove(resultado[5])
                tu_clave.append(sumar_deuda)
                op_BD=2
                tabla=1
                base_datos(op_BD, tabla, tu_clave)
                tu_clave = []
                tu_clave.append(eci.get())
                tu_clave.append(eid_pro.get())
                tu_clave.append(ecant.get())
                tu_clave.append(str_now)
                op_BD = 1
                tabla = 2
                base_datos(op_BD, tabla, tu_clave)
                messagebox.showinfo("BASE DE DATOS", "Se guardo correctamente el pedido y se actualizaron los campos inventario y deuda")
            else:
                messagebox.showerror("ERROR", "No pueden haber pedidos que la Cantidad Pedido exceda la Cantidad disponible en el inventario. Error: 022")
        except:
            messagebox.showerror("ERROR", "El CANTIDAD PEDIDO debe ser un numero entero. Error: 023")
    else:
        messagebox.showerror("ERROR", "No pueden haber campos en blanco. Error: 024")
    obt_pedidos()
    obt_productos()
    clean_pedido()

#Elimina un pedido
def eliminar_pedido():
    global tree3, enumero_factura, ecant, eci, eid_pro
    enumero_factura.configure(state = 'normal')
    tu_clave = []
    seleccion = eid_pro.get()
    op_BD=0
    tabla=0
    op_producto = 0
    resultado1 = (base_datos(op_BD, tabla, tu_clave, seleccion, op_producto))
    tu_clave = []
    op_producto = 9
    seleccion = eci.get()
    op_BD=0
    tabla=1
    op_cliente = 0
    resultado = (base_datos(op_BD, tabla, tu_clave, seleccion, op_producto, op_cliente))
    if validacion_pedido():
        disminuir_inventario = int(resultado1[3]) + int(ecant.get())
        tu_clave = []
        tu_clave.append(resultado1[0])
        tu_clave.append(resultado1[1])
        tu_clave.append(resultado1[2])
        tu_clave.append(disminuir_inventario)
        op_BD = 2
        tabla = 0
        seleccion = eid_pro.get()
        base_datos(op_BD, tabla, tu_clave, seleccion)
        if (int(ecant.get()) * float(resultado1[2])) <= resultado[5]:
            sumar_deuda = resultado[5] - (int(ecant.get()) * float(resultado1[2]))
            tu_clave = []
            tu_clave.append(resultado[0])
            tu_clave.append(resultado[1])
            tu_clave.append(resultado[2])
            tu_clave.append(resultado[3])
            tu_clave.append(resultado[4])
            tu_clave.append(resultado[5])
            tu_clave.remove(resultado[5])
            tu_clave.append(sumar_deuda)
            op_BD=2
            tabla=1
            base_datos(op_BD, tabla, tu_clave)
        else:
            messagebox.showerror("ERROR", "Hubo un error al eliminar datos datos. Error: 025")
            return
        tu_clave = []
        tu_clave.append(enumero_factura.get())
        op_BD = 3
        tabla = 2
        base_datos(op_BD, tabla, tu_clave)
        messagebox.showinfo("BASE DE DATOS", "Se elimino correctamente el pedido y se actualizaron los campos inventario y deuda")
    else:
        messagebox.showerror("ERROR", "No pueden haber campos en blanco. Error: 026")
    eci.configure(state = 'normal')
    eid_pro.configure(state = 'normal')
    ecant.configure(state = 'normal')
    bgpedido["state"] = "normal"
    bepedido["state"] = "disable"
    obt_pedidos()
    obt_productos()
    clean_pedido()
    enumero_factura.configure(state = 'disable')
    Hovertip(eci, text = "", hover_delay = 360000)
    Hovertip(eid_pro, text = "", hover_delay = 360000)
    Hovertip(ecant, text = "", hover_delay = 360000)

#Limpia los campos de pedido
def clean_pedido():
    global tree3, enumero_factura, ecant, eci, eid_pro
    eci.delete(0, END)
    eid_pro.delete(0, END)
    ecant.delete(0, END)
    enumero_factura.delete(0, END)

#Seleccionar al hacer doble click en pedido
def seleccionar_click2(event):
    global tree3, enumero_factura, ecant, eci, eid_pro
    global bgpedido, bepedido, bpsearch, bprin_pedido, bpedido, bactualizar_pedido
    try:
        clean()
        enumero_factura.configure(state = 'normal')
        selected = tree3.focus()
        values = tree3.item(selected, 'values')
        enumero_factura.insert(0, values[0])
        eci.insert(0, values[1])
        eid_pro.insert(0, values[2])
        ecant.insert(0, values[3])
        bgpedido["state"] = "disable"
        bepedido["state"] = "normal"
        eci.configure(state = 'disable')
        eid_pro.configure(state = 'disable')
        ecant.configure(state = 'disable')
        Hovertip(eci, text = "No puede actualizar los pedidos ya ingresados", hover_delay = 100)
        Hovertip(eid_pro, text = "No puede actualizar los pedidos ya ingresados", hover_delay = 100)
        Hovertip(ecant, text = "No puede actualizar los pedidos ya ingresados", hover_delay = 100)
        enumero_factura.configure(state = 'disable')
    except:
        enumero_factura.configure(state = 'disable')
        messagebox.showerror("ERROR", "Debe hacer doble click sobre un pedido. Error: 027")

#Funciones de los botones para moverse entre ventanas de pedido
def cliente_pedido():
    global windpedido
    windpedido.destroy()
    clientes()

def buscar_pedido():
    global windpedido
    windpedido.destroy()
    buscar()

def principal_pedido():
    global windpedido
    windpedido.destroy()
    wind.deiconify()

def abono_pedido():
    global windpedido
    windpedido.destroy()
    abono_deuda()

#Ventana pedido
def pedido():
    global windpedido
    wind.iconify()
    windpedido = Toplevel()
    windpedido.resizable(width = 0, height = 0)
    windpedido.geometry("1000x520")
    windpedido.iconbitmap('archivo.ico')
    windpedido.title("Aplicacion de Inventario (PEDIDOS)")

    global tree3, enumero_factura, ecant, eci, eid_pro
    global bgpedido, bepedido, bpsearch, bprin_pedido, bpedido, bactualizar_pedido
    tree3 = ttk.Treeview(windpedido)
    tree3['columns'] = ("N_FACTURA", "CI_CLIENTE", "ID_PRODUCTO", "CANTIDAD_PRODUCTO", "FECHA")
    tree3.place(x = 0, y = 220)
    tree3.bind("<Double-Button-1>", seleccionar_click2)
    tree3.column('#0', width = 0, stretch = NO)
    tree3.column('#1', minwidth = 200, anchor = CENTER)
    tree3.column('#2', minwidth = 200, anchor = CENTER)
    tree3.column('#3', minwidth = 200, anchor = CENTER)
    tree3.column('#4', minwidth = 200, anchor = CENTER)
    tree3.column('#5', minwidth = 200, anchor = CENTER)
    tree3.heading('#1', text = 'NUMERO FACTURA', anchor = CENTER)
    tree3.heading('#2', text = 'CI CLIENTE', anchor = CENTER)
    tree3.heading('#3', text = 'ID PRODUCTO', anchor = CENTER)
    tree3.heading('#4', text = 'CANTIDAD PRODUCTO', anchor = CENTER)
    tree3.heading('#5', text = 'FECHA', anchor = CENTER)
    obt_pedidos()

    l2 = Label(windpedido, text = "Ingrese un pedido")
    l2.place(x = 445, y = 5)

    lnumero_factura = Label(windpedido, text = "Numero Factura: ")
    lnumero_factura.place(x = 383, y = 35)
    enumero_factura = Entry(windpedido, width = 30)
    enumero_factura.place(x = 500, y = 35)
    enumero_factura.configure(state = 'disable')

    lci = Label(windpedido, text = "CI Cliente: ")
    lci.place(x = 416, y = 65)
    l_formato_pedido = Label(windpedido, text = "Formato: V-00000000")
    l_formato_pedido.place(x = 700, y = 65)
    eci = Entry(windpedido, width = 30)
    eci.focus()
    eci.place(x = 500, y = 65)

    lid_pro = Label(windpedido, text = "ID Producto: ")
    lid_pro.place(x = 404, y = 95)
    eid_pro = Entry(windpedido, width = 30)
    eid_pro.place(x = 500, y = 95)

    lcant = Label(windpedido, text = "Cantidad Producto: ")
    lcant.place(x = 367, y = 125)
    ecant = Entry(windpedido, width = 30)
    ecant.place(x = 500, y = 125)

    bgpedido = ttk.Button(windpedido, text = "Guardar Pedido", width = 60, command =  lambda: agregar_pedido())
    bgpedido.place(x = 315, y = 160)

    bepedido = ttk.Button(windpedido, text = "Eliminar Pedido", width = 60, command = lambda: eliminar_pedido())
    bepedido.place(x = 315, y = 460)
    bepedido['state'] = 'disable'

    nombre_image = resolver_ruta('buscar.png')
    img1 = PhotoImage(file = nombre_image)
    bpsearch = Button(windpedido, width = 35, height = 35, command = lambda: buscar_pedido())
    bpsearch.image_names = img1
    bpsearch.config(image = img1)
    bpsearch.place(x = 15, y = 15)
    Hovertip(bpsearch, text = "buscar", hover_delay = 100)

    nombre_image = resolver_ruta('principal.png')
    img2 = PhotoImage(file = nombre_image)
    bprin_pedido = Button(windpedido, width = 35, height = 35, command = lambda: principal_pedido())
    bprin_pedido.image_names = img2
    bprin_pedido.config(image = img2)
    bprin_pedido.place(x = 15, y = 65)
    Hovertip(bprin_pedido, text = "Pantalla Principal", hover_delay = 100)

    nombre_image = resolver_ruta('cliente.png')
    img3 = PhotoImage(file = nombre_image)
    bpedido = Button(windpedido, width = 35, height = 35, command = lambda: cliente_pedido())
    bpedido.image_names = img3
    bpedido.configure(image = img3)
    bpedido.place(x = 15, y = 115)
    Hovertip(bpedido, text = "Clientes", hover_delay = 100)

    "Agrege el boton de abono deuda"
    nombre_image = resolver_ruta('abono_deuda.png')
    img4 = PhotoImage(file = nombre_image)
    babono_deuda = Button(windpedido, width = 35, height = 35, command = lambda: abono_pedido())
    babono_deuda.image_names = img4
    babono_deuda.configure(image = img4)
    babono_deuda.place(x = 15, y = 165)
    Hovertip(babono_deuda, text = "Abono Deuda", hover_delay = 100)

    "Acabo de agregar el boton actualizar"
    nombre_image = resolver_ruta('actualizar_tree.png')
    img5 = PhotoImage(file = nombre_image)
    bactualizar_pedido = Button(windpedido, width = 18, height = 18, command = lambda: actualizar_tabla1())
    bactualizar_pedido.place(x = 690, y = 160)
    bactualizar_pedido.image_names = img5
    bactualizar_pedido.config(image = img5)
    Hovertip(bactualizar_pedido, text = "Actualizar Lista", hover_delay = 100)

    menuvar = Menu(windpedido)
    menuDB = Menu(menuvar, tearoff = 0)
    menuDB.add_command(label = "Limpiar Base De Datos", command = lambda: borrarTODO())
    menuDB.add_command(label = "Salir", command = lambda : salirApp())
    menuvar.add_cascade(label = "Inicio", menu = menuDB)

    ayudamenu = Menu(menuvar, tearoff = 0)
    ayudamenu.add_command(label = "Resetear Campos", command = lambda: clean_pedido())
    ayudamenu.add_command(label = "Manual de Usuario", command = lambda: manual())
    menuvar.add_cascade(label = "Ayuda", menu = ayudamenu)
    
    windpedido.config(menu = menuvar)

#Resta la deuda en la pantalla abono deuda
def resta_deuda():
    global windabono_deuda, windclientes
    global eabono_deuda, eci_abono

    if len(eabono_deuda.get()) != 0 and len(eci_abono.get()) != 0:
        try:
            abono = float(eabono_deuda.get())
            if float(eabono_deuda.get()) > 0:
                tu_clave = []
                op_BD=0
                tabla=1
                op_cliente = 0
                seleccion = eci_abono.get()
                resultado = (base_datos(op_BD,tabla,tu_clave,seleccion,op_producto,op_cliente))
                if resultado != NONE:
                    if (resultado[5] - abono) >= 0:
                        resta = list(resultado)
                        resta[5] = resta[5] - abono
                        op_BD = 2
                        tabla = 1
                        tu_clave = resta
                        base_datos(op_BD,tabla,tu_clave)
                        if resta[5] == 0:
                            messagebox.showinfo("BASE DE DATOS", "La deuda de " + resultado[1] + " " + resultado[2] + " quedo en CERO")
                        else:
                            messagebox.showinfo("BASE DE DATOS", "Se disminuyo correctamente la deuda")
                        windclientes.deiconify()
                        windabono_deuda.destroy()
                        clean1()
                        obt_clientes()
                    else:
                        messagebox.showerror("ERROR", "La cantidad abonada no puede ser mayor a la deuda. Error: 028")
                else:
                    messagebox.showerror("ERROR", "La Cedula que Ingreso no Existe. Error: 029")
            else:
                messagebox.showerror("ERROR", "El Abono debe ser mayor a 0. Error: 030")
        except:
            messagebox.showerror("ERROR", "El Abono debe ser numerico. Error: 031") 
    else:
        messagebox.showerror("ERROR", "No se puede dejar campos en blanco. Error: 032")

#Funciones de los botones para mpverse entre las ventanas de abono deuda
def pantallaprincipal():
    global windabono_deuda
    windabono_deuda.destroy()
    windclientes.destroy()
    wind.deiconify()

def pantallabuscar():
    global windbuscar
    windabono_deuda.destroy()
    windclientes.destroy()
    buscar()

def pantallapedido():
    global windpedido
    windabono_deuda.destroy()
    windclientes.destroy()
    pedido()

def pantallacliente():
    global windclientes
    windabono_deuda.destroy()
    windclientes.deiconify()

#Ventana abono deuda
def abono_deuda():
    global windabono_deuda
    global labono_deuda, eabono_deuda, eci_abono, babono_deuda

    windabono_deuda = Toplevel()
    windabono_deuda.resizable(width = 0, height = 0)
    windabono_deuda.geometry("245x230")
    windabono_deuda.iconbitmap('archivo.ico')
    windabono_deuda.title("Aplicacion de Inventario (ABONO DEUDA)")
    
    labono_deuda = Label(windabono_deuda, text = "Agregue el Monto que Desea Abonar")
    labono_deuda.place(x = 20, y = 10)

    eabono_deuda = Entry(windabono_deuda, width = 31)
    eabono_deuda.place(x = 25, y = 40)

    lci_abono = Label(windabono_deuda, text = "Agregue la Cedula del Cliente que Abono")
    lci_abono.place(x = 10, y = 70)

    eci_abono = Entry(windabono_deuda, width = 31)
    eci_abono.place(x = 25, y = 100)

    babono_deuda = ttk.Button(windabono_deuda, text = "Abono deuda", width = 30, command = lambda: resta_deuda())
    babono_deuda.place(x = 25, y = 135)

    nombre_image = resolver_ruta('buscar.png')
    img = PhotoImage(file = nombre_image)
    bsearch = Button(windabono_deuda, width = 35, height = 35, command = lambda: pantallabuscar())
    bsearch.image_names = img
    bsearch.config(image = img)
    bsearch.place(x = 25, y = 175)
    Hovertip(bsearch, text = "Buscar", hover_delay = 100)

    nombre_image = resolver_ruta('principal.png')
    img1 = PhotoImage(file = nombre_image)
    babrir_principal = Button(windabono_deuda, width = 35, height = 35, command = lambda: pantallaprincipal())
    babrir_principal.image_names = img1
    babrir_principal.config(image = img1)
    babrir_principal.place(x = 75, y = 175)
    Hovertip(babrir_principal, text = "Pantalla Principal", hover_delay = 100)

    nombre_image = resolver_ruta('cliente.png')
    img2 = PhotoImage(file = nombre_image)
    babrir_pedido = Button(windabono_deuda, width = 35, height = 35, command = lambda: pantallacliente())
    babrir_pedido.image_names = img2
    babrir_pedido.configure(image = img2)
    babrir_pedido.place(x = 125, y = 175)
    Hovertip(babrir_pedido, text = "Clientes", hover_delay = 100)

    nombre_image = resolver_ruta('pedidos.png')
    img3 = PhotoImage(file = nombre_image)
    babrir_cliente = Button(windabono_deuda, width = 35, height = 35, command = lambda: pantallapedido())
    babrir_cliente.image_names = img3
    babrir_cliente.configure(image = img3)
    babrir_cliente.place(x = 175, y = 175)
    Hovertip(babrir_cliente, text = "Pedidos", hover_delay = 100)

    clientes()
    windclientes.iconify()
    wind.iconify()

# Vacia la tabla producto
def borrarPRODUCTO():
    op_BD = 3
    tabla = 0
    clean_total = 1
    base_datos(op_BD, tabla, tu_clave, seleccion, op_producto, op_cliente, op_pedido, clean_total)
    clean()
    obt_productos()

#Valida que los campos de producto no esten vacios
def validacion():
    return len(eid.get()) != 0 and len(eprice_c.get()) != 0 and len(eprice_v.get()) != 0 and len(eamount.get()) != 0

#Rellena el treeview de producto 
def obt_productos():
    view = tree.get_children()
    for elementos in view:
         tree.delete(elementos)
    op_BD=0
    tabla=0
    op_producto=4
    resultado=(base_datos(op_BD,tabla,tu_clave,seleccion,op_producto))
    for row in resultado:
         tree.insert("", 0, text = "", values = (row[0], row[1], row[2], row[3]))

#Actualiza el treeview de producto
def actualizar_tabla():
    view = tree.get_children()
    for elementos in view:
         tree.delete(elementos)
    op_BD=0
    tabla=0
    op_producto=4
    resultado=(base_datos(op_BD,tabla,tu_clave,seleccion,op_producto))
    for row in resultado:
         tree.insert("", 0, text = "", values = (row[0], row[1], row[2], row[3]))
    b1["state"] = "normal"
    b2["state"] = "disable"
    b3["state"] = "disable"
    bmas["state"] = "disable"
    bmenos["state"] = "disable"
    eid["state"] = "normal"
    clean()
    Hovertip(eid, text = "", hover_delay = 360000)

#Añade un producto
def agregar_producto():
    tu_clave = []
    if validacion():
        try:
            tu_clave = []
            seleccion = eid.get()
            op_BD=0
            tabla=0
            op_producto = 4
            resultado1 = (base_datos(op_BD, tabla, tu_clave, seleccion, op_producto))
            len_resultado = len(resultado1)
            print(len_resultado)
            j = 0
            aux = 0
            for i in range(len_resultado):
                if eid.get() != resultado1[j][0]:
                    aux += 1
                    j += 1         
            if aux == len_resultado:
                float(eprice_c.get())
                float(eprice_v.get())
                int(eamount.get())
                if len(eid.get()) <= 15 and float(eprice_c.get()) > 0 and float(eprice_v.get()) > 0 and int(eamount.get()) >= 0: 
                    tu_clave.append(eid.get())
                    tu_clave.append(eprice_c.get())
                    tu_clave.append(eprice_v.get())
                    tu_clave.append(eamount.get())
                    op_BD=1
                    tabla=0
                    base_datos(op_BD, tabla, tu_clave)
                    messagebox.showinfo("BASE DE DATOS", "Se guardaron correctamente los campos")
                    clean()
                else:
                    messagebox.showerror("ERROR", "El ID PRODUCTO debe ser maximo de 15 caracteres, CANTIDAD PRODUCTO debe ser mayor o igual a 0 y los demas campos deben ser mayores a 0. Error: 033")
            else:
                messagebox.showerror("ERROR", "El ID del PRODUCTO ya existe no puede volver agregarlo. Error: 034")
        except:
            messagebox.showerror("ERROR", "PRECIO COSTO, PRECIO VENTA y CANTIDAD deben ser numericos. Error: 035")
    else:
        messagebox.showerror("ERROR", "No pueden haber campos en blanco. Error: 036")
    obt_productos()

#Edita un producto
def editar_producto():
    tu_clave = []
    if validacion():
        try:
            float(eprice_c.get())
            float(eprice_v.get())
            int(eamount.get())
            if float(eprice_c.get()) > 0 and float(eprice_v.get()) > 0 and int(eamount.get()) >= 0: 
                tu_clave.append(eid.get())
                tu_clave.append(eprice_c.get())
                tu_clave.append(eprice_v.get())
                tu_clave.append(eamount.get())
                op_BD=2
                tabla=0
                base_datos(op_BD, tabla, tu_clave)
                messagebox.showinfo("BASE DE DATOS", "Se actualizaron correctamente los campos")
                eid.configure(state = 'normal')
                clean()
                b1["state"] = "normal"
                b2["state"] = "disable"
                b3["state"] = "disable"
                bmas["state"] = "disable"
                bmenos["state"] = "disable"
            else:
                messagebox.showerror("ERROR", "El ID PRODUCTO debe ser maximo de 15 caracteres, CANTIDAD PRODUCTO debe ser mayor o igual a 0 y los demas campos deben ser mayores a 0. Error: 037")
        except:
            messagebox.showerror("ERROR", "PRECIO COSTO, PRECIO VENTA y CANTIDAD deben ser numericos. Error: 038")
    else:
        messagebox.showerror("ERROR", "No puede haber campos en blanco. Error: 039")
    obt_productos()
    Hovertip(eid, text = "", hover_delay = 360000)

#Elimina un producto
def eliminar_producto():
    tu_clave = []
    if len(eid.get()) != 0:
        tu_clave.append(eid.get())
        op_BD=3
        tabla=0
        base_datos(op_BD, tabla, tu_clave)
        eid.configure(state = 'normal')
        clean()
        b1["state"] = "normal"
        b2["state"] = "disable"
        b3["state"] = "disable"
        bmas["state"] = "disable"
        bmenos["state"] = "disable"
        messagebox.showinfo("BASE DE DATOS", "Se eliminaron correctamente los campos")
    else:
        messagebox.showerror("ERROR", "El ID Producto no puede estar vacio. Error: 040")
    obt_productos()
    Hovertip(eid, text = "", hover_delay = 360000)

#Suma en el inventario lo colocado en cantidad cuando se le da al boton +
def suma_inventario():
    if validacion():
        try:
            float(eprice_c.get())
            float(eprice_v.get())
            int(eamount.get())
            if float(eprice_c.get()) > 0 and float(eprice_v.get()) > 0 and int(eamount.get()) > 0:
                tu_clave = []
                cant_n = int(eamount.get())
                seleccion = eid.get()
                op_BD=0
                tabla=0
                op_producto = 0
                resultado = (base_datos(op_BD, tabla, tu_clave, seleccion, op_producto))
                tu_clave = []
                suma = cant_n + int(resultado[3])
                tu_clave.append(eid.get())
                tu_clave.append(eprice_c.get())
                tu_clave.append(eprice_v.get())
                tu_clave.append(suma)
                op_BD = 2
                tabla = 0
                base_datos(op_BD, tabla, tu_clave)
                messagebox.showinfo("BASE DE DATOS", "Se aumento correctamente el inventario")
                eid.configure(state = 'normal')
                clean()
                b1["state"] = "normal"
                b2["state"] = "disable"
                b3["state"] = "disable"
                bmas["state"] = "disable"
                bmenos["state"] = "disable"
            else:
                messagebox.showerror("ERROR", "Los campos desbloqueados deben ser mayores a 0. Error: 041")
        except:
            messagebox.showerror("ERROR", "PRECIO COSTO, PRECIO VENTA y CANTIDAD deben ser numericos. Error: 042")
    else:
        messagebox.showerror("ERROR", "No puede haber campos en blanco. Error: 043")
    obt_productos()
    Hovertip(eid, text = "", hover_delay = 360000)

#Resta en el inventario lo colocado en cantidad cuando se le da al boton -
def resta_inventario():
    if validacion():
        try:
            float(eprice_c.get())
            float(eprice_v.get())
            int(eamount.get())
            if float(eprice_c.get()) > 0 and float(eprice_v.get()) > 0 and int(eamount.get()) > 0:
                tu_clave = []
                cant_n = int(eamount.get())
                seleccion = eid.get()
                op_BD=0
                tabla=0
                op_producto = 0
                resultado = (base_datos(op_BD, tabla, tu_clave, seleccion, op_producto))
                if cant_n <= int(resultado[3]):
                    resta = int(resultado[3]) - cant_n
                    tu_clave.append(eid.get())
                    tu_clave.append(eprice_c.get())
                    tu_clave.append(eprice_v.get())
                    tu_clave.append(resta)
                    op_BD = 2
                    tabla = 0
                    base_datos(op_BD, tabla, tu_clave)
                else:
                    tu_clave = []
                    tu_clave.append(eid.get())
                    tu_clave.append(eprice_c.get())
                    tu_clave.append(eprice_v.get())
                    tu_clave.append(0)
                    op_BD = 2
                    tabla = 0
                    base_datos(op_BD, tabla, tu_clave)
                    messagebox.showwarning("ADVERTENCIA", "Habian "+ str(resultado[3]) +" repuestos de "+ str(seleccion) +" y usted ha restado " +
                    str(cant_n) + " asi que se ha colocado la cantidad en 0")
                messagebox.showinfo("BASE DE DATOS", "Se disminuyo correctamente el inventario")
                eid.configure(state = 'normal')
                clean()
                b1["state"] = "normal"
                b2["state"] = "disable"
                b3["state"] = "disable"
                bmas["state"] = "disable"
                bmenos["state"] = "disable"
            else:
                messagebox.showerror("ERROR", "Los campos desbloqueados deben ser mayores a 0. Error: 044")
        except:
           messagebox.showerror("ERROR", "PRECIO COSTO, PRECIO VENTA y CANTIDAD deben ser numericos. Error: 045") 
    else:
        messagebox.showerror("ERROR", "No puede haber campos en blanco. Error: 046")
    obt_productos()
    Hovertip(eid, text = "", hover_delay = 360000)

#Vacia los campos de producto
def clean():
    eid.delete(0, END)
    eprice_c.delete(0, END)
    eprice_v.delete(0, END)
    eamount.delete(0, END)

#Seleccionr con doble click producto
def seleccionar_click(event):
    try:
        clean()
        selected = tree.focus()
        values = tree.item(selected, 'values')
        eid.insert(0, values[0])
        eprice_c.insert(0, values[1])
        eprice_v.insert(0, values[2])
        eamount.insert(0, values[3])
        eid.configure(state = 'disable')
        b1["state"] = "disable"
        b2["state"] = "normal"
        b3["state"] = "normal"
        bmas["state"] = "normal"
        bmenos["state"] = "normal"
        Hovertip(eid, text = "No puede actualizar el ID de los productos ya ingresados", hover_delay = 100)
    except:
        messagebox.showerror("ERROR", "Debe hacer doble click sobre un producto. Error: 047")

#Ventana pincipal, Ventana producto
wn = Tk()
wind = wn

wind = wn
wind.title("Aplicacion de Inventario (PRODUCTOS)")
wind.resizable(width = 0, height = 0)
wind.geometry("802x530")
wind.iconbitmap('archivo.ico')
    
tree = ttk.Treeview(wn)
tree['columns'] = ("ID_PRODUCTO", "PRECIO_COSTO", "PRECIO_VENTA", "CANTIDAD")
tree.place(x = 0, y = 225)
tree.column('#0', width = 0, stretch = NO)
tree.column('#1', minwidth = 200, anchor = CENTER)
tree.column('#2', minwidth = 200, anchor = CENTER)
tree.column('#3', minwidth = 200, anchor = CENTER)
tree.column('#4', minwidth = 200, anchor = CENTER)
tree.heading('#1', text = 'ID PRODUCTO', anchor = CENTER)
tree.heading('#2', text = 'PRECIO COSTO', anchor = CENTER)
tree.heading('#3', text = 'PRECIO VENTA', anchor = CENTER)
tree.heading('#4', text = 'CANTIDAD', anchor = CENTER)
tree.bind("<Double-Button-1>", seleccionar_click)
obt_productos()

l1 = Label(wind, text = "Agregue un producto")
l1.place(x = 345, y = 15)

lid = Label(wind, text = "ID Producto: ")
lid.place(x = 305, y = 40)
eid = Entry(wind, width = 30)
eid.focus()
eid.place(x = 400, y = 40)

lprice_c = Label(wind, text = "Precio Costo: ")
lprice_c.place(x = 300, y = 70)
eprice_c = Entry(wind, width = 30)
eprice_c.place(x = 400, y = 70)

lprice_v = Label(wind, text = "Precio Venta: ")
lprice_v.place(x = 300, y = 100)
eprice_v = Entry(wind, width = 30)
eprice_v.place(x = 400, y = 100)

lamount = Label(wind, text = "Cantidad: ")
lamount.place(x = 318, y = 130)
eamount = Entry(wind, width = 30)
eamount.place(x = 400, y = 130)

b1 = ttk.Button(wind, text = "Guardar producto", width = 60, command = lambda: agregar_producto())
b1.place(x = 215, y = 160)

b2 = ttk.Button(wind, text = "Eliminar Producto", width = 60, command = lambda: eliminar_producto())
b2.place(x = 400, y = 470)
b2['state'] = 'disable'

b3 = ttk.Button(wind, text = "Actualizar Producto", width = 60, command = lambda: editar_producto())
b3.place(x = 30, y = 470)
b3['state'] = 'disable'

nombre_image = resolver_ruta('buscar.png')
img = PhotoImage(file = nombre_image)
bsearch = Button(wind, width = 35, height = 35, command = lambda: buscar())
bsearch.image_names = img
bsearch.config(image = img)
bsearch.place(x = 15, y = 15)
Hovertip(bsearch, text = "Buscar", hover_delay = 100)

nombre_image = resolver_ruta('cliente.png')
img1 = PhotoImage(file = nombre_image)
bclientes= Button(wind,width=35,height=35, command = lambda: clientes())
bclientes.image_names = img1
bclientes.config(image=img1)
bclientes.place(x=15,y=65)
Hovertip(bclientes, text = "Clientes", hover_delay = 100)

"Acabo de agregar el boton MAS"
nombre_image = resolver_ruta('sumar_inventario.png')
img2 = PhotoImage(file = nombre_image)
bmas = Button(wind, width = 15, height = 15, command = lambda: suma_inventario())
bmas.image_names = img2
bmas.config(image = img2)
bmas.place(x = 590, y = 130)
bmas['state'] = 'disable'

"Acabo de agregar el boton MENOS"
nombre_image = resolver_ruta('restar_inventario.png')
img3 = PhotoImage(file = nombre_image)
bmenos = Button(wind, width = 15, height = 15, command = lambda: resta_inventario())
bmenos.image_names = img3
bmenos.config(image = img3)
bmenos.place(x = 615, y = 130)
bmenos['state'] = 'disable'

"Acabo de agregar el boton actualizar"
nombre_image = resolver_ruta('actualizar_tree.png')
img4 = PhotoImage(file = nombre_image)
bactualizar = Button(wind, image = img4, width = 18, height = 18, command = lambda: actualizar_tabla())
bactualizar.place(x = 590, y = 160)
bactualizar.image_names = img4
bactualizar.config(image = img4)
Hovertip(bactualizar, text = "Actualizar Lista", hover_delay = 100)

"Agrege el boton de pedido"
nombre_image = resolver_ruta('pedidos.png')
img5 = PhotoImage(file = nombre_image)
bpedido = Button(wind, width = 35, height = 35, command = lambda: pedido())
bpedido.image_names = img5
bpedido.configure(image = img5)
bpedido.place(x = 15, y = 115)
Hovertip(bpedido, text = "Pedidos", hover_delay = 100)

"Agrege el boton de abono deuda"
nombre_image = resolver_ruta('abono_deuda.png')
img6 = PhotoImage(file = nombre_image)
babono_deuda = Button(wind, width = 35, height = 35, command = lambda: abono_deuda())
babono_deuda.image_names = img6
babono_deuda.configure(image = img6)
babono_deuda.place(x = 15, y = 165)
Hovertip(babono_deuda, text = "Abono Deuda", hover_delay = 100)

menuvar = Menu(wind)
menuDB = Menu(menuvar, tearoff = 0)
menuDB.add_command(label = "Limpiar Base De Datos", command = lambda: borrarTODO())
menuDB.add_command(label = "Salir", command = lambda : salirApp())
menuvar.add_cascade(label = "Inicio", menu = menuDB)

ayudamenu = Menu(menuvar, tearoff = 0)
ayudamenu.add_command(label = "Resetear Campos", command = lambda: clean())
ayudamenu.add_command(label = "Manual de Usuario", command = lambda: manual())
menuvar.add_cascade(label = "Ayuda", menu = ayudamenu)

wind.config(menu = menuvar)

nombre_base = resolver_ruta('inventario.db')
conn = sqlite3.connect(nombre_base)
conn.commit()

app = wind
wn.mainloop()