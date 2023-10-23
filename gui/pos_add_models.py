from PyQt6.QtWidgets import (QVBoxLayout, QGridLayout, QHBoxLayout, QLabel, QCheckBox, QTableWidget, QSpinBox)
from PyQt6.QtCore import Qt
from database.pos_crud_and_validations import (create_db_category, validate_category_name, get_categories_list, create_db_tipo_iva,
                               validate_iva_input, get_iva_types_list, get_iva_value_by_name, remove_iva_by_name,
                               change_iva_by_name, validate_iva_name, validate_iva_value, get_tipo_iva_list,
                               remove_category_by_name, change_category_by_name, get_category_description_by_name,
                               validate_product_inputs, get_product_iva_type, get_product_category, create_db_product,
                               dec)
from database.mysql_engine import session

from gui.pos_custom_widgets import (POSDialog, SetEditOptionsWindow, MessageWindow, MissingValueWindow, open_new_window,
                                    RoundedButton, HighOptionsButton, RoundedLeftLineEdit, RoundedComboBox)

class AddUserWindow(POSDialog):
    def set_widgets_placements(self):
        self.setGeometry(200, 200, 450, 230)
        self.setWindowTitle('Adicionar Utilizador')
        add_user_layout = QVBoxLayout()
        self.setLayout(add_user_layout)
        
        add_user_fields_layout = QGridLayout()
        add_user_buttons_layout = QHBoxLayout()
        add_user_layout.addLayout(add_user_fields_layout)
        add_user_layout.addLayout(add_user_buttons_layout)
        
        add_user_name_label = QLabel('Nome:')
        self.add_user_name_line_edit = RoundedLeftLineEdit()
        add_user_username_label = QLabel('Username:')
        self.add_user_username_line_edit = RoundedLeftLineEdit()
        self.add_user_admin_check_box = QCheckBox('Privilégios de Administração')
        add_user_password_label = QLabel('Password')
        self.add_user_password_line_edit = RoundedLeftLineEdit()
        add_user_confirm_password_label = QLabel('Confirmar Password')
        self.add_user_confirm_password_line_edit = RoundedLeftLineEdit()
        add_user_create_button = HighOptionsButton('Criar Utilizador')
        add_user_close_button = HighOptionsButton('Fechar')
        
        add_user_name_label.setFixedWidth(120)
        add_user_username_label.setFixedWidth(120)
        add_user_password_label.setFixedWidth(120)
        add_user_confirm_password_label.setFixedWidth(120)
        
        add_user_fields_layout.addWidget(add_user_name_label, 0, 0)
        add_user_fields_layout.addWidget(self.add_user_name_line_edit, 0, 1)
        add_user_fields_layout.addWidget(add_user_username_label, 1, 0)
        add_user_fields_layout.addWidget(self.add_user_username_line_edit, 1, 1)
        add_user_fields_layout.addWidget(self.add_user_admin_check_box, 2, 0, 1, 2)
        add_user_fields_layout.addWidget(add_user_password_label, 3, 0)
        add_user_fields_layout.addWidget(self.add_user_password_line_edit, 3, 1)
        add_user_fields_layout.addWidget(add_user_confirm_password_label, 4, 0)
        add_user_fields_layout.addWidget(self.add_user_confirm_password_line_edit, 4, 1)
        add_user_buttons_layout.addWidget(add_user_create_button)
        add_user_buttons_layout.addWidget(add_user_close_button)
        
        add_user_close_button.clicked.connect(lambda: self.close())

