import os

command = "sqlacodegen postgresql+psycopg2://postgres:1224g@localhost/BD_app > .\generated_models.txt"

test = "systeminfo > .\Process.txt"

os.system(test)
