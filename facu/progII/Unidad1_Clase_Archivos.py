"""Excepciones y Archivos"""

def main():
    # Estructura posible de try/except
    try:
        # Ejercicio con archivos

        # Se declara una variable "f" para abrir un archivo
        f = open("miarchivo.txt", "w")
        # Escribimos una linea
        f.write("linea 1")
        f.close() # siempre hay que cerrar el archivo 

        # Para ver el archivo, lo abrimos. Lo leemos con 'print'
        f = open("miarchivo.txt", "w") # "w" 
        print("linea nueva", file=f) # "file=f" apunta al archivo
        f.close()

        f = open("miarchivo.txt", "r") # "r" solo lectura
        for i in f: 
            print(i)
        f.close()

    except ZeroDivisionError:
        # Siempre se definen excepciones desde la mas particular a la mas general
        print("Excepcion particular.")
    except:
        print("Ocurrio un error inesperado en tiempo de ejecución")
    else:
        print("Else no se ejecuta siempre, solo lo hace cuando cuando NO HAY EXCEPCION")
    finally:
        print("finally se ejecuta siempre, haya error o no")


if __name__ == "__main__":
    main()