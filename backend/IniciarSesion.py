import ArbolitoB
import os
import csv
import platform
import matplotlib.pyplot as plt

global limp

limp = "clear"

sistema_operativo = platform.system()

if sistema_operativo == "Windows":
    limp = "cls"
elif sistema_operativo == "Darwin":
    limp = "clear"

global C

global B


C=ArbolitoB.BTree(9)
B=ArbolitoB.BTree(2)
ArbolitoB.GuadarDatosUsers(C)
ArbolitoB.GuardarDatosArchivos(B)

def modificarIntentos(pos, intentos,celda):

    with open("Usuarios.csv", 'r', newline='') as archivo:
        reader = csv.reader(archivo)
        filas = list(reader)

        # Verificamos que la línea y la celda especificadas estén dentro de los límites
        if int(pos.key-1) < len(filas) and celda < len(filas[pos.key-1]):
            filas[pos.key-1][celda] = int(pos.intF)+intentos

    with open("Usuarios.csv", 'w', newline='') as archivo:
        writer = csv.writer(archivo)
        writer.writerows(filas)

def iniciarSesion():
    opcion=True

    while opcion:
        os.system(limp)
        user=input("Ingrese su usuario: \t")

        pos = C.search_user(user)

        if  pos is not None:
            opcion = False

    opcion = True

    intentos=0

    while opcion:
        os.system(limp)
        print(pos.Pasword)
        pasword = input("Contraseña: \t")

        if pasword == pos.Pasword:
            opcion = False
        else:
            intentos+=1
        
    modificarIntentos(pos,intentos,5)

    modificarIntentos(pos,1, 4)

    InterfazDeUsuario(pos)

def AgregarInformacion(Archivo,celda,infonueva):

    with open("Archivos.csv", 'r', newline='') as archivo:
        reader = csv.reader(archivo)
        filas = list(reader)

        if int(Archivo.key) < len(filas) and celda < len(filas[Archivo.key]):
            filas[Archivo.key][celda] = Archivo.info+" "+infonueva

    with open("Archivos.csv", 'w', newline='') as archivo:
        writer = csv.writer(archivo)
        writer.writerows(filas)

def ModificarInformacion2(Archivo,celda,infonueva):

    with open("Archivos.csv", 'r', newline='') as archivo:
        reader = csv.reader(archivo)
        filas = list(reader)

        if int(Archivo.key) < len(filas) and celda < len(filas[Archivo.key]):
            filas[Archivo.key][celda] = infonueva

    with open("Archivos.csv", 'w', newline='') as archivo:
        writer = csv.writer(archivo)
        writer.writerows(filas)

def ModificarInformacion(Archivo):
    infonueva = input("\nModificar Info:\t")
    ModificarInformacion2(Archivo,2,infonueva)
    infonueva = input("Modificar Dueño:\t")
    ModificarInformacion2(Archivo,1,infonueva)

def BorrarInfo(Archivo):
    ModificarInformacion2(Archivo,2," ")

def CambiarPermisos(Archivo):
    infonueva = input("\nNueno Nivel de Acceso: \t")
    ModificarInformacion2(Archivo,3,infonueva)

def BorrarArchivo(Archivo):
    ModificarInformacion2(Archivo,1," ")
    ModificarInformacion2(Archivo,2," ")
    ModificarInformacion2(Archivo,3," ")

