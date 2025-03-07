import mysql.connector

def conectar_db():
    #alterar de acordo com a sua senha
    return mysql.connector.connect(host='localhost', user='root', password='mysqlK.O2806', database='db_projeto')
