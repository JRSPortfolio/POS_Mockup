from PyQt6.QtWidgets import (QVBoxLayout, QGridLayout, QHBoxLayout, QLabel, QCheckBox, QTableView, QSpinBox, QHeaderView)
from PyQt6.QtCore import Qt
from database.pos_crud_and_validations import (create_db_category, validate_category_name, get_categories_list, create_db_tipo_iva,
                               validate_iva_input, get_iva_value_by_name, remove_iva_by_name, change_iva_by_name, validate_iva_name,
                               validate_iva_value, get_tipo_iva_list, remove_category_by_name, change_category_by_name,
                               get_category_description_by_name, validate_add_product_inputs, create_db_product, get_last_product_order,
                               get_product_order, get_product_name_by_category_and_order, switch_product_order,
                               get_amount_products_in_category, get_product_by_name_and_category,
                               get_category_id_by_name, get_iva_id, edit_product_values, get_product_id_by_name_and_category,
                               validate_edit_product_inputs, reorder_products_order, remove_product_by_order_name,
                               get_product_by_order_name, dec)
from PyQt6.QtGui import QStandardItem
from database.mysql_engine import session

from gui.pos_custom_widgets import (POSDialog, SetEditOptionsWindow, MessageWindow, MissingValueWindow, open_new_window,
                                    RoundedButton, HighOptionsButton, RoundedLeftLineEdit, RoundedComboBox, NewProductOrderWindow,
                                    EditProductOrderWindow, TableSelectionUpButton, TableSelectionDownButton, ReadOnlyItemModel)

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
        self.add_user_password_label = QLabel('Password')
        self.add_user_password_line_edit = RoundedLeftLineEdit()
        self.add_user_confirm_password_label = QLabel('Confirmar Password')
        self.add_user_confirm_password_line_edit = RoundedLeftLineEdit()
        add_user_create_button = HighOptionsButton('Criar Utilizador')
        add_user_close_button = HighOptionsButton('Fechar')
        
        add_user_name_label.setFixedWidth(120)
        add_user_username_label.setFixedWidth(120)
        self.add_user_password_label.setFixedWidth(120)
        self.add_user_confirm_password_label.setFixedWidth(120)
        
        self.add_user_admin_check_box.setChecked(False)
        self.add_user_password_label.hide()
        self.add_user_password_line_edit.hide()
        self.add_user_confirm_password_label.hide()
        self.add_user_confirm_password_line_edit.hide()
        
        
        
        add_user_fields_layout.addWidget(add_user_name_label, 0, 0)
        add_user_fields_layout.addWidget(self.add_user_name_line_edit, 0, 1)
        add_user_fields_layout.addWidget(add_user_username_label, 1, 0)
        add_user_fields_layout.addWidget(self.add_user_username_line_edit, 1, 1)
        add_user_fields_layout.addWidget(self.add_user_admin_check_box, 2, 0, 1, 2)
        add_user_fields_layout.addWidget(self.add_user_password_label, 3, 0)
        add_user_fields_layout.addWidget(self.add_user_password_line_edit, 3, 1)
        add_user_fields_layout.addWidget(self.add_user_confirm_password_label, 4, 0)
        add_user_fields_layout.addWidget(self.add_user_confirm_password_line_edit, 4, 1)
        add_user_buttons_layout.addWidget(add_user_create_button)
        add_user_buttons_layout.addWidget(add_user_close_button)
        
        self.add_user_admin_check_box.stateChanged.connect(self.admin_checkbox_check)
        add_user_close_button.clicked.connect(self.close)
        
    def admin_checkbox_check(self):
        if self.add_user_admin_check_box.isChecked():
            self.add_user_password_label.show()
            self.add_user_password_line_edit.show()
            self.add_user_confirm_password_label.show()
            self.add_user_confirm_password_line_edit.show()
        else:
            self.add_user_password_label.hide()
            self.add_user_password_line_edit.hide()
            self.add_user_confirm_password_label.hide()
            self.add_user_confirm_password_line_edit.hide()

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

