from tkinter import *
import tkinter.ttk as ttk
import csv
import sqlite3

# Llamamos la database

con = sqlite3.connect('JAnayaHenriquez.db')

c = con.cursor() # Creo la mano para poder meter datos, eliminar, crear tablas, etc.

#c.execute(""" CREATE TABLE IF NOT EXISTS data (
 #                                       id integer PRIMARY KEY AUTOINCREMENT,
#										mes integer NOT NULL,
#                                        indice text NOT NULL,
 #                                       anio integer NOT NULL,
  #                                      pico_cedula text NOT NULL,
#										cedula integer NOT NULL,
#										salida text NOT NULL
#                                   ); """ )


f = open("entrada.txt", "r")
vectaux1=f.readlines()
v=[]
for i in range(len(vectaux1)):
	vec=[]
	vec.append(vectaux1[i][0])
	vec.append(int(vectaux1[i][2:6]))
	v.append(vec)
dsem=["lunes","martes","miercoles","jueves","viernes","sabado","domingo"]
meses=["Enero","Febrero","Marzo","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
cmes=[31,29,31,30,31,30,31,31,30,31,30,31]


def obt(mes,pico,ind,cedula):
	ldi=v[ind][0]
	di=0
	salida=""
	salbd=""
	cedula=1
	if(ldi=="L"):
		di=0
	else:
		if(ldi=="M"):
			di=1
		else:
			if(ldi=="X"):
				di=2
			else:
				if(ldi=="J"):
					di=3
				else:
					if(ldi=="V"):
						di=4
					else:
						if(ldi=="S"):
							di=5
						else:
							if(ldi=="D"):
								di=6

	estim=0
	for i in range(mes):
		estim+= cmes[i]
	def cantidad(di,estim):
		df = di
		for i in range(estim):
			if(df<6):
				df+=1
			else:
				df=0
		return df
	df=cantidad(di,estim)

	dias = []
	for i in range(0,len(pico),2):
		dias.append(int(pico[i:i+1]))
	dist =0
	for i in dias:
		if(i==cedula):
			break
		dist+=1
	for i in range(0,cmes[mes-1],len(dias)):
		if(dist+i<cmes[mes-1]):
			salida+="Dia semana: "+dsem[cantidad(df,dist+i)]+", Fecha: "+str(1+dist+i)+"/"+str(mes)+"/"+str(v[ind][1])+"\n\n"
			salbd+=" "+dsem[cantidad(df,dist+i)]+", Fecha: "+str(1+dist+i)+"/"+str(mes)+"/"+str(v[ind][1])+" "
	vecsal=[mes,v[ind][0],v[ind][1],pico,cedula,salbd]


	c.execute('INSERT INTO data (mes, indice, anio, pico_cedula, cedula,  salida) VALUES (?, ?, ?, ?, ?, ?)', (mes, v[ind][0], v[ind][1], pico, cedula, salbd))
	
	con.commit()
	return salida


def cantidadc():

	return c.execute("SELECT COUNT(*) FROM data").fetchone()[0]

def crear_ventana():
	global ventana
	ventana = Tk()
	ventana.geometry("600x600")
	ventana.title("Datos Hospital")
	crear_inicio()

def crear_inicio():
	global Frame_inicial
	Frame_inicial = Frame(ventana)
	Frame_inicial.place(x=0, y=0, width=600, height=600)
	opcion_var = IntVar()
	Label = ttk.Label(Frame_inicial, text="Escoja el dia y año: ") 
	Label.config(font=('Arial', 10))
	Label.place( x=230,y=50)
	for i in range(len(v)):
		texto= str(v[i][0])+" "+ str(v[i][1])
		ttk.Radiobutton(Frame_inicial, text=texto, variable=opcion_var,value=i).place(x=250,y=i*20+150)
	ttk.Button(Frame_inicial, text ="Consultar",command=lambda:inicio_consultar(opcion_var.get())).place(x=250, y=550)

def crear_consulta(x=0,y=""):
	global Frame_consultar
	Frame_consultar = Frame(ventana)
	Frame_consultar.place(x=0, y=0, width=600, height=600)
	Label1 = ttk.Label(Frame_consultar, text="Ingrese el pico y cedula: ") 
	Label1.config(font=('Arial', 10))
	Label1.place( x=230,y=20)
	fecha_var = StringVar()
	fecha_entry = ttk.Entry(Frame_consultar, textvariable=fecha_var,width=25)
	fecha_entry.place(x=175, y=50)
	Label2 = ttk.Label(Frame_consultar, text="Ingrese el mes: ") 
	Label2.config(font=('Arial', 10))
	Label2.place( x=250,y=100)
	combo=ttk.Combobox(Frame_consultar,values=meses, state="readonly")
	combo.current(0)
	combo.place(x=220, y=130)
	Label3 = ttk.Label(Frame_consultar, text="Ingrese su cedula: ") 
	Label3.config(font=('Arial', 10))
	Label3.place( x=240,y=180)
	combo1=ttk.Combobox(Frame_consultar,values=[0,1,2,3,4,5,6,7,8,9,0], state="readonly")
	combo1.current(0)
	combo1.place(x=220, y=210)
	Label4 = ttk.Label(Frame_consultar, text="Cantidad de consultas: "+str(cantidadc())) 
	Label4.config(font=('Arial', 10))
	Label4.place( x=220,y=260)
	if(len(y)>0):
		Label3 = ttk.Label(Frame_consultar, text=y) 
		Label3.config(font=('Arial', 10))
		Label3.place( x=190,y=310)
	ttk.Button(Frame_consultar, text ="Inicio",command=consultar_inicio).place(x=250, y=550)
	ttk.Button(Frame_consultar, text ="Consultar",command =lambda:consultar_consultar(x,obt(combo.current(),fecha_var.get(),x,combo1.current()))).place(x=350, y=50)

def eliminar(x):
	x.destroy()

def inicio_consultar(x=0):
	eliminar(Frame_inicial)
	crear_consulta(x)

def consultar_inicio():
	eliminar(Frame_consultar)
	crear_inicio()

def consultar_consultar(x= 0,y=""):
	eliminar(Frame_consultar)
	crear_consulta(x,y)

crear_ventana()


ventana.mainloop()

con.close()