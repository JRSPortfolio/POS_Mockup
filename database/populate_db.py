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
                cat_id = 2, iva_id = 3, ordem = 'Bebidas1', ativo = True, 
                description = 'Descrição Um'),
        Produto(name = 'Sumo Laranja', price = dec(2.10), price_withouth_iva = dec(1.91),
                cat_id = 2, iva_id = 2, ordem = 'Bebidas2', ativo = True,
                description = 'Descrição Dois'),
        Produto(name = 'Sumo Manga', price = dec(2.40), price_withouth_iva = dec(2.40),
                cat_id = 2, iva_id = 1, ordem = 'Bebidas3', ativo = True,
                description = 'Descrição Três'),
        Produto(name = 'Sumo Limão', price = dec(2.68), price_withouth_iva = dec(2.44),
                cat_id = 2, iva_id = 2, ordem = 'Bebidas4', ativo = True, 
                description = 'Descrição Três e Meio'),
        Produto(name = 'Rissol', price = dec(2.60), price_withouth_iva = dec(2.36),
                cat_id = 1, iva_id = 2, ordem = 'Aperitivos1', ativo = True, 
                description = 'Descrição Quatro'),
        Produto(name = 'Croquete', price = dec(3.10), price_withouth_iva = dec(2.58),
                cat_id = 1, iva_id = 3, ordem = 'Aperitivos2', ativo = True,
                description = 'Descrição Cinco'),
        Produto(name = 'Chamuça', price = dec(1.95), price_withouth_iva = dec(1.95),
                cat_id = 1, iva_id = 1, ordem = 'Aperitivos3', ativo = True,
                description = 'Descrição Seis'),
        Produto(name = 'Bife Novilho', price = dec(11.95), price_withouth_iva = dec(9.96),
                cat_id = 3, iva_id = 3, ordem = 'Pratos1', ativo = True,
                description = 'Descrição Sete'),
        Produto(name = 'Bife Vazia', price = dec(12.95), price_withouth_iva = dec(11.77),
                cat_id = 3, iva_id = 2, ordem = 'Pratos2', ativo = True,
                description = 'Descrição Sete e Meio'),
        Produto(name = 'Bife Acém', price = dec(12.25), price_withouth_iva = dec(11.14),
                cat_id = 3, iva_id = 2, ordem = 'Pratos3', ativo = True,
                description = 'Descrição Oito'),
        Produto(name = 'Bife Frango', price = dec(10.45), price_withouth_iva = dec(9.50),
                cat_id = 3, iva_id = 2, ordem = 'Pratos4', ativo = True,
                description = 'Descrição Oito e Meia'),
        Produto(name = 'Bife Porco', price = dec(11.20), price_withouth_iva = dec(11.20),
                cat_id = 3, iva_id = 1, ordem = 'Pratos5', ativo = True,
                description = 'Descrição Nove'),
        Produto(name = 'Bife Atum', price = dec(12.25), price_withouth_iva = dec(11.14),
                cat_id = 3, iva_id = 2, ativo = False,
                description = 'Descrição Nove'),
        Produto(name = 'Sumo Melão', price = dec(2.40), price_withouth_iva = dec(2.40),
                cat_id = 2, iva_id = 1, ativo = False,
                description = 'Descrição Três'),
    ])
    session.commit()
    session.close()
    
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