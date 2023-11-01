from sqlalchemy.orm import Session
from sqlalchemy import asc, func

from database.pos_models import (Categoria, TipoIVA, Produto, Utilizador, Transacoes,
                                 ProdutosVendidos)
from decimal import Decimal as dec
import bcrypt

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
        messages = [f"Nome de categoria não pode estar vazio!"]
        return messages
    
    name = db_session.query(Categoria).filter(Categoria.cat_name == category_name).first()
    if name:
        messages = [f"Já existe uma categoria {category_name}!"]
        db_session.close()
        return messages
    db_session.close()
    
def get_categories_list(db_session: Session):
    category_names = db_session.query(Categoria.cat_name).all()
    categories = [category[0] for category in category_names]
    db_session.close()
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
    db_session.close()
    return description

def get_category_id_by_name(db_session: Session, name: str):
    cat_id = db_session.query(Categoria).filter(Categoria.cat_name == name).value(Categoria.cat_id)
    db_session.close()
    return cat_id

def get_amount_products_in_category(db_session: Session, category: str):
    category_id = get_category_id_by_name(db_session, category)
    products = db_session.query(Produto).filter(Produto.cat_id == category_id).order_by(Produto.ordem).all()
    
    product_items = {}
    
    for prod in products:
        iva_value = str(get_iva_value_by_id(db_session, prod.iva_id)) + '%'
        order = prod.ordem[len(category):]
        product_items[prod.prod_id] = [order, prod.name ,str(prod.price), iva_value]
        
    db_session.close()
    return product_items
    
    
    
###
###
### IVA
###
###
def get_tipo_iva_list(db_session: Session):
    iva_names = db_session.query(TipoIVA.iva_description).all()
    iva_list = [iva[0] for iva in iva_names]
    db_session.close()
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
        db_session.close()
        return messages
    db_session.close()
    
def validate_iva_name(db_session: Session, iva_name: str):
    messages = []
    name = db_session.query(TipoIVA).filter(TipoIVA.iva_description == iva_name).first()
    if len(iva_name) == 0 or iva_name.isspace():
        messages.append("Campo Designação não pode estar vazio!")
    if name:
        messages.append(f"Já existe uma designação {iva_name}!")
    db_session.close()
    return messages

def validate_iva_value(db_session: Session, value: int):
    messages = []
    iva_value = db_session.query(TipoIVA).filter(TipoIVA.iva_value == value).first()
    if not isinstance(value, int):
        messages.append("O campo Taxa é um valo inteiro!")
    elif value <0 or value >100:
        messages.append("Taxa têm de ser entre 0 e 100%!")
    elif iva_value:
        messages.append(f"Já existe uma Taxa de {value}%!")
    db_session.close()
    return messages
        
def get_iva_id(db_session: Session, value: int):
    iva_id = db_session.query(TipoIVA).filter(TipoIVA.iva_value == value).value(TipoIVA.iva_id)
    db_session.close()
    return iva_id
    
def get_iva_value_by_name(db_session: Session, iva_name: str):
    iva_value = db_session.query(TipoIVA).filter(TipoIVA.iva_description == iva_name).value(TipoIVA.iva_value)
    db_session.close()
    return iva_value

def get_iva_value_by_id(db_session: Session, iva_id: int):
    iva_value = db_session.query(TipoIVA).filter(TipoIVA.iva_id == iva_id).value(TipoIVA.iva_value)
    db_session.close()
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
    db_session.close()
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
    db_session.close()
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
        messages.append("Campo Nome não pode estar vazio!")
    if name:
        messages.append(f"Já existe uma designação {product_name} em {category}!")
    db_session.close()
    return messages

def validate_product_edit_name(product_name: str):
    messages = []
    if len(product_name) == 0 or product_name.isspace():
        messages.append("Campo Nome não pode estar vazio")
    return messages
    
def validate_product_price(price: dec):
    messages = []
    if not isinstance(price, dec):
        messages.append("O campo Preço é um valor númerico!")
    elif price < 0:
        messages.append("Preço necessita de ser maior que 0!")
    return messages

