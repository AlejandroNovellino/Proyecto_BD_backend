import os

# postgresql+psycopg2://postgres:1224@localhost/IS_app

# command without flask
command = "sqlacodegen postgresql+psycopg2://postgres:1224@localhost/BD_app > .\generated_models.txt"
# command with flask
command2 = "python -m sqlacodegen.main --flask --outfile generated_models.py postgresql+psycopg2://postgres:1224@localhost:5432/BD_app"

os.system(command2)