class EditProductWindow(ProductWindow):
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
        
        super(EditProductWindow, self).__init__(category_list, iva_list)
        self.set_edit_product_values()
        
    def set_edit_product_values(self):
        self.product_name_line_edit.setText(self.product_name)
        self.product_price_line_edit.setText(self.product_price)
        self.product_set_iva_check_box.setChecked(self.product_iva_cb)
        self.product_order_spin_box.setValue(self.product_order)
        self.product_iva_combo_box.setCurrentText(self.product_iva_type)
        self.product_category_combo_box.setCurrentText(self.product_category)
        self.product_description_line_edit.setText(self.product_description)
        self.product_create_button.setText('Editar Produto')
        self.product_id = get_product_id_by_name_and_category(session, self.product_name, self.product_category)
         
    def save_product(self):
        existing_order = self.product_order_spin_box.value()
        category = self.product_category_combo_box.currentText()
        values = self.product_values_dict()
        name = values['name']
        price = values['price']
        
        if category == self.product_category and name == self.product_name:
            messages = validate_edit_product_inputs(name, price)
        else:
            messages = validate_add_product_inputs(session, name, category, price)
        
        
        same_order_num = self.product_order == existing_order
                
        if not messages and category == self.product_category and same_order_num:
            self.edit_db_product(values, category)
            self.close()
        elif not messages and category == self.product_category and not same_order_num:
            existing_name = get_product_name_by_category_and_order(session, existing_order, category)
            self.set_product_edit_order_window(existing_order, existing_name, self.product_order, name,
                                                category, values)
            self.close()
        elif not messages and category != self.product_category:    
            self.edit_diferent_category_product(category, values)
            self.close()
        else:
            message_title = "Erro de Inserção"
            message_window = MessageWindow(message_title, messages)
            open_new_window(message_window)
            self.close()
                        
    def set_product_edit_order_window(self, existing_order: int, existing_name: str, new_order: int,
                                      new_name: str, category: str, values: dict):
        title = 'Ordem Existente'
        message = (f'{existing_name} já ocupa a posição de ordenação {existing_order}.\nDeseja colocar {new_name} ' 
                   f'nessa posição e passar {existing_name} para a posição {new_order}?')
        button_title = f'Gravar {new_name}\nna posição\n{new_order}'
        additional_button_title = f'Gravar {new_name}\nna posição\n{existing_order}'
        
        window = EditProductOrderWindow(title = title, message = message, button_title = button_title,
                                        add_value_window = self.edit_db_product, aditional_button_title = additional_button_title,
                                        add_aditional_window = self.edit_switch_order_product, existing_name = existing_name, 
                                        category = category, existing_order = existing_order, new_order = new_order,
                                        values = values)
        open_new_window(window)
        
    def edit_switch_order_product(self, existing_order, new_order, category: str, existing_name: str, values: dict):
        existing_order_name = category + str(existing_order)
        new_order_name = category + str(new_order)
        placeholder = '_'
                
        switch_product_order(session, existing_name, existing_order_name, placeholder)
        self.edit_db_product(values, category)
        switch_product_order(session, existing_name, placeholder, new_order_name)

    def edit_diferent_category_product(self, category: str, values: dict):
        last_order = self.get_product_spinbox_last_order()
        current_order = self.product_order_spin_box.value()
        
        if current_order == last_order:
            self.edit_db_product(values, category)
            reorder_products_order(session, self.product_category, self.product_order)
        else:
            existing_name = get_product_name_by_category_and_order(session, current_order, category)
            self.set_diferent_category_edit_window(current_order, last_order, category, self.product_category, existing_name,
                                                   values)
           
    def set_diferent_category_edit_window(self, current_order: int, new_order: int, current_category: str, 
                                          previous_category: str, existing_name: str, values: dict):
        name = values['name']
        title = 'Ordem Existente'
        message = (f'{existing_name} já ocupa a posição de ordenação {current_order}.\nDeseja colocar {name} ' 
                   f'nessa posição e passar {existing_name} para a posição {new_order}?')
        button_title = f'Gravar {name}\nna posição\n{new_order}'
        additional_button_title = f'Gravar {name}\nna posição\n{current_order}'
        self.different_category_check = True
        
        window = EditProductOrderWindow(title = title, message = message, button_title = button_title,
                                        add_value_window = self.edit_db_product,
                                        aditional_button_title = additional_button_title,
                                        add_aditional_window = self.edit_diferent_category_and_order_product,
                                        existing_name = existing_name, category = current_category, existing_order = self.product_order,
                                        new_order = new_order, values = values, previous_category = previous_category,
                                        check = self.different_category_check)
        open_new_window(window)
        
    def edit_diferent_category_and_order_product(self, current_order: int, new_order: int, current_category: str,
                                                 existing_name: str, values: dict, previous_category: str):     
        new_order_name = current_category + (str(new_order))
        switch_product_order(session, existing_name, values['ordem'], new_order_name)
        self.edit_db_product(values, current_category)
        reorder_products_order(session, previous_category, current_order)

    def edit_db_product(self, values: dict, category: str):
        edit_product_values(session, values)
        message_title = 'Produto Editado'
        message_content = [f'Editado produto {values['name']} em {category}']
        message_window = MessageWindow(message_title, message_content)
        open_new_window(message_window)
        
    def set_product_spinbox_values(self):
        order = self.get_product_spinbox_last_order()
        self.product_order_spin_box.setMinimum(1)
        
        if self.product_category == self.product_category_combo_box.currentText():
            self.product_order_spin_box.setMaximum(order - 1)
            self.product_order_spin_box.setValue(self.product_order)
        else:
            self.product_order_spin_box.setMaximum(order)
            self.product_order_spin_box.setValue(order)