def NivelDeAcceso(user, Archivo):
    option = 0
    
    print("\n\tEl archivo es de: ", Archivo.dueno)
    print("\tLa informacion de la especie es: ",Archivo.info)

    if(int(user.LevelAcces)>=3):
        if int(user.LevelAcces)>=int(Archivo.Nivel):
            Opciones = ["\n1 - Agregar informacion", "2 - Modificar Archivo", 
                        "3 - Borrar informacion", "4 - Cambiar Permisos", 
                        "5 - Borrar Archivo"]
        
            for i in range(int(user.LevelAcces)-3):
                print(Opciones[i])

            if int(user.LevelAcces)>3:
                option = int(input("Seleccione una opcion: \t"))

            if(option == 1 and (int(user.LevelAcces)-3)>=1):
                infonueva = input("Inserte Informacion a agregar:\t")
                AgregarInformacion(Archivo,2,infonueva)  
            elif(option == 2 and (int(user.LevelAcces)-3)>=2):
                ModificarInformacion(Archivo)
            elif(option == 3 and (int(user.LevelAcces)-3)>=3):
                BorrarInfo(Archivo)
            elif(option == 4 and (int(user.LevelAcces)-3)>=4):
                CambiarPermisos(Archivo)
            elif(option == 5 and (int(user.LevelAcces)-3)>=5):
                BorrarArchivo(Archivo)
            else: 
                print("Opcion invalida")
        elif (int(user.LevelAcces)>=1):
            print("\nExiste El archivo")
        else: 
            print("\nNo tiene acceso a este Archivo")
    else:
        print("\nNo tiene acceso a Archivos")

def AgregarArchivo(key, dueño, nivel, pasword):
    nueva_entidad = [key, dueño, nivel, pasword]

    with open('Archivos.csv', 'a', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        
        escritor_csv.writerow(nueva_entidad)

def Graficar():

    sizes = B.RecabarDatos()

    labels = ['Ninguno', 'Conocimiento', 'Ejecucion', 'Lectura', 'Agregar',
              'Modificar', 'Borrar informacion', 'Cambiar Permisos', 'Borrar Arhivo']

    colors = ['red', 'yellow', 'purple', 'orange', 'green', 'blue', 'pink', 
              'brown', 'gray']

    explode = (0, 0, 0, 0, 0, 0, 0, 0, 0)

    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, explode=explode)

    plt.title('Distribución de Niveles de Acceso')

    plt.axis('equal')

    plt.show()

    print(sizes)
        
def InterfazDeUsuario(User):
    os.system(limp)
    Sesion = True

    while Sesion:

        print("\nUsuario:",User.user)
        print("Nivel De acceso: ", User.LevelAcces)
        print("LLave: ",User.key)
        print("\n1 - Cerrar Sesion")
        print("2 - Buscar Archivo")
        print("3 - Agregar Archivo")
        print("4 - Listar Archivos Visibles")
        print("5 - Mostrar Estadisticas")
        print("6 - Grafica de Barras\n")

        opcion = input("Selecciona una opción (1-5): ")
        print("\n")
        os.system(limp)
        if opcion == "1":
            print("Cerrando sesión...")
            break
        elif opcion == "2":
            print("Seleccionaste la opción 2 - Buscar Archivo")
            Archivo = input("Archivo a buscar segun la llave: \t")
            A = B.search(int(Archivo))
            if A is None:
                A=B.search_user(Archivo)
            if A is None:
                print("No se encontro el archivo")
            else:
                NivelDeAcceso(User, A)
        elif opcion == "3":
            print("Seleccionaste la opción 3 - Agregar Archivo")
            if(int(User.LevelAcces)>=7):
                key = 1
                while B.search(key)!=None:
                    key = int(input("\nLlave entera?\t"))
                dueno = input("\nDueño?\t")
                nivel = input("\nNivel de Acceso?\t")
                info = input("\ninformacion?\t")
                AgregarArchivo(key, dueno,info, nivel)
        elif opcion == "4":
            print("Seleccionaste la opción 4 - Listar Archivos Visibles")

            B.traverse(User.LevelAcces)
        elif opcion == "5":
            print("Seleccionaste la opción 5 - Mostrar Estadísticas")
            Graficar()
        elif opcion == "6":
            print("Grafica de Barras: ")
            categorias = ["Inicios Correctos","Inicios Fallidos"]
            valores = [0,0]
            valores[0] = int(User.intB)
            valores[1] = int(User.intF)
            plt.bar(categorias, valores)

            plt.title('Inicios de Sesion')
            plt.xlabel('Categorías')
            plt.ylabel('Valores')
            plt.show()

            print(valores)

        else:
            print("Opción no válida. Por favor, selecciona una opción válida (1-5).")
