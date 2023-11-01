from PyQt6.QtWidgets import (QVBoxLayout, QGridLayout, QHBoxLayout, QLabel, QCheckBox, QSpinBox)
from PyQt6.QtCore import Qt
from database.pos_crud_and_validations import (create_db_category, validate_category_name, get_categories_list, create_db_tipo_iva,
                               validate_iva_input, get_iva_value_by_name, remove_iva_by_name, change_iva_by_name, validate_iva_name,
                               validate_iva_value, get_tipo_iva_list, remove_category_by_name, change_category_by_name,
                               get_category_description_by_name, validate_add_product_inputs, create_db_product, get_last_product_order,
                               get_product_order, get_product_name_by_category_and_order, switch_product_order,
                               get_category_id_by_name, get_iva_id, validate_add_user_input, create_hash_password, create_db_user,
                               get_users_dict, get_user_by_username, edit_db_user, validate_edit_user_input, check_if_admin_by_id,
                               remove_db_user, check_if_user_exists, check_users_exist, dec)
from database.mysql_engine import session
from gui.pos_custom_widgets import (POSDialog, SetEditOptionsWindow, MessageWindow, MissingValueWindow, open_new_window,
                                    HighOptionsButton, RoundedLeftLineEdit, RoundedComboBox, NewProductOrderWindow,
                                    MarginCheckBox, EditAdminStatusWindow, LargeThinButton, RemoveUserWindow)

