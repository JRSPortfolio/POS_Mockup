from sqlalchemy.orm import Session

from database.pos_models import (Categoria, TipoIVA, Produto, Utilizador, Transacoes,
                                 ProdutosVendidos)

def create_db_category(db_session: Session, category_name: str, desc: str):
    db_category = Categoria(cat_name = category_name, description = desc)
    
    db_session.add(db_category)
    db_session.commit()
    db_session.refresh(db_category)
    
def validate_category_name(db_session: Session, category_name: str):
    name = db_session.query(Categoria).filter(Categoria.cat_name == category_name).first()
    
    if name:
        messages = [f"Já existe uma categoria {category_name}"]
        return messages
    else:
        return None
    
def get_categories_list(db_session: Session):
    category_names = db_session.query(Categoria.cat_name).all()
    categories = [category[0] for category in category_names]
    return categories