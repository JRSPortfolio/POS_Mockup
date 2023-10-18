from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, 
                            QPushButton, QTextEdit, QComboBox, QTableWidget, QWidget)
from PyQt6.QtCore import Qt
from database.pos_crud import (create_db_category, validate_category_name, get_categories_list, create_db_tipo_iva,
                               validate_iva_input, get_iva_types_list, get_iva_value_by_name)
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
        
class AddCategoryWindow(POSDialog):

    def set_widgets_placements(self):
        self.setGeometry(200, 200, 450, 230)
        self.setWindowTitle('Adicionar Categoria')
        add_category_layout = QVBoxLayout()
        self.setLayout(add_category_layout)
        
        add_category_fields_layout = QGridLayout()
        add_category_buttons_layout = QHBoxLayout()
        add_category_layout.addLayout(add_category_fields_layout)
        add_category_layout.addLayout(add_category_buttons_layout)
        
        add_category_name_label = QLabel('Nome:')
        self.add_category_name_line_edit = QLineEdit()
        add_category_descripton_label = QLabel('Descrição:')
        self.add_category_description_text_edit = QTextEdit()
        add_category_create_button = QPushButton('Adicionar Categoria')
        add_category_close_button = QPushButton('Fechar')
        
        add_category_name_label.setFixedWidth(80)
        add_category_descripton_label.setFixedWidth(80)
        add_category_descripton_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.add_category_description_text_edit.setMinimumHeight(80)
        add_category_create_button.setFixedSize(140, 40)
        add_category_close_button.setFixedSize(140, 40)
        
        add_category_fields_layout.addWidget(add_category_name_label, 0, 0)
        add_category_fields_layout.addWidget(self.add_category_name_line_edit, 0, 1)
        add_category_fields_layout.addWidget(add_category_descripton_label, 1, 0)
        add_category_fields_layout.addWidget(self.add_category_description_text_edit, 1, 1)
        add_category_buttons_layout.addWidget(add_category_create_button)
        add_category_buttons_layout.addWidget(add_category_close_button)
        
        add_category_create_button.clicked.connect(self.create_category)
        add_category_close_button.clicked.connect(self.close)
                
    def create_category(self):
        name = self.add_category_name_line_edit.text()
        description = self.add_category_description_text_edit.toPlainText()
        
        messages = validate_category_name(session, name)
        if messages == None:
            create_db_category(session, name, description)
            message_title = 'Categoria Criada'
            message_content = [f'Criada categoria {name}']
            message_window = MessageWindow(message_title, message_content)
            open_new_window(message_window)
            self.add_category_name_line_edit.clear()
            self.add_category_description_text_edit.clear()
        else:
            message_title = "Nome de Categoria"
            message_window = MessageWindow(message_title, messages)
            open_new_window(message_window)
            self.add_category_name_line_edit.clear()

class AddProductWindow(POSDialog):
    def __init__(self, category_list: list):
        self.category_list = category_list
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
        
class EditRemCatProdWindow(POSDialog):

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
        category_edit_button = QPushButton('Editar Categoria')
        category_remove_button = QPushButton('Remover Categoria')
        products_label = QLabel('Produtos:')
        produts_table = QTableWidget()
        product_edit_button = QPushButton('Editar Produto')
        product_remove_button = QPushButton('Remover Produto')
        edit_rem_close_button = QPushButton('Fechar')
        
        category_edit_button.setFixedWidth(140)
        category_remove_button.setFixedWidth(140)
        product_edit_button.setFixedWidth(140)
        product_remove_button.setFixedWidth(140)
        edit_rem_close_button.setFixedSize(140, 40)
        
        cat_prod_fields_layout.addWidget(category_label, 0, 0)
        cat_prod_fields_layout.addWidget(self.category_combo_box, 0 ,1)
        cat_prod_fields_layout.addWidget(category_edit_button, 1, 0, alignment= Qt.AlignmentFlag.AlignCenter)
        cat_prod_fields_layout.addWidget(category_remove_button, 1, 1, alignment= Qt.AlignmentFlag.AlignCenter)
        cat_prod_fields_layout.addWidget(products_label, 2, 0, 1, 2)
        cat_prod_fields_layout.addWidget(produts_table, 3, 0, 1, 2)
        cat_prod_fields_layout.addWidget(product_edit_button, 4, 0, alignment = Qt.AlignmentFlag.AlignCenter)
        cat_prod_fields_layout.addWidget(product_remove_button, 4, 1, alignment = Qt.AlignmentFlag.AlignCenter)
        edit_rem_cat_pro_button_layout.addWidget(edit_rem_close_button)
        
        edit_rem_close_button.clicked.connect(self.close)
        