def get_product_order(db_session: Session, order: int, category: str):
    order_name = category + str(order)
    existing_order = db_session.query(Produto).filter(Produto.ordem == order_name).value(Produto.ordem)
    if not existing_order:
        order_num = None
        db_session.close()
        return order_num
    else:
        db_session.close()
        return order
  
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
    db_session.close()
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
    db_session.close()
    return name
    
def switch_product_order(db_session: Session, name: str, existing_order: str, new_order: str):
    db_row = db_session.query(Produto).filter(Produto.name == name, Produto.ordem == existing_order).first()
    db_row.ordem = new_order
    db_session.merge(db_row)
    db_session.commit()
    db_session.close()

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
        db_session.close()
        return produto
    else:
        db_session.close()
        return None
    
def edit_product_values(db_session: Session, values: dict):
    product = db_session.query(Produto).filter_by(prod_id = values['prod_id']).first()
    iva_value = get_iva_value_by_id(db_session, values['iva_id'])
    iva_price = set_iva_price(values['price'], values['iva_checkbox'], iva_value)
    
    if product.name != values['name']:
        product.name = values['name']
        db_session.merge(product)

    if values['iva_checkbox']:
        if product.price != values['price']:
            product.price = values['price']
            product.price_withouth_iva = iva_price
            db_session.merge(product)
    else:
        if product.price_withouth_iva != values['price']:
            product.price_withouth_iva = values['price']
            product.price = iva_price
            db_session.merge(product)

    if product.cat_id != values['cat_id']:
        product.cat_id = values['cat_id']
        db_session.merge(product)
  
    if product.iva_id != values['iva_id']:
        product.iva_id = values['iva_id']
        db_session.merge(product)
        
    if product.ordem != values['ordem']:
        product.ordem = values['ordem']
        db_session.merge(product)

    if product.description != values['description']:
        product.description = values['description']
        db_session.merge(product)
        
    db_session.commit()
    db_session.close()
    
def get_product_id_by_name_and_category(db_session: Session, name: str, category: str):
    category_id = get_category_id_by_name(db_session, category)
    product_id = db_session.query(Produto).filter_by(name = name, cat_id = category_id).value(Produto.prod_id)
    db_session.close()
    return product_id

def reorder_products_order(db_session: Session, category: str, order: int):
    order_name = category + str(order + 1)
    category_id = get_category_id_by_name(db_session, category)
    products = db_session.query(Produto).filter(Produto.cat_id == category_id,
                                                Produto.ordem >= order_name).order_by(Produto.ordem).all()
        
    for prod in products:
        order_name = category + str(order)
        prod.ordem = order_name
        db_session.merge(prod)
        order += 1
        
    db_session.commit() 
    db_session.close()
    
def remove_product_by_order_name(db_session: Session, order_name: str):
    product =  db_session.query(Produto).filter_by(ordem = order_name).first()
    db_session.delete(product)
    db_session.commit()
    db_session.close()
        
# ###
###
### Utilizador
###
###

def validate_add_user_input(db_session: Session, name: str, username: str, password = None, confirm = None):
    messages = []
    
    name_list = validate_user_name(name)
    if name_list:
        messages.extend(name_list)
        
    username_list = validate_add_user_username(db_session, username)
    if username_list:
        messages.extend(username_list)
    
    if password:
        password_list = validate_user_password(password, confirm)
        messages.extend(password_list)
        
    if messages:
        return messages
      
def validate_user_name(name):
    messages = []
    if len(name) == 0 or name.isspace():
        messages.append("Campo Nome não pode estar vazio!")
    return messages
    
def validate_add_user_username(db_session: Session, username: str):
    messages = []
    
    if len(username) == 0 or username.isspace():
        messages.append("Campo Username não pode estar vazio!")
        
    user_row = db_session.query(Utilizador).filter_by(username = username).first()
    if user_row:
        messages.append(f"Já existe um Username! {username}")
        
    db_session.close()
    return messages

