from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from models import conectar_db

class Arbitro(UserMixin):
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

    def add_arbitro(self):        
        conn = conectar_db()  
        cursor = conn.cursor(dictionary=True)      
        cursor.execute("INSERT INTO tb_arbitros(arb_nome, arb_email, arb_cpf, arb_telefone, arb_senha) VALUES(%s,%s,%s,%s,%s)", (self._nome, self._email, self._cpf, self._telefone, self._hash,))
        self._id = cursor.lastrowid
        conn.commit()
        conn.close()
        cursor.close()
        return True
    
    @classmethod
    def get(cls,user_id):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_arbitros WHERE arb_id = %s", (user_id,))
        user = cursor.fetchone()
        conn.commit()
        conn.close()
        if user:
            loaduser = Arbitro(email=user['arb_email'] , hash=user['arb_senha'])
            loaduser._id = user['arb_id']
            return loaduser
        else:
            return None
    
    @classmethod
    def exists(cls, email):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_arbitros WHERE arb_email = %s", (email,))
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
        cursor.execute("SELECT arb_id, arb_email, arb_senha FROM tb_arbitros WHERE arb_email = %s", (email,))
        user = cursor.fetchone() 
        conn.commit()
        conn.close()
    
        return user