class SetIVAWindow(POSDialog):

    def set_widgets_placements(self):
        self.setGeometry(200, 200, 400, 100)
        self.setWindowTitle('Adicionar Categoria')
        iva_layout = QVBoxLayout()
        self.setLayout(iva_layout)
        
        self.iva_fields_layout = QGridLayout()
        iva_buttons_layout = QHBoxLayout()
        iva_layout.addLayout(self.iva_fields_layout)
        iva_layout.addLayout(iva_buttons_layout)
        
        iva_label = QLabel('Designação:')
        self.iva_line_edit = QLineEdit()
        iva_valor_label = QLabel('Taxa (%):')
        self.iva_valor_line_edit = QLineEdit()
        iva_create_button = QPushButton('Adicionar')
        iva_placeholder = QWidget()
        iva_close_button = QPushButton('Fechar')
        
        iva_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        iva_valor_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.iva_line_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.iva_valor_line_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        iva_create_button.setFixedWidth(160)
        iva_close_button.setFixedSize(140, 40)
        iva_placeholder.setFixedWidth(80)
                
        self.iva_fields_layout.addWidget(iva_label, 0, 0)
        self.iva_fields_layout.addWidget(iva_valor_label, 0, 1)
        self.iva_fields_layout.addWidget(self.iva_line_edit, 1, 0)
        self.iva_fields_layout.addWidget( self.iva_valor_line_edit, 1, 1)
        self.iva_fields_layout.addWidget(iva_create_button, 1, 2, 1, 2)
        self.iva_fields_layout.addWidget(iva_placeholder, 1, 3)
        iva_buttons_layout.addWidget(iva_close_button)
        
        iva_create_button.clicked.connect(self.create_iva_type)
        iva_close_button.clicked.connect(self.close)

        self.set_iva_types_list()
        
    def create_iva_type(self):
        name = self.iva_line_edit.text()
        value = self.iva_valor_line_edit.text()
        try:
            value = int(value)
        except:
            pass
        
        messages = validate_iva_input(session, name, value)
        
        if messages == None:
            create_db_tipo_iva(session, name, value)
            message_title = 'Designação Criada'
            message_content = [f'Criada Designação de IVA {name} com Taxa de {value}%']
            message_window = MessageWindow(message_title, message_content)
            open_new_window(message_window)
            self.iva_line_edit.clear()
            self.iva_valor_line_edit.clear()
            self.set_iva_types_list()
        else:
            message_title = "Erro de Inserção"
            message_window = MessageWindow(message_title, messages)
            open_new_window(message_window)
            self.iva_line_edit.clear()
            self.iva_valor_line_edit.clear()
            
    def set_iva_types_list(self):
        iva_list = get_iva_types_list(session)
        if not iva_list:
            return
        
        iva_list_label = QLabel('Designações Existentes:')
        iva_list_label.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.iva_fields_layout.addWidget(iva_list_label, 2, 0)
        
        row_number = 3
        for entry in iva_list:
            value = get_iva_value_by_name(session, entry)
            name_label = QLabel(entry)
            value_label = QLabel(str(value))
            edit_button = QPushButton('Editar')
            
            name_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            value_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            edit_button.setFixedSize(80, 25)
            
            self.iva_fields_layout.addWidget(name_label, row_number, 0)
            self.iva_fields_layout.addWidget(value_label, row_number, 1)
            self.iva_fields_layout.addWidget(edit_button, row_number, 2)
            
            edit_button.clicked.connect(lambda _, name_label = name_label, value_label = value_label, iva_edit = edit_button,
                                        row = row_number: self.edit_iva_fields(name_label, value_label, iva_edit, row))

            row_number += 1

    def edit_iva_fields(self, name_label: QLabel, value_label: QLabel, iva_edit: QPushButton, row: int):
        name_label.hide()
        value_label.hide()
        iva_edit.hide()
        
        name_edit = QLineEdit()
        value_edit = QLineEdit()
        modify_button = QPushButton('Alterar')
        cancel_button = QPushButton('Cancelar')
        
        name_edit.setText(name_label.text())
        value_edit.setText(value_label.text())
        modify_button.setFixedSize(80, 25)
        cancel_button.setFixedSize(80, 25)
        
        self.iva_fields_layout.addWidget(name_edit, row, 0)
        self.iva_fields_layout.addWidget(value_edit, row, 1)
        self.iva_fields_layout.addWidget(modify_button, row, 2)
        self.iva_fields_layout.addWidget(cancel_button, row, 3)
        
        cancel_button.clicked.connect(lambda: self.cancel_iva_edit(name_label, value_label, iva_edit, name_edit, value_edit, modify_button,
                                                                 cancel_button))
            
    def cancel_iva_edit(self, name: QLabel, value: QLabel, iva_edit: QPushButton, name_edit: QLineEdit,
                      value_edit: QLineEdit, iva_edit_button: QPushButton, cancel_button: QPushButton):
        name_edit.hide()
        value_edit.hide()
        iva_edit_button.hide()
        cancel_button.hide()
        
        name.show()
        value.show()
        iva_edit.show()
              
class MessageWindow(QDialog):
    def __init__(self, titulo: str, messages: list):
        super(MessageWindow, self).__init__()
        
        self.titulo = titulo
        self.messages = messages
        
        self.set_widgets_placements()
    
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
        
class MissingValueWindow(QDialog):
    def __init__(self, title: str, message: str, button_title: str, add_value: QDialog):
        super(MissingValueWindow, self).__init__()
        
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        self.title = title
        self.message = message
        self.button_title = button_title
        self.open_window = add_value
        
        self.set_widgets_placements()
    
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
        missing_value_layout.addWidget(missing_value_window_button, 1, 0, alignment = Qt.AlignmentFlag.AlignCenter)
        missing_value_layout.addWidget(missing_value_close_button,1, 1, alignment = Qt.AlignmentFlag.AlignCenter)
        
        missing_value_window_button.clicked.connect(self.open_AddCategoryWindow)
        missing_value_close_button.clicked.connect(self.close)
        
    def open_AddCategoryWindow(self):
        self.close()
        open_new_window(AddCategoryWindow())
        
def open_new_window(new_window: QDialog):
    open_qdialog = new_window
    open_qdialog.exec()
         
def open_AddProductWindow():
    category_list = get_categories_list(session)
    if category_list:
        add_product = AddProductWindow(category_list)
        open_new_window(add_product)
    else:
        title = "Sem Categorias"
        message = "É necessário Categorias para adicionar Produto.\nCriar Categoria?"
        button_title = "Criar Categoria"
        new_window = MissingValueWindow(title, message, button_title, AddCategoryWindow())
        open_new_window(new_window)
     
        
        
        
        
        
        
        
        
        
        