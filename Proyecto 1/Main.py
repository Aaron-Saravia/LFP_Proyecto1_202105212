from tkinter import *
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import customtkinter
from tkdocviewer import *

num ="0123456789"
letters = "abcdefghijklmñopqrstuvwxyz"

#--------------Buscador-------------------------------------------
def explorador_archivos(): 
    global filename
    filename = fd.askopenfilename(filetype = "/", title = "Select a File", 
                                          filetypes = (("Text files", "*.txt*"), 
                                                       ("all files", "*.*")))

#---------Funcion que pone en marca el analizador léxico----------------------
def Analizar():
    global filename
    lista_errores=[]
    lista_reconocidos=[]
    try:
        tokens = {
        "tk_tipo_abierto": "<tipo>",
        "tk_tipo_cerrado": "</tipo>",
        "tk_suma" : "<operacion=suma>",
        "tk_resta":"<operacion=resta>",
        "tk_mult":"<operacion=multiplicacion>",
        "tk_div":"<operacion=division>",
        "tk_pot":"<operacion=potencia>",
        "tk_raiz":"<operacion=raiz>",
        "tk_inv":"<operacion=inverso>",
        "tk_seno":"<operacion=seno>",
        "tk_cos":"<operacion=coseno>",
        "tk_tan":"<operacion=tangente>",
        "tk_mod":"<operacion=mod>",
        "tk_op_cerrado": "</operacion>",
        "tk_num_abierto": "<numero>",
        "tk_num_cerrado": "</numero>",
        "tk_info_abierto":"<Texto>",
        "tk_info_cerrado":"</Texto>",
        "tk_fun_abrir":"<Funcion=ESCRIBIR>",
        "tk_fun_cerrar":"</Funcion>",
        "tk_titulo1":"<Titulo>",
        "tk_titulo2":"</Titulo>",
        "tk_des1":"<Descripcion>",
        "tk_des2":"</Descripcion>",
        "tk_cont1":"<Contenido>",
        "tk_cont2":"</Contenido>",
        "tk_estilo1":"<Estilo>",
        "tk_estilo2":"</Estilo>",
        "numeroDecimal":afd_numeroDecimal,
        "numeroEntero":afd_numeroEntero
        }
        
        f = open(filename, "r")
        f = f.read()
        f = f.strip()
        print(f)
        f = f.replace(" ", "")
        f = f.replace("\n", "")
        f = f.replace("\t", "")
        f = f.lower()

        indice = 0
        encontrado = False

        while indice < len(f):
            for key, value in tokens.items():
                if type(value) == str:
                    if indice + len(value) > len(f): continue
                    lexema = f[indice : indice + len(value)]
                    if value == lexema:
                        print("se encontró el token:", key, ", en la posicion:", indice, "lexema:",lexema)
                        indice += len(value)-1
                        encontrado = True
                        break
                else:
                    indice_aux = indice
                    anterior_reconocido = False

                    while(indice_aux <= len(f)):
                        lexema = f[indice:indice_aux]
                        encontrado = value(lexema)

                        if not encontrado and anterior_reconocido:
                            encontrado = True
                            lexema = f[indice:indice_aux-1]
                            indice = indice_aux-1
                            print("se encontró el token:", key, ", en la posicion:", indice, "lexema:",lexema)
                            break

                        anterior_reconocido = encontrado
                        indice_aux += 1

                    if encontrado:
                        indice-=1

                if encontrado: break

            if not encontrado:
                print("error lexico en la posicion:", indice, ", no se ha reconocido el lexema:",f[indice])

            encontrado = False
            indice += 1
    except:
        mb.showerror("ADVERTENCIA: ", "No hay datos que Analizar")


#---------Automarta para analisis de numeros decimales---------------------------------------------
def afd_numeroDecimal(lexema):
    estado = 0
    aceptacion = [3]
    
    for char in lexema:
        if estado == 0 and char in num:
            estado = 1
        elif estado == 1 and char in num:
            estado = 1
        elif estado == 1 and char == ".":
            estado = 2
        elif estado == 2 and char in num:
            estado = 3
        elif estado == 3 and char in num:
            estado = 3
        else:
            estado = -1
            break
    
    if estado in aceptacion:
        return True
    
    return False

#---------Automata para analisis de numeros enteros-------------------------------------------------
def afd_numeroEntero(lexema):
    estado = 0
    aceptacion = [1]
    
    for char in lexema:
        if estado == 0 and char in num:
            estado = 1
        elif estado == 1 and char in num:
            estado = 1
        else:
            estado = -1
            break
    
    if estado in aceptacion:
        return True
    
    return False

#-----------Funcion para regresar a la ventana anterior---------------------------------------------------------------------
def Regresar(Padre, Hijo):
    Padre.deiconify()
    Hijo.destroy()
    
#---------Funcion para finalizar la ejecucion del programa-----------------------------------------------------------
def Salir(Padre):
    Padre.destroy()

