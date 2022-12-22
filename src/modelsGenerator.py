import os

# Como correr este codigo
# Desde la carpeta padre del proyecto correr
# "pipenv run python .\src\modelsGenerator.py"
# Se genera un nuevo archivo donde estan los nuevos modelos creados
# Se ejecuta desde pipenv porque alli estan los paquetes instalados

# postgresql+psycopg2://postgres:1224@localhost/IS_app

# command without flask
command = "sqlacodegen postgresql+psycopg2://postgres:1224@localhost/BD_app > .\generated_models.txt"
# command with flask
command2 = "python -m sqlacodegen.main --flask --outfile generated_models.py postgresql+psycopg2://postgres:1224@localhost:5432/BD_app"

os.system(command2)
