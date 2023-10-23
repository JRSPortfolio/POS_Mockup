from sqlalchemy.orm import Session
from sqlalchemy import asc, func

from database.pos_models import (Categoria, TipoIVA, Produto, Utilizador, Transacoes,
                                 ProdutosVendidos)
from decimal import Decimal as dec

###
###
### Categorias
###
###
def create_db_category(db_session: Session, category_name: str, desc: str):
    db_category = Categoria(cat_name = category_name, description = desc)
    
    db_session.add(db_category)
    db_session.commit()
    db_session.refresh(db_category)
    
def validate_category_name(db_session: Session, category_name: str):
    messages = []
    if len(category_name) == 0 or category_name.isspace():
        messages = [f"Nome de categoria não pode estar vazio"]
        return messages
    
    name = db_session.query(Categoria).filter(Categoria.cat_name == category_name).first()
    if name:
        messages = [f"Já existe uma categoria {category_name}"]
        return messages
    
def get_categories_list(db_session: Session):
    category_names = db_session.query(Categoria.cat_name).all()
    categories = [category[0] for category in category_names]
    return categories

def remove_category_by_name(db_session: Session, category_name: str):
    db_row = db_session.query(Categoria).filter(Categoria.cat_name == category_name).first()
    db_session.delete(db_row)
    db_session.commit()
    
def change_category_by_name(db_session: Session, category_name: str, new_name: str, value: int):    
    db_row = db_session.query(Categoria).filter(Categoria.cat_name == category_name).first()
    if db_row.cat_name != new_name:
        db_row.cat_name = new_name
    if db_row.description != value:
        db_row.description = value
    db_session.commit()
    
def get_category_description_by_name(db_session: Session, name: str):
    description = db_session.query(Categoria).filter(Categoria.cat_name == name).value(Categoria.description)
    return description

def get_category_id_by_name(db_session: Session, name: str):
    cat_id = db_session.query(Categoria).filter(Categoria.cat_name == name).value(Categoria.cat_id)
    return cat_id
###
###
### IVA
###
###
def get_tipo_iva_list(db_session: Session):
    iva_names = db_session.query(TipoIVA.iva_description).all()
    iva_list = [iva[0] for iva in iva_names]
    return iva_list

def create_db_tipo_iva(db_session: Session, iva_name: str, value: int):
    db_iva = TipoIVA(iva_value = value, iva_description = iva_name)
    
    db_session.add(db_iva)
    db_session.commit()
    db_session.refresh(db_iva)
    
def validate_iva_input(db_session: Session, iva_name: str, value: int):
    messages = []
    val_iva_name_list = validate_iva_name(db_session, iva_name)
    if val_iva_name_list:
        messages.extend(val_iva_name_list)
    val_iva_values_list = validate_iva_value(db_session, value)
    if val_iva_values_list:
        messages.extend(val_iva_values_list)
    if messages:
        return messages
    
def validate_iva_name(db_session: Session, iva_name: str):
    messages = []
    name = db_session.query(TipoIVA).filter(TipoIVA.iva_description == iva_name).first()
    if len(iva_name) == 0 or iva_name.isspace():
        messages.append("Campo Designação não pode estar vazio")
    if name:
        messages.append(f"Já existe uma designação {iva_name}")
    return messages

def validate_iva_value(db_session: Session, value: int):
    messages = []
    iva_value = db_session.query(TipoIVA).filter(TipoIVA.iva_value == value).first()
    if not isinstance(value, int):
        messages.append("O campo Taxa é um valo inteiro")
    elif value <0 or value >100:
        messages.append("Taxa têm de ser entre 0 e 100%")
    elif iva_value:
        messages.append(f"Já existe uma Taxa de {value}%")
    return messages
        
def get_iva_types_list(db_session: Session):
    iva_types = db_session.query(TipoIVA.iva_description).order_by(asc(TipoIVA.iva_value)).all()
    iva_list = [iva[0] for iva in iva_types]
    return iva_list

def get_iva_id(db_session: Session, value: int):
    iva_id = db_session.query(TipoIVA).filter(TipoIVA.iva_value == value).value(TipoIVA.iva_id)
    return iva_id
    
