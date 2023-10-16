from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, 
                            QPushButton, QTextEdit, QComboBox, QTableWidget)
from PyQt6.QtCore import Qt
from database.pos_crud import create_db_category
from database.mysql_engine import session

class AddUserWindow(QDialog):
    def __init__(self):
        super(AddUserWindow, self).__init__()
        
        self.set_widgets_placements()
    
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
        add_user_exit_button = QPushButton('Sair')
        
        add_user_name_label.setFixedWidth(120)
        add_user_username_label.setFixedWidth(120)
        add_user_password_label.setFixedWidth(120)
        add_user_confirm_password_label.setFixedWidth(120)
        add_user_create_button.setFixedSize(140, 40)
        add_user_exit_button.setFixedSize(140, 40)
        
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
        add_user_buttons_layout.addWidget(add_user_exit_button)
        
        add_user_exit_button.clicked.connect(lambda: self.close())
        
class AddCategoryWindow(QDialog):
    def __init__(self):
        super(AddCategoryWindow, self).__init__()
        
        self.set_widgets_placements()
    
    def set_widgets_placements(self):
        self.setGeometry(200, 200, 450, 230)
        self.setWindowTitle('Adicionar Categoria?')
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
        add_category_exit_button = QPushButton('Sair')
        
        add_category_name_label.setFixedWidth(80)
        add_category_descripton_label.setFixedWidth(80)
        add_category_descripton_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.add_category_description_text_edit.setMinimumHeight(80)
        add_category_create_button.setFixedSize(140, 40)
        add_category_exit_button.setFixedSize(140, 40)
        
        add_category_fields_layout.addWidget(add_category_name_label, 0, 0)
        add_category_fields_layout.addWidget(self.add_category_name_line_edit, 0, 1)
        add_category_fields_layout.addWidget(add_category_descripton_label, 1, 0)
        add_category_fields_layout.addWidget(self.add_category_description_text_edit, 1, 1)
        add_category_buttons_layout.addWidget(add_category_create_button)
        add_category_buttons_layout.addWidget(add_category_exit_button)
        
        add_category_create_button.clicked.connect(self.create_category)
        add_category_exit_button.clicked.connect(lambda: self.close())
        
    def create_category(self):
        name = self.add_category_name_line_edit.text()
        description = self.add_category_description_text_edit.toPlainText()
        create_db_category(session, name, description)

class AddProductWindow(QDialog):
    def __init__(self):
        super(AddProductWindow, self).__init__()
        
        self.set_widgets_placements()
    
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
        add_product_exit_button = QPushButton('Sair')
        
        add_product_name_label.setFixedWidth(120)
        add_product_price_label.setFixedWidth(120)
        add_product_iva_label.setFixedWidth(120)
        add_product_category_label.setFixedWidth(120)
        add_product_description_label.setFixedWidth(120)
        add_product_description_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.add_product_description_text_edit.setMinimumHeight(80)
        add_product_create_button.setFixedSize(140, 40)
        add_product_exit_button.setFixedSize(140, 40)
        
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
        add_product_buttons_layout.addWidget(add_product_exit_button)
        
        add_product_exit_button.clicked.connect(lambda: self.close())
        
class EditRemCatProdWindow(QDialog):
    def __init__(self):
        super(EditRemCatProdWindow, self).__init__()
        
        self.set_widgets_placements()
    
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
        edit_rem_exit_button = QPushButton('Sair')
        
        category_edit_button.setFixedWidth(140)
        category_remove_button.setFixedWidth(140)
        product_edit_button.setFixedWidth(140)
        product_remove_button.setFixedWidth(140)
        edit_rem_exit_button.setFixedSize(140, 40)
        
        cat_prod_fields_layout.addWidget(category_label, 0, 0)
        cat_prod_fields_layout.addWidget(self.category_combo_box, 0 ,1)
        cat_prod_fields_layout.addWidget(category_edit_button, 1, 0, alignment= Qt.AlignmentFlag.AlignCenter)
        cat_prod_fields_layout.addWidget(category_remove_button, 1, 1, alignment= Qt.AlignmentFlag.AlignCenter)
        cat_prod_fields_layout.addWidget(products_label, 2, 0, 1, 2)
        cat_prod_fields_layout.addWidget(produts_table, 3, 0, 1, 2)
        cat_prod_fields_layout.addWidget(product_edit_button, 4, 0, alignment= Qt.AlignmentFlag.AlignCenter)
        cat_prod_fields_layout.addWidget(product_remove_button, 4, 1, alignment= Qt.AlignmentFlag.AlignCenter)
        edit_rem_cat_pro_button_layout.addWidget(edit_rem_exit_button)
        
        edit_rem_exit_button.clicked.connect(lambda: self.close())


     
        
        
        
        
        
        
        
        
        
        