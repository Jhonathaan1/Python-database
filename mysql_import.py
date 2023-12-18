import mysql.connector

meubd = mysql.connector.connect(
    host='localhost',
    user='root',
    password='72992982',
    database='pythonsql'
)

comando = """INSERT INTO pythonsql.venda(nome, email, senha)
values
    ('alisson', 'alissonr.p18@gmail.com', '123456') """

cursor = meubd.cursor()
print('Banco de Dados Conectado com sucesso')
cursor.execute(comando)
meubd.commit()
cursor.execute("SELECT * FROM pythonsql.venda")

meuresultado = cursor.fetchall()

print(meuresultado)
