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
    db_session.close()
    
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
    db_session.close()
    
def change_category_by_name(db_session: Session, category_name: str, new_name: str, value: int):    
    db_row = db_session.query(Categoria).filter(Categoria.cat_name == category_name).first()
    if db_row.cat_name != new_name:
        db_row.cat_name = new_name
    if db_row.description != value:
        db_row.description = value
    db_session.commit()
    db_session.close()
    
def get_category_description_by_name(db_session: Session, name: str):
    description = db_session.query(Categoria).filter(Categoria.cat_name == name).value(Categoria.description)
    return description

def get_category_id_by_name(db_session: Session, name: str):
    cat_id = db_session.query(Categoria).filter(Categoria.cat_name == name).value(Categoria.cat_id)
    return cat_id

def get_amount_products_in_category(db_session: Session, category: str):
    category_id = get_category_id_by_name(db_session, category)
    products = db_session.query(Produto).filter(Produto.cat_id == category_id).order_by(Produto.ordem).all()
    
    product_items = {}
    
    for prod in products:
        iva_value = str(get_iva_value_by_id(db_session, prod.iva_id)) + '%'
        order = prod.ordem[len(category):]
        product_items[prod.prod_id] = [prod.name ,str(prod.price), iva_value, order]
    return product_items
    
    
    
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
    db_session.close()
    
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
        
def get_iva_id(db_session: Session, value: int):
    iva_id = db_session.query(TipoIVA).filter(TipoIVA.iva_value == value).value(TipoIVA.iva_id)
    return iva_id
    
def get_iva_value_by_name(db_session: Session, iva_name: str):
    iva_value = db_session.query(TipoIVA).filter(TipoIVA.iva_description == iva_name).value(TipoIVA.iva_value)
    return iva_value

def get_iva_value_by_id(db_session: Session, iva_id: int):
    iva_value = db_session.query(TipoIVA).filter(TipoIVA.iva_id == iva_id).value(TipoIVA.iva_value)
    return iva_value
    
def remove_iva_by_name(db_session: Session, iva_name: str):
    db_row = db_session.query(TipoIVA).filter(TipoIVA.iva_description == iva_name).first()
    db_session.delete(db_row)
    db_session.commit()
    db_session.close()
    
def change_iva_by_name(db_session: Session, iva_name: str, new_name: str, value: int):    
    db_row = db_session.query(TipoIVA).filter(TipoIVA.iva_description == iva_name).first()
    if db_row.iva_description != new_name:
        db_row.iva_description = new_name
    if db_row.iva_value != value:
        db_row.iva_value = value
    db_session.commit()
    db_session.close()
    
def get_iva_value_and_name_by_id(db_session: Session, iva_id: int):
    iva_type = db_session.query(TipoIVA).filter_by(iva_id = iva_id).first()
    iva = (iva_type.iva_description, iva_type.iva_value)
    return iva
###
###
### Produto
###
###
def validate_add_product_inputs(db_session, product_name: str, category: str, price: dec):
    messages = []
    val_product_name = validate_product_add_name(db_session, product_name, category)
    val_product_price = validate_product_price(price)
    if val_product_name:
        messages.extend(val_product_name)
    if val_product_price:
        messages.extend(val_product_price)
    return messages

def validate_edit_product_inputs(product_name: str, price: dec):
    messages = []
    val_product_name = validate_product_edit_name(product_name)
    val_product_price = validate_product_price(price)
    if val_product_name:
        messages.extend(val_product_name)
    if val_product_price:
        messages.extend(val_product_price)
    return messages
    
def validate_product_add_name(db_session: Session, product_name: str, category: str):
    messages = []
    category_id = db_session.query(Categoria).filter(Categoria.cat_name == category).value(Categoria.cat_id)
    name = db_session.query(Produto).filter(Produto.name == product_name, Produto.cat_id == category_id).first()
    if len(product_name) == 0 or product_name.isspace():
        messages.append("Campo Nome não pode estar vazio")
    if name:
        messages.append(f"Já existe uma designação {product_name} em {category}")
    return messages

def validate_product_edit_name(product_name: str):
    messages = []
    if len(product_name) == 0 or product_name.isspace():
        messages.append("Campo Nome não pode estar vazio")
    return messages
    
def validate_product_price(price: dec):
    messages = []
    if not isinstance(price, dec):
        messages.append("O campo Preço é um valor númerico")
    elif price < 0:
        messages.append("Preço necessita de ser maior que 0")
    return messages

def get_product_order(db_session: Session, order: int, category: str):
    order_name = category + str(order)
    existing_order = db_session.query(Produto).filter(Produto.ordem == order_name).value(Produto.ordem)
    if not existing_order:
        order_num = None
        return order_num
    else:
       return order
   
# def get_last_product_order(db_session: Session, category: str):
#     category_id = db_session.query(Categoria).filter(Categoria.cat_name == category).value(Categoria.cat_id)
#     order = db_session.query(Produto).filter(Produto.cat_id == category_id).with_entities(func.max(Produto.ordem)).first()
#     order_string = order[0]
#     if order_string:
#         order_num = int(order_string[len(category):])
#         return order_num
#     else:
#         return 0
    