#--------Ventana emergente para mostrar el manual de usuario---------------------------------------------------------
def Manual_user():
    Ventana.withdraw()
    Ver_Manu_user = Toplevel()
    Ver_Manu_user.title("Manual de usuario")
    Ver_Manu_user.geometry("800x900")
    Ver_Manu_user.config(bg="green")

    btt_back = customtkinter.CTkButton(Ver_Manu_user,  text = "Regresar", command = lambda: Regresar(Ventana, Ver_Manu_user),
        text_font=("Showcard Gothic", 15, "bold"), text_color="black", hover= True, hover_color= "#f2f2f2", height=30, width= 100,
        border_width=2, corner_radius=20, border_color= "#d3d3d3", bg_color="green", fg_color= "#fafafa")    
    btt_back.pack()

    ver_doc1 = DocViewer(Ver_Manu_user)
    ver_doc1.pack(side="top", expand=1, fill="both")
    ver_doc1.display_file("Manual de usuario de proyecto 1 LFP A+.pdf")

#-------Ventana emergente para mostrar el manual técnico------------------------------------------------
def Manual_Tec():
    Ventana.withdraw()
    Ver_Manu_Tec = Toplevel()
    Ver_Manu_Tec.title("Manual Técnico")
    Ver_Manu_Tec.geometry("800x900")
    Ver_Manu_Tec.config(bg="green")
    
    btt_back = customtkinter.CTkButton(Ver_Manu_Tec,  text = "Regresar", command = lambda: Regresar(Ventana, Ver_Manu_Tec),
        text_font=("Showcard Gothic", 15, "bold"), text_color="black", hover= True, hover_color= "#f2f2f2", height=30, width= 100,
        border_width=2, corner_radius=20, border_color= "#d3d3d3", bg_color="green", fg_color= "#fafafa")  
    btt_back.pack()

    ver_doc2 = DocViewer(Ver_Manu_Tec)
    ver_doc2.pack(side="top", expand=1, fill="both")
    ver_doc2.display_file("Manual Tecnico de proyecto 1 LFP A+.pdf")

#-----Funcion para mostrar los datos del creador------------------------------------------------
def Datos_user():
    mb.showinfo(message='''Actualmente (Año 2022) es estudiante de Lenguajes Formales y de Programacion en la USAC:

 
          CREADOR: Aarón Abdam Saravia Martínez


                        CARNET: 202105212''',
                        
                        title="Datos del creador")

#-----Funcion para mostrar los datos en el cuadro de texto------------------------------------------------
def Ver_datos():
    global filename
    if filename != "":
        achivo_lectura = open(filename, "r", encoding="utf-8")
        contenido = achivo_lectura.read()
        achivo_lectura.close()
        text.delete("1.0", tk.END) 
        text.insert("1.0", contenido)
    else:
        mb.showerror("ADVERTENCIA: ", "No hay datos cargados")

#-----Funcion para guardar nuevos datos a un mismo archivo--------------------------------------------------
def Guardar():
    global filename
    if filename != "" and text.get("1.0", tk.END) != "":
        achivo_lectura=open(filename, "w", encoding="utf-8")
        achivo_lectura.write(text.get("1.0", tk.END))
        achivo_lectura.close()
        mb.showinfo("Información", "Los datos fueron guardados en el archivo.")
    else:
        mb.showerror("ADVERTENCIA: ", "No hay datos nuevos que guardar")

#-----Funcion para crear y guardar los datos en un nuevo archivo----------------------------------------------------
def Guardar_as():
    if text.get(1.0, "end-1c") != "":
        nombre_file = fd.asksaveasfile(title = "Guardar como", filetypes = (("Text files", "*.txt*"), ("all files", "*.*")))

        if nombre_file:
            mensaje = text.get("1.0", tk.END)
            nombre_file.write(mensaje)
            nombre_file.close()
            mb.showinfo("INFORMACION: ", "Se guardaron correctamente los datos")
    else:
        mb.showerror("ADVERTENCIA: ", "No hay datos que guardar")
    text.delete("1.0", tk.END)

#------Ventana emergenente para edicion del archivo cargado---------------------------------------------
def Editar_archivo():
    Ventana.withdraw()
    Editar = Toplevel()
    Editar.title("Editar")
    Editar.geometry("800x700")
    Editar.config(bg="green")

    global text
    text= Text(Editar,width= 80,height=30)
    text.place(x=70, y = 100)

    btt_show_datos = customtkinter.CTkButton(Editar, command = Ver_datos, text= "Ver datos cargados", text_font=("Showcard Gothic", 15, "bold"),
        text_color="black", hover= True, hover_color= "#f2f2f2", height=30, width= 100, border_width=2, corner_radius=20,
        border_color= "#d3d3d3", bg_color="green", fg_color= "#fafafa")
    btt_show_datos.place(x = 50, y = 40)
    
    btt_Guardar_as = customtkinter.CTkButton(Editar,command= lambda: Guardar_as(),text= "Guardar Como", text_font=("Showcard Gothic", 15, "bold"),
        text_color="black", hover= True, hover_color= "#f2f2f2", height=30, width= 100, border_width=2, corner_radius=20,
        border_color= "#d3d3d3", bg_color="green", fg_color= "#fafafa")
    btt_Guardar_as.place(x = 350, y = 40)

    btt_Guardar = customtkinter.CTkButton(Editar, command = Guardar, text= "Guardar", text_font=("Showcard Gothic", 15, "bold"),
        text_color="black", hover= True, hover_color= "#f2f2f2", height=30, width= 100, border_width=2, corner_radius=20,
        border_color= "#d3d3d3", bg_color="green", fg_color= "#fafafa")
    btt_Guardar.place(x = 600, y = 40)

    btt_back = customtkinter.CTkButton(Editar,command= lambda: Regresar(Ventana, Editar),text= "Regresar", text_font=("Showcard Gothic", 15, "bold"),
        text_color="black", hover= True, hover_color= "#f2f2f2", height=30, width= 100, border_width=2, corner_radius=20,
        border_color= "#d3d3d3", bg_color="green", fg_color= "#fafafa")
    btt_back.place(x = 325, y = 625)
    
    
