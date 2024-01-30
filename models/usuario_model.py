from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()
target_metadata = Base.metadata

class ClienteAdm(Base):
    __tablename__ = 'pessoas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(120))
    email = Column(String(100))
    senha = Column(String(500))
    nascimento = Column(String(11))
    cpf = Column(String(15))
    genero = Column(String(10))
    telefone = Column(String(20))
    foto = Column(String(1000))
    adm = Column(Boolean, default=False)
    bloqueado = Column(Boolean, default=False)
    fatores_email = Column(Boolean, default=False)
    telegram = Column(String(100))
    data_criacao = Column(TIMESTAMP)
    data_atualizacao = Column(TIMESTAMP)

    def __repr__(self):
        pessoa_dict = {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'senha': self.senha,
            'nascimento': self.nascimento,
            'cpf': self.cpf,
            'genero': self.genero,
            'telefone': self.telefone,
            'foto': self.foto,
            'adm': self.adm,
            'bloqueado': self.bloqueado,
            "fatores": self.fatores_email,
            "telegram": self.telegram,
            "data_criacao": self.formatar_data(self.data_criacao),
            "data_atualizacao": self.formatar_data(self.data_atualizacao),
        }
        return json.dumps(pessoa_dict)
    
    def formatar_data(self, data):
        if data is not None:
            return data.strftime("%Y-%m-%d %H:%M:%S")
        return None
    