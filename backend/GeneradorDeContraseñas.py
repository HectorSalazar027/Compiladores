import random
import string

def generar_contraseña(longitud=12):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contraseña = ''.join(random.choice(caracteres) for _ in range(longitud))
    return contraseña

# Solicitar la longitud de la contraseña al usuario
longitud = int(input("Ingresa la longitud de la contraseña: "))
contraseña_generada = generar_contraseña(longitud)

print(f"Tu contraseña segura es: {contraseña_generada}")