class EditRemoveProdutcsWindow(POSDialog):
    def set_widgets_placements(self):
        self.setGeometry(200, 200, 700, 400)
        self.setWindowTitle('Editar/Remover Categoria/Produto')
        
        edit_rem_cat_pro_layout = QVBoxLayout()
        self.setLayout(edit_rem_cat_pro_layout)
        
        cat_prod_fields_layout = QGridLayout()
        products_table_layout = QGridLayout()
        edit_rem_cat_pro_button_layout = QHBoxLayout()
        edit_rem_cat_pro_layout.addLayout(cat_prod_fields_layout)
        edit_rem_cat_pro_layout.addLayout(products_table_layout)
        edit_rem_cat_pro_layout.addLayout(edit_rem_cat_pro_button_layout)
        
        category_label = QLabel('Categoria:')
        self.category_combo_box = RoundedComboBox()
        self.produts_table = QTableView()
        self.move_product_up_button = TableSelectionUpButton()
        self.move_product_down_button = TableSelectionDownButton()
        product_edit_button = RoundedButton('Editar Produto')
        product_remove_button = RoundedButton('Remover Produto')
        self.order_edit_button = RoundedButton('Re-Ordenar')
        edit_rem_close_button = HighOptionsButton('Fechar')
        
        product_edit_button.setFixedSize(140, 22)
        product_remove_button.setFixedSize(140, 22)
        self.order_edit_button.setFixedSize(140, 22)
        self.order_edit_button.setCheckable(True)
        
        self.produts_table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        
        category_list = get_categories_list(session)
        for category in category_list:
            self.category_combo_box.addItem(category)
        
        self.set_table_model()
        
        cat_prod_fields_layout.addWidget(category_label, 0, 0)
        cat_prod_fields_layout.addWidget(self.category_combo_box, 0 ,1)
        products_table_layout.addWidget(self.produts_table, 1, 0, 2, 3)
        products_table_layout.addWidget(self.move_product_up_button, 1, 3, alignment = Qt.AlignmentFlag.AlignVCenter)
        products_table_layout.addWidget(self.move_product_down_button, 2, 3, alignment = Qt.AlignmentFlag.AlignVCenter)
        products_table_layout.addWidget(product_edit_button, 3, 0, alignment = Qt.AlignmentFlag.AlignCenter)
        products_table_layout.addWidget(product_remove_button, 3, 1, alignment = Qt.AlignmentFlag.AlignCenter)
        products_table_layout.addWidget(self.order_edit_button, 3, 2, alignment = Qt.AlignmentFlag.AlignCenter)
        edit_rem_cat_pro_button_layout.addWidget(edit_rem_close_button)
        
        self.category_combo_box.currentIndexChanged.connect(self.table_category_change)
        self.move_product_up_button.clicked.connect(self.up_button_check)
        self.move_product_down_button.clicked.connect(self.down_button_check)
        product_edit_button.clicked.connect(self.edit_product_in_row)
        product_remove_button.clicked.connect(self.remove_product_row)
        self.order_edit_button.clicked.connect(self.unlock_ordering)
        edit_rem_close_button.clicked.connect(self.close)
        
        self.table_header = self.produts_table.horizontalHeader()
        self.table_header.setDisabled(True)
        self.table_header.sectionClicked.connect(self.set_order_by_header)
        
    def set_table_model(self):
        self.table_model = ReadOnlyItemModel()        
        self.category = self.category_combo_box.currentText().strip()
        
        headers = ['Produto', 'Preço', 'IVA', 'Ordem']
        contents = get_amount_products_in_category(session, self.category)
        
        self.row_number = len(contents.keys())
        
        self.table_model.setColumnCount(4)
        self.table_model.setRowCount(self.row_number)
        
        self.table_model.setHorizontalHeaderLabels(headers)
        
        row_counter = 0
        for key in contents.keys():
            for i in range(4):
                item = QStandardItem(contents[key][i])
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_model.setItem(row_counter, i, item)
            row_counter += 1
                
        self.produts_table.setModel(self.table_model)
        self.produts_table.verticalHeader().hide()
        self.produts_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        
        for col in range(len(headers)):
            self.produts_table.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)

        self.produts_table.show()

    def table_category_change(self):
        self.set_table_model()
        self.order_edit_button.setChecked(False)
        self.table_header.setDisabled(True)
        
    def up_button_check(self):
        if self.order_edit_button.isChecked():
            selection_order = self.move_product_up()
            self.set_table_model()
            if selection_order or selection_order == 0:
                self.produts_table.selectRow(selection_order)
        else:
            self.select_upper_row()

    def down_button_check(self):
        if self.order_edit_button.isChecked():
            selection_order = self.move_product_down()
            self.set_table_model()
            if selection_order or selection_order == 0:
                self.produts_table.selectRow(selection_order)
        else:
            self.select_down_row()
        
    def select_upper_row(self):
        row = self.get_selected_row_index()
        if row:
            if row == 0:
                row = self.row_number - 1
            else:
                row -= 1
            self.produts_table.selectRow(row)
        else:
            self.produts_table.selectRow(self.row_number - 1)
                
    def select_down_row(self):
        row = self.get_selected_row_index()
        if row or row == 0:
            if row == self.row_number - 1:
                row = 0
            else:
                row += 1   
            self.produts_table.selectRow(row)
        else:
            self.produts_table.selectRow(0)

    def move_product_up(self):
        order, order_name, product = self.get_moving_values()
        
        if order:
            order = int(order) - 1
            placeholder = '_'
            row_number = self.row_number - 1
            if order == 0:
                order = row_number
                index = self.table_model.index(row_number, 0)
                switching_product = self.table_model.itemFromIndex(index).text()
                new_order_name = self.category + str(self.row_number)
            else:
                order -= 1
                index = self.table_model.index(order, 0)
                switching_product = self.table_model.itemFromIndex(index).text()
                new_order_name = self.category + str(order + 1)
                                
            switch_product_order(session, switching_product, new_order_name, placeholder)
            switch_product_order(session, product, order_name, new_order_name)
            switch_product_order(session, switching_product, placeholder, order_name)

            return order
            
    def move_product_down(self):
        order, order_name, product = self.get_moving_values()
        if order:
            order = int(order) - 1
            placeholder = '_'
            row_number = self.row_number - 1
            if order == row_number:
                order = 0
                index = self.table_model.index(0, 0)
                switching_product = self.table_model.itemFromIndex(index).text()
                new_order_name = self.category + '1'
            else:
                order += 1
                index = self.table_model.index(order, 0)
                switching_product = self.table_model.itemFromIndex(index).text()
                new_order_name = self.category + str(order + 1)
            
            switch_product_order(session, switching_product, new_order_name, placeholder)
            switch_product_order(session, product, order_name, new_order_name)
            switch_product_order(session, switching_product, placeholder, order_name)
            
            return order 
           
    def get_moving_values(self):
        order = self.get_selected_order()
        product = self.get_selected_product()
        try:
            order_name = self.category + order
            return order, order_name, product
        except:
            return None, None, None
        
    def get_selected_order(self):
        rows = self.produts_table.selectionModel().selectedRows()
        if rows:
            row = rows[0].row()
            item = self.table_model.item(row, 3)
            order = item.text()
            return order
        else:
            return None

    def get_selected_row_index(self):
        rows = self.produts_table.selectionModel().selectedRows()
        if rows:
            index = rows[0]
            row = index.row()
            return row
        else:
            return None
        
    def get_selected_product(self):
        rows = self.produts_table.selectionModel().selectedRows()
        if rows:
            row = rows[0].row()
            item = self.table_model.item(row, 0)
            name = item.text()
            return name
        else:
            return None
        
    def edit_product_in_row(self):
        name = self.get_selected_product()
        if name:
            db_product = get_product_by_name_and_category(session, name, self.category)
            categories_list = get_categories_list(session)
            iva_list = get_tipo_iva_list(session)
            edit_window = EditProductWindow(categories_list, iva_list, product_name = db_product['name'],
                                        product_price = db_product['price'], product_iva_cb = True, 
                                        product_order = db_product['order'], product_iva_type = db_product['iva_type'],
                                        product_category = self.category, product_description = db_product['description'])
            open_new_window(edit_window)
            self.set_table_model()
            
    def remove_product_row(self):
        order = self.get_selected_order()
        if order:
            order_name = self.category + order
            remove_product_by_order_name(session, order_name)
            reorder_products_order(session, self.category, int(order))
            self.set_table_model()
    
    def unlock_ordering(self):
        if self.order_edit_button.isChecked():
            self.table_header.setDisabled(False)
            self.produts_table.setSortingEnabled(True)
            self.produts_table.sortByColumn(3, Qt.SortOrder.AscendingOrder)
        else:
            self.table_header.setDisabled(True)
            self.produts_table.setSortingEnabled(False)
            
    def set_order_by_header(self):
        order_num = 1
        placeholder = '_'
        
        for row in range(self.table_model.rowCount()):
            name = self.table_model.item(row, 0).text()
            order = self.table_model.item(row, 3).text()
            order_name = self.category + order
            switch_product_order(session, name, order_name, placeholder)
            placeholder += '_'
            
        placeholder = '_'    
            
        for row in range(self.table_model.rowCount()):
            name = self.table_model.item(row, 0).text()
            order_name = self.category + str(order_num)
            switch_product_order(session, name, placeholder, order_name)
            placeholder += '_'
            order_num += 1
            
        self.set_table_model()
                  
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


        
        
        
        
        
        