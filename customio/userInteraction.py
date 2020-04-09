import os

def list_mid_files_in_directory():
    included_extensions = ['mid']
    file_names = [fn for fn in os.listdir('.')
                  if any(fn.endswith(ext) for ext in included_extensions)]
    print(*file_names, sep='\n')
    return file_names

def RequestUserInfo():
    print("Nombre de archivos disponibles en el directorio:")

    media_files = list_mid_files_in_directory()

    print(media_files)

    print("Insertar nombre de Archivo")
    nombredeArchivo = input()
    if nombredeArchivo not in media_files:
      print("Coloque bien el nombre del archivo, incluyendo la extensión")
      exit()
    print("Espectograma ON? Y/N")
    rta=input()
    if(rta=='Y' or rta=='y'):
      BooleanEspectograma=1
    elif(rta=='n' or rta=='N'):
      BooleanEspectograma=0
    else:
      print("Input Error")
      exit()
    
    return (nombredeArchivo, BooleanEspectograma)