class ProductWindow(POSDialog):
    def __init__(self, category_list: list, iva_list: list, product_name = None, product_price = None,
                 product_iva_cb = None, product_order = None, product_iva_type = None, product_category = None,
                 product_description = None):
        self.product_name = product_name
        self.product_price = product_price
        self.product_iva_cb = product_iva_cb
        self.product_order = product_order
        self.product_iva_type = product_iva_type
        self.product_category = product_category
        self.product_description = product_description
        self.edit_check = False
        
        self.category_list = category_list
        self.iva_list = iva_list
        super(ProductWindow, self).__init__()
        
    def set_widgets_placements(self):
        self.setGeometry(200, 200, 500, 200)
        self.setWindowTitle('Adicionar Produto')
                
        product_layout = QVBoxLayout()
        self.setLayout(product_layout)

        product_fields_layout = QGridLayout()
        product_buttons_layout = QHBoxLayout()
        product_layout.addLayout(product_fields_layout)
        product_layout.addLayout(product_buttons_layout)
        
        product_name_label = QLabel("Nome:")
        self.product_name_line_edit = RoundedLeftLineEdit()
        product_price_label = QLabel("Preço:")
        self.product_price_line_edit = RoundedLeftLineEdit()
        self.product_set_iva_check_box = QCheckBox("Preço c/ IVA")
        product_order_label = QLabel('Ordem:')
        self.product_order_spin_box = QSpinBox()
        product_iva_label = QLabel("Cateogira de IVA:")
        self.product_iva_combo_box = RoundedComboBox()
        product_category_label = QLabel("Categoria:")
        self.product_category_combo_box = RoundedComboBox()
        product_description_label = QLabel("Descrição")
        self.product_description_line_edit = RoundedLeftLineEdit()
        self.product_create_button = HighOptionsButton('Adicionar Produto')
        self.product_close_button = HighOptionsButton('Fechar')
        
        product_name_label.setFixedWidth(120)
        product_price_label.setFixedWidth(120)
        product_order_label.setFixedWidth(120)
        product_iva_label.setFixedWidth(120)
        product_category_label.setFixedWidth(120)
        product_description_label.setFixedWidth(120)
        product_description_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.product_set_iva_check_box.setChecked(True)
        self.product_order_spin_box.setFixedWidth(60)
        self.product_order_spin_box.setMinimum(1)
        self.product_order_spin_box.setMaximum(1000)
        self.product_order_spin_box.setValue(10)
        
        for category in self.category_list:
            self.product_category_combo_box.addItem(category)
        
        for iva_type in self.iva_list:
            iva_value = get_iva_value_by_name(session, iva_type)
            self.product_iva_combo_box.addItem(f"{iva_type} ({iva_value}%)")
                        
        product_fields_layout.addWidget(product_name_label, 0, 0)
        product_fields_layout.addWidget(self.product_name_line_edit, 0, 1, 1, 3)
        product_fields_layout.addWidget(product_price_label, 1, 0)
        product_fields_layout.addWidget(self.product_price_line_edit, 1, 1, 1, 3)
        product_fields_layout.addWidget(self.product_set_iva_check_box, 2, 0)
        product_fields_layout.addWidget(product_order_label, 2, 1, 1, 3, Qt.AlignmentFlag.AlignRight)
        product_fields_layout.addWidget(self.product_order_spin_box, 2, 2, 1, 2, Qt.AlignmentFlag.AlignRight)
        product_fields_layout.addWidget(product_iva_label, 3, 0)
        product_fields_layout.addWidget(self.product_iva_combo_box, 3, 1, 1, 3)
        product_fields_layout.addWidget(product_category_label, 4, 0)
        product_fields_layout.addWidget(self.product_category_combo_box, 4, 1, 1, 3)
        product_fields_layout.addWidget(product_description_label, 5, 0)
        product_fields_layout.addWidget(self.product_description_line_edit, 5, 1, 1, 3)
        product_buttons_layout.addWidget(self.product_create_button)
        product_buttons_layout.addWidget(self.product_close_button)
        
        self.product_create_button.clicked.connect(self.create_product)
        self.product_close_button.clicked.connect(self.close)   
        
        self.check_if_edit()
        
    def check_if_edit(self):
        if self.product_name is None:
            pass
        else:
            self.product_name_line_edit.setText(self.product_name)
            self.product_price_line_edit.setText(self.product_price)
            self.product_set_iva_check_box.setChecked(self.product_iva_cb)
            self.product_order_spin_box.setValue(self.product_order)
            self.product_iva_combo_box
            self.product_category_combo_box
            self.product_description_line_edit.setText(self.product_description)
            self.product_create_button.setText('Editar Produto')
            self.edit_check = True
            
    def create_product(self):
        name = self.product_name_line_edit.text()
        price = self.product_price_line_edit.text()
        iva_checkbox = self.product_set_iva_check_box.isChecked()
        order_num = self.product_order_spin_box.value()
        iva_type = self.product_iva_combo_box.currentText()
        category = self.product_category_combo_box.currentText()
        description = self.product_description_line_edit.text()
        
        iva_type = iva_type.split(' ')[0]
        iva_value = get_iva_value_by_name(session, iva_type)
        try:
            price = dec(price)
        except:
            pass
        
        messages = validate_product_inputs(session, name, category, price)
        if not messages:
            create_db_product(session, name, price, category, iva_value, order_num, description,
                              iva_checkbox)
            message_title = 'Produto Criado'
            message_content = [f'Criado produto {name} em {category}']
            message_window = MessageWindow(message_title, message_content)
            open_new_window(message_window)
        else:
            message_title = "Erro de Inserção"
            message_window = MessageWindow(message_title, messages)
            open_new_window(message_window)

