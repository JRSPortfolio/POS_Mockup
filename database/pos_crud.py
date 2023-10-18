from sqlalchemy.orm import Session
from sqlalchemy import asc

from database.pos_models import (Categoria, TipoIVA, Produto, Utilizador, Transacoes,
                                 ProdutosVendidos)

def create_db_category(db_session: Session, category_name: str, desc: str):
    db_category = Categoria(cat_name = category_name, description = desc)
    
    db_session.add(db_category)
    db_session.commit()
    db_session.refresh(db_category)
    
def validate_category_name(db_session: Session, category_name: str):
    if len(category_name) == 0 or category_name.isspace():
        messages = [f"Nome de categoria não pode estar vazio"]
        return messages
    
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

def create_db_tipo_iva(db_session: Session, iva_name: str, value: int):
    db_iva = TipoIVA(iva_value = value, iva_description = iva_name)
    
    db_session.add(db_iva)
    db_session.commit()
    db_session.refresh(db_iva)
    
def validate_iva_input(db_session: Session, iva_name: str, value: int):
    name = db_session.query(TipoIVA).filter(TipoIVA.iva_description == iva_name).first()
    iva_value = db_session.query(TipoIVA).filter(TipoIVA.iva_value == value).first()
    
    messages = []
    
    if len(iva_name) == 0 or iva_name.isspace():
        messages.append("Campo Designação não pode estar vazio")
    if not isinstance(value, int):
        messages.append("O campo Taxa é um valo inteiro")
    elif value <0 or value >100:
        messages.append("Taxa têm de ser entre 0 e 100%")
    if messages:
        return messages
    
    if name:
        messages.append(f"Já existe uma designação {iva_name}")
    if iva_value:
        messages.append(f"Já existe uma Taxa de {value}%")
    if messages:
        return messages
    else:
        return None
    
def get_iva_types_list(db_session: Session):
    iva_types = db_session.query(TipoIVA.iva_description).order_by(asc(TipoIVA.iva_value)).all()
    iva_list = [iva[0] for iva in iva_types]
    return iva_list
    
def get_iva_value_by_name(db_session: Session, iva_name: str):
    iva_value = db_session.query(TipoIVA).filter(TipoIVA.iva_description == iva_name).value(TipoIVA.iva_value)
    return iva_value
    