#------Ventana MAIN--------------------------------------------------
Ventana = Tk()
Ventana.title('Analizador Léxico') 
Ventana.geometry("800x600")
Ventana.config(background = "green") 


label_Archivo = Label(Ventana,  text = "Archivo", bg = "green", fg = "blue", font=("Showcard Gothic", 40, "bold")) 
label_Archivo.place(x = 75, y = 75)

btt_Abrir = customtkinter.CTkButton(Ventana,command= explorador_archivos,text= "Abrir", text_font=("Showcard Gothic", 20, "bold"),
    text_color="black", hover= True, hover_color= "#f2f2f2", height=30, width= 100, border_width=2, corner_radius=20,
    border_color= "#d3d3d3", bg_color="green", fg_color= "#fafafa")
btt_Abrir.place(x = 120, y = 175)

btt_Editar_archivo = customtkinter.CTkButton(Ventana,command= Editar_archivo,text= "Editar archivo", text_font=("Showcard Gothic", 20, "bold"),
    text_color="gray", hover= True, hover_color= "#f2f2f2", height=30, width= 100, border_width=2, corner_radius=20,
    border_color= "#d3d3d3", bg_color="green", fg_color= "#fafafa")
btt_Editar_archivo.place(x = 50, y = 250)

btt_Analizar = customtkinter.CTkButton(Ventana,command= Analizar,text= "Analizar", text_font=("Showcard Gothic", 20, "bold"),
    text_color="black", hover= True, hover_color= "#f2f2f2", height=30, width= 100, border_width=2, corner_radius=20,
    border_color= "#d3d3d3", bg_color="green", fg_color= "#fafafa")
btt_Analizar.place(x = 100, y = 325)

btt_Error = customtkinter.CTkButton(Ventana, text= "Errores", text_font=("Showcard Gothic", 20, "bold"),
    text_color="gray", hover= True, hover_color= "#f2f2f2", height=30, width= 100, border_width=2, corner_radius=20,
    border_color= "#d3d3d3", bg_color="green", fg_color= "#fafafa")
btt_Error.place(x = 100, y = 400)

btt_salir = customtkinter.CTkButton(Ventana, command= lambda: Salir(Ventana), text= "Salir", text_font=("Showcard Gothic", 25, "bold"),
    text_color="black", hover= True, hover_color= "#f2f2f2", height=30, width= 100, border_width=2, corner_radius=20,
    border_color= "#d3d3d3", bg_color="green", fg_color= "#fafafa") 
btt_salir.place(x = 325, y = 500)

label_Ayuda = Label(Ventana,  text = "Ayuda", bg = "green", fg = "blue", font=("Showcard Gothic", 40, "bold")) 
label_Ayuda.place(x = 505, y = 75)

btt_Manual_user = customtkinter.CTkButton(Ventana,command= Manual_user,text= "Manual de Usuario", text_font=("Showcard Gothic", 20, "bold"),
    text_color="gray", hover= True, hover_color= "#f2f2f2", height=30, width= 100, border_width=2, corner_radius=20,
    border_color= "#d3d3d3", bg_color="green", fg_color= "#fafafa")
btt_Manual_user.place(x = 430, y = 175)

btt_Manual_Tec = customtkinter.CTkButton(Ventana,command= Manual_Tec,text= "Manual Técnico", text_font=("Showcard Gothic", 20, "bold"),
    text_color="black", hover= True, hover_color= "#f2f2f2", height=30, width= 100, border_width=2, corner_radius=20,
    border_color= "#d3d3d3", bg_color="green", fg_color= "#fafafa")
btt_Manual_Tec.place(x = 455, y = 250)

btt_Datos = customtkinter.CTkButton(Ventana,command= Datos_user, text= "Temas de Ayuda", text_font=("Showcard Gothic", 20, "bold"),
    text_color="gray", hover= True, hover_color= "#f2f2f2", height=30, width= 100, border_width=2, corner_radius=20,
    border_color= "#d3d3d3", bg_color="green", fg_color= "#fafafa")
btt_Datos.place(x = 455, y = 325)


Ventana.mainloop()
