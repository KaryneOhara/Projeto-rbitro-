from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from models import conectar_db

class Contratante(UserMixin):
    _hash : str
    def __init__(self, **kwargs):
        self._id = None
        if 'nome' in kwargs.keys():
            self._nome = kwargs['nome']
        if 'email' in kwargs.keys():
            self._email = kwargs['email']
        if 'cpf' in kwargs.keys():
            self._cpf = kwargs['cpf']
        if 'telefone' in kwargs.keys():
            self._telefone = kwargs['telefone']
        if 'senha' in kwargs.keys():
            self._senha = kwargs['senha']
        if 'hash' in kwargs.keys():
            self._hash = kwargs['hash']


    def get_id(self):
        return str(self._id)

    
    @property
    def _senha(self):
        return self._hash
    
    @_senha.setter
    def _senha(self, senha):
        self._hash = generate_password_hash(senha)

    def add_contratante(self):        
        conn = conectar_db()  
        cursor = conn.cursor(dictionary=True)      
        cursor.execute("INSERT INTO tb_contratantes(con_nome, con_email, con_cpf, con_telefone, con_senha) VALUES(%s,%s,%s,%s,%s)", (self._nome, self._email, self._cpf, self._telefone, self._hash,))
        self._id = cursor.lastrowid
        conn.commit()
        conn.close()
        cursor.close()
        return True
    
    @classmethod
    def get(cls,user_id):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_contratantes WHERE con_id = %s", (user_id,))
        user = cursor.fetchone()
        conn.commit()
        conn.close()
        if user:
            loaduser = Contratante(email=user['con_email'] , hash=user['con_senha'])
            loaduser._id = user['con_id']
            return loaduser
        else:
            return None
    
    @classmethod
    def exists(cls, email):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_contratantes WHERE con_email = %s", (email,))
        user = cursor.fetchall()
        conn.commit()
        conn.close()
        if user:
            return True
        else:
            return False
    
    
    
    @classmethod
    def get_by_email(cls,email):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT con_id, con_email, con_senha FROM tb_contratantes WHERE con_email = %s", (email,))
        user = cursor.fetchone() 
        conn.commit()
        conn.close()
    
        return user
