# Desenvolva sua lógica de manipulação das imagens aqui
from http import HTTPStatus
import os
from flask import send_file, safe_join


def criando_rota_abspath(FILES_DIRECTORY, filename):
    abs_path = os.path.abspath(FILES_DIRECTORY)
    file_path = safe_join(abs_path, filename)
    
    return file_path


def listando_todas_imagem(dirs, FILES_DIRECTORY): 
    list_image = []
    for indice in dirs:
        *_, file = next(os.walk(f"{FILES_DIRECTORY}/{indice}"))
        
        for lista in file:
            list_image.append(lista)
    return list_image

def teste(file_send, ALLOWED_EXTENSIONS, FILES_DIRECTORY):
    ...   
            