class EditRemoveProdutcsWindow(POSDialog):
    def set_widgets_placements(self):
        self.setGeometry(200, 200, 500, 200)
        self.setWindowTitle('Editar/Remover Categoria/Produto')
        
        edit_rem_cat_pro_layout = QVBoxLayout()
        self.setLayout(edit_rem_cat_pro_layout)
        
        cat_prod_fields_layout = QGridLayout()
        edit_rem_cat_pro_button_layout = QHBoxLayout()
        edit_rem_cat_pro_layout.addLayout(cat_prod_fields_layout)
        edit_rem_cat_pro_layout.addLayout(edit_rem_cat_pro_button_layout)
        
        category_label = QLabel('Categoria:')
        self.category_combo_box = RoundedComboBox()
        products_label = QLabel('Produtos:')
        produts_table = QTableWidget()
        product_edit_button = RoundedButton('Editar Produto')
        product_remove_button = RoundedButton('Remover Produto')
        edit_rem_close_button = HighOptionsButton('Fechar')
        

        product_edit_button.setFixedSize(140, 22)
        product_remove_button.setFixedSize(140, 22)
        
        cat_prod_fields_layout.addWidget(category_label, 0, 0)
        cat_prod_fields_layout.addWidget(self.category_combo_box, 0 ,1)
        cat_prod_fields_layout.addWidget(products_label, 1, 0, 1, 2)
        cat_prod_fields_layout.addWidget(produts_table, 2, 0, 1, 2)
        cat_prod_fields_layout.addWidget(product_edit_button, 3, 0, alignment = Qt.AlignmentFlag.AlignCenter)
        cat_prod_fields_layout.addWidget(product_remove_button, 3, 1, alignment = Qt.AlignmentFlag.AlignCenter)
        edit_rem_cat_pro_button_layout.addWidget(edit_rem_close_button)
        
        edit_rem_close_button.clicked.connect(self.close)
            
class SetEditCategoryWindow(SetEditOptionsWindow):
    def __init__(self):
        self.first_title_label_text = 'Designação'
        self.second_title_label_text = 'Descrição'
        self.get_types_list = get_categories_list
        self.get_value_by_name = get_category_description_by_name
        self.change_by_name = change_category_by_name
        self.remove_by_name = remove_category_by_name
        super(SetEditCategoryWindow, self).__init__()
        self.setWindowTitle = 'Adicionar Categoria'
        self.setGeometry(200, 200, 700, 100)
    
    def create_type(self):
        name = self.first_line_edit.text()
        description = self.second_line_edit.text()
        
        messages = validate_category_name(session, name)
        if not messages:
            create_db_category(session, name, description)
            message_title = 'Categoria Criada'
            message_content = [f'Criada categoria {name}']
            message_window = MessageWindow(message_title, message_content)
            open_new_window(message_window)
            self.first_line_edit.clear()
            self.second_line_edit.clear()
            self.remove_listing()
            self.remove_listing()
            self.set_types_list()
        else:
            message_title = "Nome de Categoria"
            message_window = MessageWindow(message_title, messages)
            open_new_window(message_window)
            self.first_line_edit.clear()
            
    def validate_row(self, name:str , new_name: str, value: str, new_value: str):
        messages = []
        if name == new_name and value == new_value:
            messages.append('Não foram realizadas alterações')
        elif len(new_name) == 0 or new_name.isspace():
            messages.append('Nome de Categoria não pode estar vazio')
        return messages

