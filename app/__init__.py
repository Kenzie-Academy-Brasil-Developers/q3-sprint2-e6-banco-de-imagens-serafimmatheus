# Desenvolva suas rotas aqui

from http import HTTPStatus
from http.client import REQUEST_ENTITY_TOO_LARGE
from socket import send_fds
from flask import Flask, request, safe_join, send_file, send_from_directory
import os

from .kenzie import criando_rota_abspath, listando_todas_imagem, teste

app = Flask(__name__)
MAX_CONTENT_LENGTH = os.getenv("MAX_CONTENT_LENGTH")
app.config['MAX_CONTENT_LENGTH'] = int(MAX_CONTENT_LENGTH)

FILES_DIRECTORY = os.getenv("FILES_DIRECTORY")
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS")


try:
    os.mkdir(FILES_DIRECTORY)
    os.mkdir(f"{FILES_DIRECTORY}/png")
    os.mkdir(f"{FILES_DIRECTORY}/gif")
    os.mkdir(f"{FILES_DIRECTORY}/jpg")

except:
    @app.errorhandler(413)
    def request_entity_too_large(error):
        return {"msg": f"{error}"}, HTTPStatus.REQUEST_ENTITY_TOO_LARGE


@app.post("/upload")
def upload(): 
    file_send = request.files.values()

    for file in file_send:
        file_split = file.filename.split('.')[-1]
        allowed_ext = ALLOWED_EXTENSIONS.lower()
        if file_split in allowed_ext:

            file_path = criando_rota_abspath(FILES_DIRECTORY, file_split)
            root, dirs, file_list = next(os.walk(FILES_DIRECTORY))
            all_files = listando_todas_imagem(dirs, FILES_DIRECTORY)

            if file.filename in all_files:
                return {"msg": f"{file.filename} already exists!"}, HTTPStatus.CONFLICT
            file.save(criando_rota_abspath(file_path, file.filename)), HTTPStatus.CREATED

        else:
            return {"msg": f".{file_split} not is suported!"}, HTTPStatus.UNSUPPORTED_MEDIA_TYPE  
        
    return {"mgs": "Images uploaded!"}, HTTPStatus.CREATED

      
@app.get("/files")
def get_files():
    root, dirs, list_files = next(os.walk(FILES_DIRECTORY))
    list_image = listando_todas_imagem(dirs, FILES_DIRECTORY)

    if len(list_image) > 0:
        return {"all_img": list(list_image)}, HTTPStatus.OK


    return {"msg": "not found"}, HTTPStatus.NOT_FOUND


@app.get("/files/<extension>")
def get_files_extension(extension):
    root, dirs, file_lists = next(os.walk(FILES_DIRECTORY))

    list_image = listando_todas_imagem(dirs, FILES_DIRECTORY)

    file_lists_filtereds = [i for i in list_image if i.endswith(extension)]

    if file_lists_filtereds:
        return {"data": file_lists_filtereds}
    else:
        return {"data": "file not found"}, HTTPStatus.NOT_FOUND


@app.get("/download/<file_name>")
def download(file_name: str):    
    file_name_split = file_name.split(".")[-1]
    root, dirs, files = next(os.walk(FILES_DIRECTORY))

    dirs_list = listando_todas_imagem(dirs, FILES_DIRECTORY)

    file_path = criando_rota_abspath(FILES_DIRECTORY, file_name_split)
    file_name_list = criando_rota_abspath(file_path, file_name)

    if file_name in dirs_list:
        return send_file(file_name_list, as_attachment=True), HTTPStatus.OK

    
    return {"msg": f"{file_name} not found"}, HTTPStatus.NOT_FOUND


@app.get("/download-zip")
def download_zip():
    file_extension = request.args.get("file_extension")
    compression_ratio = request.args.get("compression_ratio")
    root, dirs, files = next(os.walk(FILES_DIRECTORY))
    list_image = listando_todas_imagem(dirs, FILES_DIRECTORY)

    if file_extension in str(list_image):
        file_name_split = file_extension.split(".")[-1]
        file_path = criando_rota_abspath("/tmp", f'{file_name_split}.zip')
        
        print(file_path)

        if compression_ratio:
            command = f"zip -{compression_ratio} -r /tmp/{file_name_split}.zip {FILES_DIRECTORY}/{file_name_split}/*"
        else:
            command = f"zip -6 -r /tmp/{file_name_split}.zip {FILES_DIRECTORY}/{file_name_split}/*"

        os.system(command)

        return send_file(file_path, as_attachment=True), HTTPStatus.OK
    
    
    return {"msg": f"{file_extension} not found"}, HTTPStatus.NOT_FOUND

