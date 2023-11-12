from database.mysql_engine import Base
from sqlalchemy import (Column, Integer, String, Numeric, ForeignKey, Date, Time, Boolean, UniqueConstraint,
                        func)
from sqlalchemy.orm import relationship

class Categoria(Base):
    __tablename__ = 'categorias'
    
    cat_id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    cat_name = Column(String(255), nullable = False, unique = True)
    description = Column(String(255), nullable = True)
    
    produto = relationship('Produto', back_populates = 'categoria')
    
class TipoIVA(Base):
    __tablename__ = 'tipo_iva'
    
    iva_id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    iva_value = Column(Integer, nullable = False, unique = True)
    iva_description = Column(String(255), nullable = False, unique = True)
    
    produto = relationship('Produto', back_populates = 'iva_tipo')
    
class Produto(Base):
    __tablename__ = 'produtos'
    
    prod_id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    name = Column(String(255), nullable = False)
    price = Column(Numeric(10, 2), nullable = False)
    price_withouth_iva = Column(Numeric(10, 2), nullable = False)
    cat_id = Column(Integer, ForeignKey("categorias.cat_id"), nullable = False)
    iva_id = Column(Integer, ForeignKey("tipo_iva.iva_id"), nullable = False)
    ordem = Column(String(255), nullable = True, unique = True)
    ativo = Column(Boolean, nullable = False)
    description = Column(String(255), nullable = True)
    
    categoria = relationship('Categoria', back_populates = 'produto')
    iva_tipo = relationship('TipoIVA', back_populates = 'produto')
    venda = relationship('ProdutosVendidos', back_populates = 'produto')
    alteracoes = relationship('MapaAleteracoeProduto', back_populates = 'produto')
    utilizador = relationship('FavoritosUtilizador', back_populates='produto')
    
class MapaAleteracoeProduto(Base):
    __tablename__ = 'mapa_alteracoes_produto'
    
    alter_id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    prod_id = Column(Integer, ForeignKey("produtos.prod_id"), nullable = False)
    data_alteracao = Column(Date, default = func.current_date(), nullable = False)
    hora_alteracao = Column(Time, default = func.current_timestamp(), nullable = False)
    previous_name = Column(String(255), nullable = False)
    previous_price = Column(Numeric(10, 2), nullable = False)
    previous_price_without_iva = Column(Numeric(10, 2), nullable = False)
    previous_iva_value = Column(Integer, nullable = False)
    
    produto = relationship('Produto', back_populates = 'alteracoes')
    
class Utilizador(Base):
    __tablename__ = 'utilizador'
    
    user_id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    name = Column(String(255), nullable = False)
    username = Column(String(255), nullable = False, unique = True)
    admin = Column(Boolean, nullable = False)
    password = Column(String(255), nullable = True)
    ativo = Column(Boolean, nullable = False)
    
    produto = relationship('FavoritosUtilizador', back_populates='utilizador')
    
class FavoritosUtilizador(Base):
    __tablename__ = 'favoritos_utilizador'
    
    cat_user_id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    user_id = Column(Integer, ForeignKey('utilizador.user_id'))
    prod_id = Column(Integer, ForeignKey('produtos.prod_id'))
    
    __table_args__ = (UniqueConstraint('user_id', 'prod_id', name='uq_user_prod_pair'),)
    
    utilizador = relationship('Utilizador', back_populates='produto')
    produto = relationship('Produto', back_populates='utilizador')
    
class Transacoes(Base):
    __tablename__ = 'transacoes'
    
    transacao_id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    data_venda = Column(Date, nullable = False, default = func.current_date())
    hora_venda = Column(Time, nullable = False, default = func.current_timestamp())
    
    produto = relationship('ProdutosVendidos', back_populates = 'transacao')

class ProdutosVendidos(Base):
    __tablename__ = 'produtos_vendidos'
    
    venda_id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    prod_id = Column(Integer, ForeignKey("produtos.prod_id"), nullable = False)
    transacao_id = Column(Integer, ForeignKey("transacoes.transacao_id"), nullable = False)
    
    produto = relationship('Produto', back_populates = 'venda')
    transacao = relationship('Transacoes', back_populates = 'produto')
    

    
    
