from database.mysql_engine import Base, engine, session
from database.pos_models import (Categoria, TipoIVA, Produto, Utilizador, Transacoes,
                                 ProdutosVendidos)


def populate_categorias():
    ...