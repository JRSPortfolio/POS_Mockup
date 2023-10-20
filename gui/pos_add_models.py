from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, 
                            QPushButton, QTextEdit, QComboBox, QTableWidget, QWidget)
from PyQt6.QtCore import Qt
from database.pos_crud import (create_db_category, validate_category_name, get_categories_list, create_db_tipo_iva,
                               validate_iva_input, get_iva_types_list, get_iva_value_by_name, remove_iva_by_name,
                               change_iva_by_name, validate_iva_name, validate_iva_value, get_tipo_iva_list,
                               remove_category_by_name, change_category_by_name, get_category_description_by_name)
from database.mysql_engine import session

class POSDialog(QDialog):
    def __init__(self):
        super(POSDialog, self).__init__()
        
        if self.set_widgets_placements():
            self.set_widgets_placements()

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
        self.add_user_name_line_edit = QLineEdit()
        add_user_username_label = QLabel('Username:')
        self.add_user_username_line_edit = QLineEdit()
        self.add_user_admin_check_box = QCheckBox('Privilégios de Administração')
        add_user_password_label = QLabel('Password')
        self.add_user_password_line_edit = QLineEdit()
        add_user_confirm_password_label = QLabel('Confirmar Password')
        self.add_user_confirm_password_line_edit = QLineEdit()
        add_user_create_button = QPushButton('Criar Utilizador')
        add_user_close_button = QPushButton('Fechar')
        
        add_user_name_label.setFixedWidth(120)
        add_user_username_label.setFixedWidth(120)
        add_user_password_label.setFixedWidth(120)
        add_user_confirm_password_label.setFixedWidth(120)
        add_user_create_button.setFixedSize(140, 40)
        add_user_close_button.setFixedSize(140, 40)
        
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

class AddProductWindow(POSDialog):
    def __init__(self, category_list: list, iva_list: list):
        self.category_list = category_list
        self.iva_list = iva_list
        super(AddProductWindow, self).__init__()
        
    def set_widgets_placements(self):
        self.setGeometry(200, 200, 500, 200)
        self.setWindowTitle('Adicionar Produto')
                
        add_product_layout = QVBoxLayout()
        self.setLayout(add_product_layout)

        add_product_fields_layout = QGridLayout()
        add_product_buttons_layout = QHBoxLayout()
        add_product_layout.addLayout(add_product_fields_layout)
        add_product_layout.addLayout(add_product_buttons_layout)
        
        add_product_name_label = QLabel("Nome:")
        self.add_product_name_line_edit = QLineEdit()
        add_product_price_label = QLabel("Preço:")
        self.add_product_price_line_edit = QLineEdit()
        self.add_product_set_iva_check_box = QCheckBox("Preço c/ IVA")
        add_product_iva_label = QLabel("Cateogira de IVA:")
        self.add_product_iva_combo_box = QComboBox()
        add_product_category_label = QLabel("Categoria:")
        self.add_product_category_combo_box = QComboBox()
        add_product_description_label = QLabel("Descrição")
        self.add_product_description_text_edit = QTextEdit()
        add_product_create_button = QPushButton('Adicionar Produto')
        self.add_product_close_button = QPushButton('Fechar')
        
        add_product_name_label.setFixedWidth(120)
        add_product_price_label.setFixedWidth(120)
        add_product_iva_label.setFixedWidth(120)
        add_product_category_label.setFixedWidth(120)
        add_product_description_label.setFixedWidth(120)
        add_product_description_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.add_product_description_text_edit.setMinimumHeight(80)
        add_product_create_button.setFixedSize(140, 40)
        self.add_product_close_button.setFixedSize(140, 40)
        
        for category in self.category_list:
            self.add_product_category_combo_box.addItem(category)
        
        for iva_type in self.iva_list:
            self.add_product_iva_combo_box.addItem(iva_type)
                        
        add_product_fields_layout.addWidget(add_product_name_label, 0, 0)
        add_product_fields_layout.addWidget(self.add_product_name_line_edit, 0, 1)
        add_product_fields_layout.addWidget(add_product_price_label, 1, 0)
        add_product_fields_layout.addWidget(self.add_product_price_line_edit, 1, 1)
        add_product_fields_layout.addWidget(self.add_product_set_iva_check_box, 2, 0, 1, 2)
        add_product_fields_layout.addWidget(add_product_iva_label, 3, 0)
        add_product_fields_layout.addWidget(self.add_product_iva_combo_box, 3, 1)
        add_product_fields_layout.addWidget(add_product_category_label, 4, 0)
        add_product_fields_layout.addWidget(self.add_product_category_combo_box, 4, 1)
        add_product_fields_layout.addWidget(add_product_description_label, 5, 0)
        add_product_fields_layout.addWidget(self.add_product_description_text_edit, 5, 1)
        add_product_buttons_layout.addWidget(add_product_create_button)
        add_product_buttons_layout.addWidget(self.add_product_close_button)
        
        self.add_product_close_button.clicked.connect(self.close)   
        
