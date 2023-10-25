##
## Module for populating de database for testing purposes
##
##


from database.mysql_engine import engine, session
from database.pos_models import (Base, Categoria, TipoIVA, Produto, Utilizador, Transacoes,
                                 ProdutosVendidos)
from decimal import Decimal as dec

def populate_categorias():
    session.add_all([
        Categoria(cat_name = 'Aperitivos', description = 'Descrição Um'),
        Categoria(cat_name = 'Bebidas', description = 'Descrição Dois'),
        Categoria(cat_name = 'Pratos', description = 'Descrição Três'),
        Categoria(cat_name = 'Sobremesas', description = 'Descrição Quatro')
    ])
    session.commit()

def populate_tipo_iva():
    session.add_all([
        TipoIVA(iva_value = 0, iva_description = 'Isento'),
        TipoIVA(iva_value = 10, iva_description = 'Intermédio'),
        TipoIVA(iva_value = 20, iva_description = 'Alto')
    ])
    session.commit()
    
def populate_produtos():
    session.add_all([
        Produto(name = 'Sumo Ananás', price = dec(2.20), price_withouth_iva = dec(1.83),
                cat_id = 2, iva_id = 3, ordem = 'Bebidas1', description = 'Descrição Um'),
        Produto(name = 'Sumo Laranja', price = dec(2.10), price_withouth_iva = dec(1.91),
                cat_id = 2, iva_id = 2, ordem = 'Bebidas2', description = 'Descrição Dois'),
        Produto(name = 'Sumo Manga', price = dec(2.40), price_withouth_iva = dec(2.40),
                cat_id = 2, iva_id = 1, ordem = 'Bebidas3', description = 'Descrição Três'),
        Produto(name = 'Rissol', price = dec(2.60), price_withouth_iva = dec(2.36),
                cat_id = 1, iva_id = 2, ordem = 'Aperitivos1', description = 'Descrição Quatro'),
        Produto(name = 'Croquete', price = dec(3.10), price_withouth_iva = dec(2.58),
                cat_id = 1, iva_id = 3, ordem = 'Aperitivos2', description = 'Descrição Cinco'),
        Produto(name = 'Chamuça', price = dec(1.95), price_withouth_iva = dec(1.95),
                cat_id = 1, iva_id = 1, ordem = 'Aperitivos3', description = 'Descrição Seis'),
        Produto(name = 'Bife Novilho', price = dec(11.95), price_withouth_iva = dec(9.96),
                cat_id = 3, iva_id = 3, ordem = 'Pratos1', description = 'Descrição Sete'),
        Produto(name = 'Bife Frango', price = dec(10.45), price_withouth_iva = dec(9.50),
                cat_id = 3, iva_id = 2, ordem = 'Pratos2', description = 'Descrição Sete'),
        Produto(name = 'Bife Porco', price = dec(11.20), price_withouth_iva = dec(11.20),
                cat_id = 3, iva_id = 1, ordem = 'Pratos3', description = 'Descrição Oito')
    ])
    session.commit()
    
# def populate_utilizadores():
#     session.add_all([
#         Utilizador(name = , username = , admin = , password = ),
#     ])
#     session.commit()
    
# def populate_transacoes():
#     session.add_all([
#         Transacoes(data_venda = , hora_venda = ),
#     ])
#     session.commit()
    
# def populate_produtos_vendidos():
#     session.add_all([
#         ProdutosVendidos(prod_id = , transacao_id =),
#     ])
#     session.commit()