class SetEditIVAWindow(SetEditOptionsWindow):
    def __init__(self):
        self.first_title_label_text = 'Designação'
        self.second_title_label_text = 'Taxa (%)'
        self.get_types_list = get_iva_types_list
        self.get_value_by_name = get_iva_value_by_name
        self.change_by_name = change_iva_by_name
        self.remove_by_name = remove_iva_by_name
        super(SetEditIVAWindow, self).__init__()
        self.setWindowTitle = 'Adicionar Taxa de IVA'
        self.setGeometry(200, 200, 500, 100)
        
    def create_type(self):
        name = self.first_line_edit.text()
        value = self.second_line_edit.text()
        try:
            value = int(value)
        except:
            pass
        
        messages = validate_iva_input(session, name, value)
        
        if not messages:
            create_db_tipo_iva(session, name, value)
            message_title = 'Designação Criada'
            message_content = [f'Criada Designação de IVA {name} com Taxa de {value}%']
            message_window = MessageWindow(message_title, message_content)
            open_new_window(message_window)
            self.first_line_edit.clear()
            self.second_line_edit.clear()
            self.remove_listing()
            self.remove_listing()
            self.set_types_list()
        else:
            message_title = "Erro de Inserção"
            message_window = MessageWindow(message_title, messages)
            open_new_window(message_window)
            self.first_line_edit.clear()
            self.second_line_edit.clear()
 
    def validate_row(self, iva_name:str , new_name: str, value: str, new_value: str):
        messages = []
        if (iva_name == new_name) and (value != new_value):
            try:
                new_value = int(new_value)
            except:
                pass
            value_message = validate_iva_value(session, new_value)
            if value_message:
                messages.extend(value_message)   
        elif (value == new_value) and (iva_name != new_name):
            name_message = validate_iva_name(session, new_name)
            if name_message:
                messages.extend(name_message)
        elif (value != new_value) and (iva_name != new_name):
            try:
                new_value = int(new_value)
            except:
                pass
            fields_message = validate_iva_input(session, new_name, new_value)
            if fields_message:
                messages.extend(fields_message)
        else:
            messages.append("Não foram realizadas alterações")
        return messages

def open_AddProductWindow():
    category_list = get_categories_list(session)
    iva_list = get_tipo_iva_list(session)
    if category_list and iva_list:
        add_product = ProductWindow(category_list, iva_list) 
        open_new_window(add_product)
    elif iva_list and not category_list:
        title = "Sem Categorias"
        message = "É necessário Categorias para adicionar Produto.\nCriar Categoria?"
        button_title = "Criar Categoria"
        new_window = MissingValueWindow(title, message, button_title, SetEditCategoryWindow())
        open_new_window(new_window)
    elif category_list and not iva_list:
        title = "Sem Taxas de IVA"
        message = "É necessário Taxas de IVA para adicionar Produto.\nCriar Taxa de IVA?"
        button_title = "Criar Taxa de IVA"
        new_window = MissingValueWindow(title, message, button_title, SetEditIVAWindow())
        open_new_window(new_window)
    else:
        title = "Campos em Falta"
        message = "É necessário Categorias e Taxas de IVA para adicionar Produto.\n\nCriar Categoria/Taxa de IVA?"
        button_title = "Criar Categoria"
        second_button_title = "Criar Taxa de IVA"
        new_window = MissingValueWindow(title, message, button_title, SetEditCategoryWindow(), second_button_title, SetEditIVAWindow())
        open_new_window(new_window)
        


        
        
        
        
        
        
        