class UserWindow(POSDialog):
    def __init__(self, title = 'Adicionar Utilizador', user_cb = 'Tornar Activo', create_button = 'Criar Utilizador',
                 edit = None, *args, **kwargs):
        self.title = title
        self.user_cb = user_cb
        self.create_button = create_button
        self.edit = edit
                        
        super(UserWindow, self).__init__(*args, **kwargs)
        
    def position_widget_fields(self):
        if self.edit:
            self.user_list_combo_box = RoundedComboBox()
            self.user_remove_user_button = LargeThinButton('Remover Utilizador')
            
            self.user_fields_layout.addWidget(self.user_list_combo_box, 0, 1)
            self.user_fields_layout.addWidget(self.user_name_label, 1, 0)
            self.user_fields_layout.addWidget(self.user_name_line_edit, 1, 1)
            self.user_fields_layout.addWidget(self.user_username_label, 2, 0)
            self.user_fields_layout.addWidget(self.user_username_line_edit, 2, 1)
            self.user_fields_layout.addWidget(self.user_active_check_box, 3, 0, 1, 2)
            self.user_fields_layout.addWidget(self.user_admin_check_box, 4, 0, 1, 2)
            self.user_fields_layout.addWidget(self.user_password_label, 5, 0)
            self.user_fields_layout.addWidget(self.user_password_line_edit, 5, 1)
            self.user_fields_layout.addWidget(self.user_confirm_password_label, 6, 0)
            self.user_fields_layout.addWidget(self.user_confirm_password_line_edit, 6, 1)
            self.user_buttons_layout.addWidget(self.user_create_button, 0, 0)
            self.user_buttons_layout.addWidget(self.user_remove_user_button, 0, 1)
            self.user_buttons_layout.addWidget(self.user_close_button, 1, 0, 1, 2, alignment = Qt.AlignmentFlag.AlignHCenter)
            
            self.set_combo_box()
            
            self.user_list_combo_box.setCurrentIndex(-1)
                        
            self.user_list_combo_box.currentIndexChanged.connect(self.set_edit_user_values)
            self.user_create_button.clicked.connect(self.edit_user)
            self.user_remove_user_button.clicked.connect(self.remove_user)
            
        else:    
            self.user_fields_layout.addWidget(self.user_name_label, 0, 0)
            self.user_fields_layout.addWidget(self.user_name_line_edit, 0, 1)
            self.user_fields_layout.addWidget(self.user_username_label, 1, 0)
            self.user_fields_layout.addWidget(self.user_username_line_edit, 1, 1)
            self.user_fields_layout.addWidget(self.user_active_check_box, 2, 0, 1, 2)
            self.user_fields_layout.addWidget(self.user_admin_check_box, 3, 0, 1, 2)
            self.user_fields_layout.addWidget(self.user_password_label, 4, 0)
            self.user_fields_layout.addWidget(self.user_password_line_edit, 4, 1)
            self.user_fields_layout.addWidget(self.user_confirm_password_label, 5, 0)
            self.user_fields_layout.addWidget(self.user_confirm_password_line_edit, 5, 1)
            self.user_buttons_layout.addWidget(self.user_create_button, 0, 0, 1, 2, alignment = Qt.AlignmentFlag.AlignHCenter)
            self.user_buttons_layout.addWidget(self.user_close_button, 1, 0, 1, 2, alignment = Qt.AlignmentFlag.AlignHCenter)
            
            self.user_create_button.clicked.connect(self.create_user)
        
    def set_widgets_placements(self):
        self.setGeometry(200, 200, 450, 230)
        self.setWindowTitle(self.title)
        user_layout = QVBoxLayout()
        self.setLayout(user_layout)
        
        self.user_fields_layout = QGridLayout()
        self.user_buttons_layout = QGridLayout()
        user_layout.addLayout(self.user_fields_layout)
        user_layout.addLayout(self.user_buttons_layout)
        
        self.user_name_label = QLabel('Nome:')
        self.user_name_line_edit = RoundedLeftLineEdit()
        self.user_username_label = QLabel('Username:')
        self.user_username_line_edit = RoundedLeftLineEdit()
        self.user_active_check_box = MarginCheckBox(self.user_cb)
        self.user_admin_check_box = MarginCheckBox('Privilégios de Administração')
        self.user_password_label = QLabel('Password')
        self.user_password_line_edit = RoundedLeftLineEdit()
        self.user_confirm_password_label = QLabel('Confirmar Password')
        self.user_confirm_password_line_edit = RoundedLeftLineEdit()
        self.user_create_button = LargeThinButton(self.create_button)
        self.user_close_button = HighOptionsButton('Fechar')
        
        self.user_name_label.setFixedWidth(120)
        self.user_username_label.setFixedWidth(120)
        self.user_password_label.setFixedWidth(120)
        self.user_confirm_password_label.setFixedWidth(120)

        self.user_admin_check_box.setChecked(False)
        self.user_active_check_box.setChecked(True)
        self.user_password_line_edit.setEchoMode(RoundedLeftLineEdit.EchoMode.Password)
        self.user_confirm_password_line_edit.setEchoMode(RoundedLeftLineEdit.EchoMode.Password)
        self.user_password_label.hide()
        self.user_password_line_edit.hide()
        self.user_confirm_password_label.hide()
        self.user_confirm_password_line_edit.hide()

        self.position_widget_fields()
        
        self.user_admin_check_box.stateChanged.connect(self.admin_checkbox_check)
        self.user_close_button.clicked.connect(self.close)
        
    def set_combo_box(self):
        self.user_list_combo_box.clear()
        combo_box_items = get_users_dict(session)
        if not combo_box_items:
            self.close()
        for key in combo_box_items.keys():
            label = f'{combo_box_items[key][0]} - {combo_box_items[key][1]}'
            self.user_list_combo_box.addItem(label)
                    
    def set_edit_user_values(self):
        if not self.user_list_combo_box.currentIndex() == -1:
            username = self.user_list_combo_box.currentText().split(' - ')[1]
            self.current_user_dict = get_user_by_username(session, username)
            self.user_name_line_edit.setText(self.current_user_dict['name'])
            self.user_username_line_edit.setText(self.current_user_dict['username'])
            
            if self.current_user_dict['admin']:
                self.user_admin_check_box.setChecked(True)
                self.user_password_label.show()
                self.user_password_line_edit.show()
                self.user_password_label.setText('Nova Password')
            else:
                self.user_admin_check_box.setChecked(False)
                self.user_password_label.hide()
                self.user_password_line_edit.hide()
                
            if self.current_user_dict['ativo']:
                self.user_active_check_box.setChecked(True)
            else:
                self.user_active_check_box.setChecked(False)
        
    def admin_checkbox_check(self):
        if self.user_admin_check_box.isChecked():
            self.user_password_label.show()
            self.user_password_line_edit.show()
            self.user_confirm_password_label.show()
            self.user_confirm_password_line_edit.show()
        else:
            self.user_password_label.hide()
            self.user_password_line_edit.hide()
            self.user_confirm_password_label.hide()
            self.user_confirm_password_line_edit.hide()

    def get_user_form_values(self):
        name = self.user_name_line_edit.text().strip()
        username = self.user_username_line_edit.text().strip()
        admin_check = self.user_admin_check_box.isChecked()
        active_check = self.user_active_check_box.isChecked()
        return name, username, admin_check, active_check

    def create_user(self):
        name, username, admin_check, active_check = self.get_user_form_values()
        
        if admin_check:
            password = self.user_password_line_edit.text().strip()
            confirm = self.user_confirm_password_line_edit.text().strip()
            messages = validate_add_user_input(session, name, username, password = password, confirm = confirm) 
        else:
            messages = validate_add_user_input(session, name, username)
            
        if not messages:
            if admin_check:
                hashed_password = create_hash_password(password)
                create_db_user(session, name, username, active_check, admin_check, hashed_password)
            else:
                create_db_user(session, name, username, active_check, admin_check)
            
            message_title = "Utilizador Criado"
            message_window = MessageWindow(message_title, [f'Criado Utilizador {username}!'])
            open_new_window(message_window)
            self.clear_user_window()
            
        else:
            self.error_message(messages)
            
    def edit_user(self):        
        name, username, admin_check, active_check = self.get_user_form_values()
        user_id = self.current_user_dict['user_id']
        admin_status = self.current_user_dict['admin']
        password = self.user_password_line_edit.text().strip()
        confirm_password = self.user_confirm_password_line_edit.text().strip()
        
        messages = validate_edit_user_input(name, username, password, confirm_password)
                        
        if not messages:  
            if admin_check:
                if password:
                    hashed_password = create_hash_password(password)
                    edit_db_user(session, user_id, name, username, active_check, admin_check, password = hashed_password)
                else:
                    edit_db_user(session, user_id, name, username, active_check, admin_check)
                self.sucess_edit_message(username)
            elif admin_status:
                if not messages:
                    self.previous_admin_edit_window(name, username, admin_check, active_check, user_id)
                    if not check_if_admin_by_id(session, user_id):
                        self.sucess_edit_message(username)
                        
            else:
                edit_db_user(session, user_id, name, username, active_check, admin_check)
                self.sucess_edit_message(username)
            self.clear_user_window()
        else:
            self.error_message(messages)
                
                
    def previous_admin_edit_window(self, name: str, username: str, admin_check: bool, active_check:bool,
                                   user_id: int):
        title = 'Mudança de Estatuto de Utilizador'
        message = f'O utilizador {username} deixará de ter privilégios de administração.'
        button_title = 'Continuar'
        
        window = EditAdminStatusWindow(name, username, admin_check, active_check, user_id, session,
                                       title, message, button_title, edit_db_user)      
        open_new_window(window)
        
    def sucess_edit_message(self, username: str):
        message_title = "Utilizador Editado"
        message = [f'Editado Utilizador {username}']
        message_window = MessageWindow(message_title, message)
        open_new_window(message_window)  
                       
    def error_message(self, messages: list):
        message_title = "Erro de Inserção"
        message_window = MessageWindow(message_title, messages)
        open_new_window(message_window)
        self.clear_password_input()
        
    def remove_user(self):
        user_id = self.current_user_dict['user_id']
        username = self.current_user_dict['username']
        title = 'Remoção de Utilizador'
        message = f'O utilizador {username} será eliminado!'
        button_title = 'Continuar'
        
        window = RemoveUserWindow(user_id, session, title, message, button_title, remove_db_user)
        open_new_window(window)
        
        if not check_if_user_exists(session, user_id):
            title = "Utilizador Removido"
            message = [f'Removido Utilizador {username}']
            message_window = MessageWindow(title, message)
            open_new_window(message_window)
            self.clear_user_window()     
                 
    def clear_user_window(self):
        try:
            self.set_combo_box()
            self.user_list_combo_box.setCurrentIndex(-1)
        except AttributeError:
            pass
        self.user_name_line_edit.setText('')
        self.user_username_line_edit.setText('')
        self.clear_password_input()
        self.user_admin_check_box.setChecked(False)
        
    def clear_password_input(self):
        self.user_password_line_edit.setText('')
        self.user_confirm_password_line_edit.setText('')
        try:
            self.user_new_password_line_edit.setText('')
        except AttributeError:
            pass
        
    
