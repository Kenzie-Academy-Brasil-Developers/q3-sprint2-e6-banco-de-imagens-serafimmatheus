# Banco de Imagens

Observe a rubrica do enunciado

Requisitos:
1 - Cada tipo de arquivo deve ser salvo em um diretório com o nome de sua extensão.
Os diretórios com cada extensão deverão estar dentro do diretório definido na variavel
de ambiente FILES_DIRECTORY

2 - Caso os diretórios necessários não existam, devem ser criados sempre que a
aplicação iniciar.

3 - O tamanho máximo de arquivos deve ser parametrizado via variável de ambiente
MAX_CONTENT_LENGTH e possuir o valor 1MB por padrão;

4 - As extensões de arquivos permitidas devem ser armazenadas em uma variável de ambiente
chamada ALLOWED_EXTENSIONS;

5 - As operações sobre arquivos devem ser importadas de um módulo chamado image que estará
disponível em uma biblioteca (pacote) denominado kenzie criado por você;

6 - Rota POST com o endpoint /upload que terá a função de enviar um arquivo por um Multipart
Form nomeado "file", com o valor sendo o arquivo a ser enviado;

7 - Rota GET com o endpoint /files que irá listar todos os arquivos e um endpoint /files/<extension>
que lista os arquivos de um determinado tipo;

8 - Rota GET com o endpoint /download/<file_name> responsável por fazer o download do arquivo solicitado
em file_name;

9 - Rota GET com o endpoint /download-zip com query params (file_extension, compression_ratio) para
especificar o tipo de arquivo para baixar todos compactados e também a taxa de compressão.