class EditProdutcsWindow(POSDialog):

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
        self.category_combo_box = QComboBox()
        products_label = QLabel('Produtos:')
        produts_table = QTableWidget()
        product_edit_button = QPushButton('Editar Produto')
        product_remove_button = QPushButton('Remover Produto')
        edit_rem_close_button = QPushButton('Fechar')
        

        product_edit_button.setFixedWidth(140)
        product_remove_button.setFixedWidth(140)
        edit_rem_close_button.setFixedSize(140, 40)
        
        cat_prod_fields_layout.addWidget(category_label, 0, 0)
        cat_prod_fields_layout.addWidget(self.category_combo_box, 0 ,1)
        cat_prod_fields_layout.addWidget(products_label, 1, 0, 1, 2)
        cat_prod_fields_layout.addWidget(produts_table, 2, 0, 1, 2)
        cat_prod_fields_layout.addWidget(product_edit_button, 3, 0, alignment = Qt.AlignmentFlag.AlignCenter)
        cat_prod_fields_layout.addWidget(product_remove_button, 3, 1, alignment = Qt.AlignmentFlag.AlignCenter)
        edit_rem_cat_pro_button_layout.addWidget(edit_rem_close_button)
        
        edit_rem_close_button.clicked.connect(self.close)

class SetEditOptionsWindow(POSDialog):

    # Required fileds in __init__:
    # self.first_title_label_text -> str
    # self.second_title_label_text -> str
    # self.get_types_list -> get listing function
    # self.list_label_text ->  str
    # self.get_value_by_name -> retrieve value by name function
    # self.change_by_name -> change row by name function
    # self.remove_by_name -> remove by name function
    #
    # Usefull fields in super:
    # self.setWindowTitle = 'Adicionar Taxa de IVA'
    # self.setGeometry(200, 200, 500, 100)
    #
    #Required methods:
    #def self.create_type(self):
    #def self.validate_row(self, name:str , new_name: str, value: str, new_value: str):

    def set_widgets_placements(self):
        base_layout = QVBoxLayout()
        self.setLayout(base_layout)
        
        self.fields_layout = QGridLayout()
        buttons_layout = QHBoxLayout()
        base_layout.addLayout(self.fields_layout)
        base_layout.addLayout(buttons_layout)
        
        first_title_label = QLabel(self.first_title_label_text)
        self.first_line_edit = QLineEdit()
        second_title_label = QLabel(self.second_title_label_text)
        self.second_line_edit = QLineEdit()
        create_button = QPushButton('Adicionar')
        placeholder = QWidget()
        close_button = QPushButton('Fechar')
        
        first_title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        second_title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.first_line_edit.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.second_line_edit.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        create_button.setFixedWidth(160)
        close_button.setFixedSize(140, 40)
        placeholder.setFixedWidth(80)
                
        self.fields_layout.addWidget(first_title_label, 0, 0)
        self.fields_layout.addWidget(second_title_label, 0, 1)
        self.fields_layout.addWidget(self.first_line_edit, 1, 0)
        self.fields_layout.addWidget(self.second_line_edit, 1, 1)
        self.fields_layout.addWidget(placeholder, 1, 2)
        self.fields_layout.addWidget(create_button, 1, 3, 1, 2)
        self.fields_layout.addWidget(placeholder, 1, 4)
        buttons_layout.addWidget(close_button)
        
        create_button.clicked.connect(self.create_type)
        close_button.clicked.connect(self.close)

        self.set_types_list()
            
    def set_types_list(self):
        type_list = self.get_types_list(session)
        if not type_list:
            return
        
        list_label = QLabel('Existentes:')
        self.fields_layout.addWidget(list_label, 2, 0)
        
        row = 3
        for entry in type_list:
            value = self.get_value_by_name(session, entry)
            name_label = QLabel(entry)
            value_label = QLabel(str(value))
            edit_button = QPushButton('Editar')
            remove_button = QPushButton('Remover')
            
            name_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            value_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            edit_button.setFixedWidth(80)
            remove_button.setFixedWidth(80)

            self.fields_layout.addWidget(name_label, row, 0)
            self.fields_layout.addWidget(value_label, row, 1)
            self.fields_layout.addWidget(edit_button, row, 2)
            self.fields_layout.addWidget(remove_button, row, 3)
            
            edit_button.clicked.connect(lambda _, name_label = name_label, value_label = value_label, edit_button = edit_button,
                                        row = row: self.edit_fields(name_label = name_label, value_label = value_label, 
                                                                        edit_button = edit_button, row = row))
            
            remove_button.clicked.connect(lambda _, name = name_label.text(): self.remove_row(name = name))
            
            row += 1

    def edit_fields(self, name_label: QLabel, value_label: QLabel, edit_button: QPushButton, row: int):
        name_label.close()
        value_label.close()
        edit_button.close()
        
        name_edit = QLineEdit()
        value_edit = QLineEdit()
        modify_button = QPushButton('Alterar')
        cancel_button = QPushButton('Cancelar')
        
        name_edit.setText(name_label.text())
        value_edit.setText(value_label.text())
        name_edit.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        value_edit.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        modify_button.setFixedWidth(80)
        cancel_button.setFixedWidth(80)
        
        self.fields_layout.addWidget(name_edit, row, 0)
        self.fields_layout.addWidget(value_edit, row, 1)
        self.fields_layout.addWidget(modify_button, row, 2)
        self.fields_layout.addWidget(cancel_button, row, 4)
        
        modify_button.clicked.connect(lambda: self.edit_row(name_label.text(), name_edit.text(), value_label.text(),
                                                                value_edit.text()))
                
        cancel_button.clicked.connect(lambda: self.cancel_edit(name_label, value_label, edit_button, name_edit, value_edit, modify_button,
                                                                 cancel_button))

    def cancel_edit(self, name: QLabel, value: QLabel, edit_button: QPushButton, name_edit: QLineEdit,
                      value_edit: QLineEdit, new_edit_button: QPushButton, cancel_button: QPushButton):
        name_edit.close()
        value_edit.close()
        new_edit_button.close()
        cancel_button.close()

        name.show()
        value.show()
        edit_button.show()
        
    def remove_listing(self):
        grid_rows = self.fields_layout.rowCount()
        for row in range(2, grid_rows):
            for col in range(5):
                item = self.fields_layout.itemAtPosition(row, col)
                if item:
                    widget = item.widget()
                    self.fields_layout.removeItem(item)
                    widget.deleteLater()
                    
    def remove_row(self, name: str):
        self.remove_by_name(session, name)
        self.remove_listing()
        self.remove_listing()
        self.set_types_list()
        
    def edit_row(self, name:str , new_name: str, value: str, new_value: str):
        messages = self.validate_row(name, new_name, value, new_value)
        if not messages:
            try:
                new_value = int(new_value)
            except:
                pass
            self.change_by_name(session, name, new_name, new_value)
            self.remove_listing()
            self.remove_listing()
            self.set_types_list()
        else:
            message_title = "Erro de Edição"
            message_window = MessageWindow(message_title, messages)
            open_new_window(message_window)
            self.remove_listing()
            self.remove_listing()
            self.set_types_list()
            
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
                      