def get_last_product_order(db_session: Session, category: str):
    category_id = db_session.query(Categoria).filter(Categoria.cat_name == category).value(Categoria.cat_id)
    order = db_session.query(Produto).filter(Produto.cat_id == category_id).order_by(Produto.ordem.desc()).first()
    if order:
        order_name = order.ordem
        order_num = int(order_name[len(category):])
        db_session.close()
        return order_num
    else:
        db_session.close()
        return 0


    
def get_product_iva_type(db_session: Session, product: str, category: str):
    iva_id = db_session.query(Produto).filter(Produto.cat_name == category, Produto.name == product).value(Produto.iva_id)
    iva_name = db_session.query(TipoIVA).filter(TipoIVA.iva_id == iva_id).first()
    return iva_name
    
def create_db_product(db_session: Session, name: str, price: dec, cat_name: str, iva_value: int, ordem: int, description: str, iva_checkbox: bool):
    cat_id = get_category_id_by_name(db_session, cat_name)
    iva_price = set_iva_price(price, iva_checkbox, iva_value)
    iva_id = get_iva_id(db_session, iva_value)
    product_order = cat_name + str(ordem)
    
    price = price.quantize(dec('0.00'))
    iva_price = iva_price.quantize(dec('0.00'))
    if iva_checkbox:
        db_product = Produto(name = name, price = price, price_withouth_iva = iva_price, cat_id = cat_id, iva_id = iva_id,
                             ordem = product_order, description = description)
    else:
        db_product = Produto(name = name, price = iva_price, price_withouth_iva = price, cat_id = cat_id, iva_id = iva_id,
                             ordem = product_order, description = description)
    
    db_session.add(db_product)
    db_session.commit()
    db_session.refresh(db_product)
    db_session.close()
    
def set_iva_price(price: dec, iva_checkbox: bool, iva_value: int):
    if iva_checkbox:
        iva_price = dec(price / (1 + dec((iva_value / 100))))
    else:
        iva_price = dec(price + (price * dec((iva_value / 100))))
    return iva_price

def get_product_name_by_category_and_order(db_session: Session, order: int, category: str):
    named_order = category + str(order)
    name = db_session.query(Produto).filter(Produto.ordem == named_order).value(Produto.name)
    return name
    
def switch_product_order(db_session: Session, name: str, existing_order: str, new_order: str):
    db_row = db_session.query(Produto).filter(Produto.name == name, Produto.ordem == existing_order).first()
    db_row.ordem = new_order
    db_session.commit()
    db_session.close()
    
def set_product_order_placeholder(db_session: Session, name: str, existing_order: str, placeholder: str):
    db_row = db_session.query(Produto).filter(Produto.name == name, Produto.ordem == existing_order).first()
    db_row.ordem = placeholder
    db_session.commit()
    db_session.close()
    
# def switch_editing_product_order(db_session: Session, name: str, editing_name: str, existing_order: str,
#                                  editing_order: str):
#     placeholder = '-'
#     print(f'{name}{existing_order}   ---    {editing_name}{editing_order}')
#     existing_row = db_session.query(Produto).filter_by(name = name, ordem = existing_order).first()
#     existing_row.ordem = placeholder
    
#     editing_row = db_session.query(Produto).filter(Produto.name == editing_name, Produto.ordem == editing_order).first()
#     editing_row.ordem = existing_order
#     existing_row.ordem = editing_order
    
#     db_session.commit()
#     db_session.close()
    
def get_product_by_name_and_category(db_session: Session, name: str, category: str):
    category_id = get_category_id_by_name(db_session, category)
    db_produto = db_session.query(Produto).filter_by(name = name, cat_id = category_id).first()
    if db_produto:
        order = int(db_produto.ordem[len(category):])
        iva_type = get_iva_value_and_name_by_id(db_session, db_produto.iva_id)
        iva_tag = f"{iva_type[0]} ({iva_type[1]}%)"
        produto = dict(name = db_produto.name,
                    price = str(db_produto.price),
                    order = order,
                    iva_type = iva_tag,
                    description = db_produto.description)
        return produto
    else:
        return None
    
def edit_product_values(db_session: Session, prod_id: int, values: dict):
    product = db_session.query(Produto).filter_by(prod_id = prod_id).first()
    iva_value = get_iva_value_by_id(db_session, values['iva_id'])
    iva_price = set_iva_price(values['price'], values['iva_checkbox'], iva_value)
    
    if product.name != values['name']:
        product.name = values['name']
        
    if values['iva_checkbox']:
        if product.price != values['price']:
            product.price = values['price']
            product.price_withouth_iva = iva_price
    else:
        if product.price_withouth_iva != values['price']:
            product.price_withouth_iva = values['price']
            product.price = iva_price
    
    if product.cat_id != values['cat_id']:
        product.cat_id = values['cat_id']
        
    if product.iva_id != values['iva_id']:
        product.iva_id = values['iva_id']
        
    if product.ordem != values['ordem']:
        product.ordem = values['ordem']
 
    if product.description != values['description']:
        product.description = values['description']
    
    db_session.commit()
    db_session.close()
    
def get_product_id_by_name_and_category(db_session: Session, name: str, category: str):
    category_id = get_category_id_by_name(db_session, category)
    product_id = db_session.query(Produto).filter_by(name = name, cat_id = category_id).value(Produto.prod_id)
    return product_id
    
        
# ###
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