def get_iva_value_by_name(db_session: Session, iva_name: str):
    iva_value = db_session.query(TipoIVA).filter(TipoIVA.iva_description == iva_name).value(TipoIVA.iva_value)
    return iva_value
    
def remove_iva_by_name(db_session: Session, iva_name: str):
    db_row = db_session.query(TipoIVA).filter(TipoIVA.iva_description == iva_name).first()
    db_session.delete(db_row)
    db_session.commit()
    
def change_iva_by_name(db_session: Session, iva_name: str, new_name: str, value: int):    
    db_row = db_session.query(TipoIVA).filter(TipoIVA.iva_description == iva_name).first()
    if db_row.iva_description != new_name:
        db_row.iva_description = new_name
    if db_row.iva_value != value:
        db_row.iva_value = value
    db_session.commit()
    
###
###
### Produto
###
###
def validate_product_inputs(db_session, product_name: str, category: str, price: dec):
    messages = []
    val_product_name = validate_product_name(db_session, product_name, category)
    val_product_price = validate_product_price(price)
    if val_product_name:
        messages.extend(val_product_name)
    if val_product_price:
        messages.extend(val_product_price)
    return messages
    
def validate_product_name(db_session: Session, product_name: str, category: str):
    messages = []
    category_id = db_session.query(Categoria).filter(Categoria.cat_name == category).value(Categoria.cat_id)
    name = db_session.query(Produto).filter(Produto.name == product_name, Produto.cat_id == category_id).first()
    if len(product_name) == 0 or product_name.isspace():
        messages.append("Campo Nome não pode estar vazio")
    if name:
        messages.append(f"Já existe uma designação {product_name} em {category}")
    return messages
    
def validate_product_price(price: dec):
    messages = []
    if not isinstance(price, dec):
        messages.append("O campo Preço é um valor númerico")
    elif price < 0:
        messages.append("Preço necessita de ser maior que 0")
    return messages

def get_product_order(db_session: Session, product: str, category: str):
    order = db_session.query(Produto).filter(Produto.cat_name == category, Produto.name == product).value(Produto.ordem)
    order_value = order[0]
    order_num = int(order_value[len(category):])
    return order_num

def get_last_product_order(db_session: Session, category: str):
    category_id = db_session.query(Categoria).filter(Categoria.cat_name == category).value(Categoria.cat_id)
    order = db_session.query(Produto).filter(Produto.cat_id == category_id, func.max(Produto.ordem)).first()
    order_value = order[0]
    order_num = int(order_value[len(category):])
    return order_num
    
def get_product_iva_type(db_session: Session, product: str, category: str):
    iva = db_session.query(Produto).filter(Produto.cat_name == category, Produto.name == product).value(Produto.iva_id)
    iva_id = iva[0]
    iva_name_row = db_session.query(TipoIVA).filter(TipoIVA.iva_id == iva_id).first()
    iva_name = iva_name_row[0]
    return iva_name
    
def get_product_category(db_session: Session, ):
    ...
    
def create_db_product(db_session: Session, name: str, price: dec, cat_name: str, iva_value: int, ordem: int, description: str, iva_checkbox: bool):
    cat_id = get_category_id_by_name(db_session, cat_name)
    iva_price = get_iva_price(price, iva_checkbox, iva_value)
    iva_id = get_iva_id(db_session, iva_value)
    product_order = cat_name + str(ordem)
    if iva_checkbox:
        db_product = Produto(name = name, price = price, price_withouth_iva = iva_price, cat_id = cat_id, iva_id = iva_id,
                             ordem = product_order, description = description)
    else:
        db_product = Produto(name = name, price = iva_price, price_withouth_iva = price, cat_id = cat_id, iva_id = iva_id,
                             ordem = product_order, description = description)
    
    db_session.add(db_product)
    db_session.commit()
    db_session.refresh(db_product)
    
def get_iva_price(price: dec, iva_checkbox: bool, iva_value: int):
    if iva_checkbox:
        iva_price = price / (1 + (iva_value / 100))
    else:
        iva_price = price + (price * (iva_value / 100))
    return iva_price
    
###
###
### Utilizador
###
###


###
###
### Transacoes
###
###


###
###
### ProdutosVendidos
###
###

def get_stylesheet():
    with open('assets//stylesheet.qss', 'r') as file:
        style = file.read()
    return style