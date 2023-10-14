from database.mysql_engine import Base
from sqlalchemy import (Column, Integer, String, Numeric, ForeignKey, Date, Time, Boolean)
from sqlalchemy.orm import relationship

class Categorias(Base):
    __tablename__ = 'categorias'
    
    cat_id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    cat_name = Column(String(255), nullable = False)
    description = Column(String(255), nullable = True)
    
    produtos = relationship('Produtos', back_populates = 'categoria')
    
class TipoIVA(Base):
    __tablename__ = 'tipo_iva'
    
    iva_id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    iva_value = Column(Numeric, nullable = False)
    iva_description = Column(String(255), nullable = False)
    
    produto = relationship('Produtos', back_populates = 'iva_tipo')
    
class Produtos(Base):
    __tablename__ = 'produtos'
    
    prod_id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    name = Column(String(255), nullable = False)
    price = Column(Numeric, nullable = False)
    price_withouth_iva = Column(Numeric, nullable = False)
    cat_id = Column(Integer, ForeignKey("categorias.cat_id"), nullable = False)
    iva_id = Column(Integer, ForeignKey("tipo_iva.iva_id"), nullable = False)
    ordem = Column(Integer, nullable = False)
    description = Column(String(255), nullable = True)
    
    categoria = relationship('Categorias', back_populates = 'produtos')
    iva_tipo = relationship('TipoIVA', back_populates = 'produto')
    venda = relationship('ProdutosVendidos', back_populates = 'produtos')
    
class Utilizador(Base):
    __tablename__ = 'utilizador'
    
    user_id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    name = Column(String(255), nullable = False)
    username = Column(String(255), nullable = False, unique = True)
    admin = Column(Boolean, nullable = False)
    password = Column(String(255), nullable = True)

class Transacoes(Base):
    __tablename__ = 'transacoes'
    
    transacao_id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    data_venda = Column(Date, nullable = False)
    hora_venda = Column(Time, nullable = False)
    
    produto = relationship('ProdutosVendidos', back_populates = 'ProdutosVendidos')

class ProdutosVendidos(Base):
    __tablename__ = 'produtos_vendidos'
    
    venda_id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    prod_id = Column(Integer, ForeignKey("produtos.prod_id"), nullable = False)
    transacao_id = Column(Integer, ForeignKey("transacoes.transacao_id"), nullable = False)
    
    produtos = relationship('Produtos', back_populates = 'venda')
    transacao = relationship('Transacoes', back_populates = 'produto')
    

    
    