class MessageWindow(POSDialog):
    def __init__(self, titulo: str, messages: list):
        self.titulo = titulo
        self.messages = messages  
        super(MessageWindow, self).__init__()

    def set_widgets_placements(self):
        self.setGeometry(200, 200, 300, 200)
        self.setWindowTitle(self.titulo)
        add_message_layout = QVBoxLayout()
        self.setLayout(add_message_layout)
        
        for message in self.messages:
            message_label = QLabel(message)
            add_message_layout.addWidget(message_label, alignment = Qt.AlignmentFlag.AlignCenter)
        
        message_close_button = QPushButton('Fechar')
        message_close_button.setFixedSize(140, 40)
        
        add_message_layout.addWidget(message_close_button, alignment = Qt.AlignmentFlag.AlignCenter)
        
        message_close_button.clicked.connect(lambda: self.close())
        
class MissingValueWindow(POSDialog):
    def __init__(self, title: str, message: str, button_title: str, add_value_window: POSDialog, aditional_button_title = None,
                 add_aditiona_window = None):
        self.title = title
        self.message = message
        self.button_title = button_title
        self.add_value_window = add_value_window
        self.aditional_button_title = aditional_button_title
        self.add_aditional_window = add_aditiona_window
        super(MissingValueWindow, self).__init__()
    
    def set_widgets_placements(self):
        self.setGeometry(200, 200, 300, 200)
        self.setWindowTitle(self.title)
        missing_value_layout = QGridLayout()
        self.setLayout(missing_value_layout)
        
        missing_value_message_label = QLabel(self.message)
        missing_value_window_button = QPushButton(self.button_title)
        missing_value_close_button = QPushButton('Fechar')
        
        missing_value_message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        missing_value_window_button.setFixedSize(140, 40)
        missing_value_close_button.setFixedSize(140, 40)
        
        missing_value_layout.addWidget(missing_value_message_label,0 ,0, 1, 2)
        
        if self.add_aditional_window is not None:
            aditional_window_button = QPushButton(self.aditional_button_title)
            aditional_window_button.setFixedSize(140, 40)
            missing_value_layout.addWidget(missing_value_window_button, 1, 0, alignment = Qt.AlignmentFlag.AlignCenter)
            missing_value_layout.addWidget(aditional_window_button, 1, 1, alignment = Qt.AlignmentFlag.AlignCenter)
            missing_value_layout.addWidget(missing_value_close_button, 2, 0, 1, 2, alignment = Qt.AlignmentFlag.AlignCenter)
            aditional_window_button.clicked.connect(self.open_aditional_window)
        else:   
            missing_value_layout.addWidget(missing_value_window_button, 1, 0, alignment = Qt.AlignmentFlag.AlignCenter)
            missing_value_layout.addWidget(missing_value_close_button,1, 1, alignment = Qt.AlignmentFlag.AlignCenter)
        
        missing_value_window_button.clicked.connect(self.open_window)
        missing_value_close_button.clicked.connect(self.close)
        
    def open_window(self):
        self.close()
        open_new_window(self.add_value_window)
        
    def open_aditional_window(self):
        self.close()
        open_new_window(self.add_aditional_window)
        
def open_new_window(new_window: POSDialog):
    open_qdialog = new_window
    open_qdialog.exec()
         
def open_AddProductWindow():
    category_list = get_categories_list(session)
    iva_list = get_tipo_iva_list(session)
    if category_list and iva_list:
        add_product = AddProductWindow(category_list, iva_list)
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

        
        
        
        
        
        
        