class ProductWindow(POSDialog):
    def __init__(self, category_list: list, iva_list: list):
                
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
        
        self.set_product_spinbox_values()
        
        self.product_create_button.clicked.connect(self.save_product)
        self.product_close_button.clicked.connect(self.close)
        self.product_category_combo_box.currentIndexChanged.connect(self.set_product_spinbox_values)
            
    def get_product_spinbox_last_order(self):
        category = self.product_category_combo_box.currentText()
        order = get_last_product_order(session, category)
        return order + 1

    def set_product_spinbox_values(self):
        order = self.get_product_spinbox_last_order()
        self.product_order_spin_box.setMinimum(1)
        self.product_order_spin_box.setMaximum(order)
        self.product_order_spin_box.setValue(order)
                
    def save_product(self):
        values = self.product_values_dict()
        
        order_num = self.product_order_spin_box.value()
        category = self.product_category_combo_box.currentText()        
        iva_value = int(self.product_iva_combo_box.currentText().split(' ')[1][1:-2])
        name = values['name']
        price = values['price']
        iva_checkbox = values['iva_checkbox']
        description = values['description']

        messages = validate_add_product_inputs(session, name, category, price)
        
        existing_order_num = get_product_order(session, order_num, category)
        if not messages and not existing_order_num:
            self.create_sequential_order_product(name, price, category, iva_value, order_num, description,
                            iva_checkbox)
            self.clear_product_window()
        elif not messages and existing_order_num:
            new_order_num = (get_last_product_order(session, category) + 1)
            existing_name = get_product_name_by_category_and_order(session, existing_order_num, category)
            self.set_product_order_window(category, existing_order_num, existing_name, new_order_num, name, price, iva_value,
                                        description, iva_checkbox)
            self.clear_product_window()
        else:
            message_title = "Erro de Inserção"
            message_window = MessageWindow(message_title, messages)
            open_new_window(message_window)
            self.clear_product_window()
            
    def product_values_dict(self):
        price = self.product_price_line_edit.text().strip()
        iva_value = int(self.product_iva_combo_box.currentText().split(' ')[1][1:-2])
        category = self.product_category_combo_box.currentText().strip()
        category_id = get_category_id_by_name(session, category)
        iva_id = get_iva_id(session, iva_value)
        order_name = category + str(self.product_order_spin_box.value())
        try:
            price = dec(price)
        except:
            pass
        try:
            product_id = self.product_id
        except:
            product_id = None

        values = dict(prod_id = product_id,
                      name = self.product_name_line_edit.text().strip(),
                      price = price,
                      iva_checkbox = self.product_set_iva_check_box.isChecked(),
                      cat_id = category_id,
                      iva_id = iva_id,
                      ordem = order_name,
                      description = self.product_description_line_edit.text().strip())
        return values
    
    def set_product_order_window(self, category: str, existing_order: int, existing_name: str, new_order: int,
                                 new_name: str, price: dec, iva_value: int, description: str, iva_checkbox: bool):
        title = 'Ordem Existente'
        message = (f'{existing_name} já ocupa a posição de ordenação {existing_order}.\nDeseja colocar {new_name} ' 
                   f'nessa posição e passar {existing_name} para a posição {new_order}?')
        button_title = f'Gravar {new_name}\nna posição\n{new_order}'
        additional_button_title = f'Gravar {new_name}\nna posição\n{existing_order}'
        
        window = NewProductOrderWindow(title = title, message = message, button_title = button_title,
                                       add_value_window = self.create_sequential_order_product,
                                       aditional_button_title = additional_button_title,
                                       add_aditional_window = self.create_switch_order_product, product_name = new_name,
                                       price = price, category = category, iva_value = iva_value, order_num = existing_order, 
                                       description = description, iva_checkbox = iva_checkbox, new_order_num = new_order,
                                       existing_product_name = existing_name)
        open_new_window(window)

    def create_sequential_order_product(self, name: str, price: dec, category: str, iva_value: int, order_num: int,
                          description: str, iva_checkbox: bool):
        create_db_product(session, name, price, category, iva_value, order_num, description, iva_checkbox)
        message_title = 'Produto Criado'
        message_content = [f'Criado produto {name} em {category}']
        message_window = MessageWindow(message_title, message_content)
        open_new_window(message_window)
        
    def create_switch_order_product(self, name: str, price: dec, category: str, iva_value: int, order_num: int,
                          description: str, iva_checkbox: bool, new_order_num: int, existing_name: str):
        order_name = category + str(order_num)
        new_order_name = category + str(new_order_num)
        switch_product_order(session, existing_name, order_name, new_order_name)
        self.create_sequential_order_product(name, price, category, iva_value, order_num, description, iva_checkbox)
        
    def clear_product_window(self):
        self.product_name_line_edit.setText('')
        self.product_price_line_edit.setText('')
        self.product_description_line_edit.setText('')
        self.set_product_spinbox_values()
                  
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
        name = self.first_line_edit.text().strip()
        description = self.second_line_edit.text().strip()
        
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
        self.get_types_list = get_tipo_iva_list
        self.get_value_by_name = get_iva_value_by_name
        self.change_by_name = change_iva_by_name
        self.remove_by_name = remove_iva_by_name
        super(SetEditIVAWindow, self).__init__()
        self.setWindowTitle = 'Adicionar Taxa de IVA'
        self.setGeometry(200, 200, 500, 100)
        
    def create_type(self):
        name = self.first_line_edit.text().strip()
        value = self.second_line_edit.text().strip()
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
        
def open_editable_UserWindow():
    title = 'Utilizador'
    user_cb = 'Ativo'
    create_button = 'Editar Utilizador'
    edit = check_users_exist(session)
    if not edit:
        no_users_window()
    else:   
        window = UserWindow(title = title, user_cb = user_cb, create_button = create_button,
                             edit = edit)
        open_new_window(window)

def no_users_window():
    title = 'Sem Utilizadores'
    message = 'Sem Utilizadore criados, criar Utilizador?'
    create_button = 'Criar Utilizador'
    user_window = UserWindow()
    window = MissingValueWindow(title, message, create_button, user_window)
    open_new_window(window)
        
        
        
        
        
        