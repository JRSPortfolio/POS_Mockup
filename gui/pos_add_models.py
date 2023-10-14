from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, 
                            QPushButton, QTextEdit)
from PyQt6.QtCore import Qt

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
        

class AddProductWindow(QDialog):
    def __init__(self):
        super(AddProductWindow, self).__init__()
        
        self.set_widgets_placements()
    
    def set_widgets_placements(self):
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle('Adicionar Produto')

