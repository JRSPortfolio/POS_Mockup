from sqlalchemy.orm import Session

from database.pos_models import (Categoria, TipoIVA, Produto, Utilizador, Transacoes,
                                 ProdutosVendidos)

def create_db_category(db_session: Session, category_name: str, desc: str):
    db_category = Categoria(cat_name = category_name, description = desc)
    
    db_session.add(db_category)
    db_session.commit()
    db_session.refresh(db_category)
    
def validate_category_name(db_session: Session, category_name: str):
    name = db_session.query(Categoria).filter(Categoria.name == category_name).first()
    
    if name:
        return f"Já existe uma categoria {category_name}"
    else:
        return None