def validate_edit_user_username(username: str):
    messages = []
    
    if len(username) == 0 or username.isspace():
        messages.append("Campo Username não pode estar vazio!")
    return messages

def validate_edit_user_input(name: str, username: str, password: str, confirm: str):
    messages = []
    
    name_list = validate_user_name(name)
    if name_list:
        messages.extend(name_list)
        
    username_list = validate_edit_user_username(username)
    if username_list:
        messages.extend(name_list) 
        
    password_list = validate_user_password(password, confirm)
    if password_list:
        messages.extend(password_list)
        
    return messages

def validate_user_password(password: str, confirm: str):
    messages = []
    if password != confirm:
        messages.append(f"Password não coincide!")
    return messages

def create_hash_password(password: str):
    password = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_password

def verify_hashed_password(password: str, hashed_password: str):
    password = password.encode('utf-8')
    hashed_password = hashed_password.encode('utf-8')
    messages = []
    if bcrypt.checkpw(password, hashed_password):
        return messages
    else:
        messages.append('Password Incorreta!')
        return messages
    
def create_db_user(db_session: Session, name: str, username: str, check_active: bool,
                   check_admin: bool, password = None):
    if check_admin:
        db_user = Utilizador(name = name, username = username, admin = check_admin, password = password, ativo = check_active)
    else:
        db_user = Utilizador(name = name, username = username, admin = check_admin, ativo = check_active)
        
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)
    db_session.close()
    
def edit_db_user(db_session: Session, user_id: int, name: str, username: str, check_active: bool,
                   check_admin: bool, password = None, check_previous_admin = None):
    db_user = db_session.query(Utilizador).filter_by(user_id = user_id).first()
    if check_admin:
        db_user.name = name
        db_user.username = username
        db_user.admin = check_admin
        if password:
            db_user.password = password
        db_user.ativo = check_active
    else:
        if check_previous_admin:
            db_user.password = ''
        db_user.name = name
        db_user.username = username
        db_user.admin = check_admin
        db_user.ativo = check_active
    
    db_session.merge(db_user)
    db_session.commit()
    db_session.close()
    
def get_users_dict(db_session: Session):
    users = db_session.query(Utilizador).all()
    user_dict = {}
    for user in users:
        user_dict[user.user_id] = [user.name, user.username]
    
    db_session.close()

    return user_dict
    
def get_user_by_username(db_session: Session, username: str):
    user = db_session.query(Utilizador).filter_by(username = username).first()
    user_dict = {'user_id' : user.user_id, 'name' : user.name, 'username' : username, 'admin' : user.admin,
                 'password' : user.password, 'ativo' : user.ativo}
    db_session.close()
    return user_dict

def check_if_admin_by_id(db_session: Session, user_id: int):
    admin_check = db_session.query(Utilizador).filter_by(user_id = user_id).value(Utilizador.admin)
    db_session.close()
    return admin_check

def check_if_admin_by_username(db_session: Session, username: str):
    admin_check = db_session.query(Utilizador).filter_by(username = username).value(Utilizador.admin)
    db_session.close()
    return admin_check

def check_if_user_exists(db_session: Session, user_id: int):
    user_check = db_session.query(Utilizador).filter_by(user_id = user_id).value(Utilizador.name)
    db_session.close()
    return user_check

def remove_db_user(db_session: Session, user_id: int):
    db_user = db_session.query(Utilizador).filter_by(user_id = user_id).first()
    db_session.delete(db_user)
    db_session.commit()
    db_session.close()
    
def check_users_exist(db_session: Session):
    users = db_session.query(Utilizador).all()
    if users:
        return True
    else:
        return False
    
def get_users_usernames(db_session: Session):
    users = db_session.query(Utilizador).all()
    usernames = []
    for user in users:
        usernames.append(user.username)
    db_session.close()
    return usernames

def get_user_password_by_username(db_session: Session, username: str):
    password = db_session.query(Utilizador).filter_by(username = username).value(Utilizador.password)
    return password
    
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