# from PyQt6.QtCore import 
# from PyQt6.QtGui import 
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QGridLayout, QLabel,
                             QStackedWidget, QFormLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
import sys
from gui.pos_add_models import (UserWindow, SetEditCategoryWindow, open_AddProductWindow,
                                SetEditIVAWindow, open_editable_UserWindow, no_users_window)
from gui.pos_edit_models import EditRemoveProdutcsWindow
from gui.pos_custom_widgets import(POSDialog, open_new_window, OptionsSectionButton, PaymentSectionButton, FONT_TYPE,
                                   RoundedComboBox, RoundedLeftLineEdit, HighOptionsButton)
from gui.pos_custom_widgets import STYLE, MessageWindow
from database.pos_crud_and_validations import (get_users_usernames, check_if_admin_by_username, verify_hashed_password,
                                               get_user_password_by_username, create_hash_password)
from database.mysql_engine import session

# class CurrentUserInfo():
#     def __init__(self):
#         self.username = 0
#         self.admin_status = 0
    
#     # username = 0
#     # admin_status = 0
        
#     def set_user_info(self, username: str, admin_status: bool):
#         self.username = username
#         self.admin_status = admin_status
        
#     def get_user_info(self):
#         return self.username, self.admin_status
        
class POSMainWindow(QMainWindow):
    def __init__(self):
        self.user_info = {}
        self.users_list = get_users_usernames(session)
        super(POSMainWindow, self).__init__()
        self.setFont(FONT_TYPE)
        self.setStyleSheet(STYLE)
        self.set_window_placements()
        self.set_menubar()
        if self.user_info:
            self.set_app_widget()
        else:
            self.set_login_widget()
        
    def set_window_placements(self):        
        self.setGeometry(100, 100, 1000, 600)
        self.setWindowTitle("POS") 
        self.baseWidget = QStackedWidget()
        self.mainWindowWidgets = QWidget()
        self.loginWidget = QWidget()
        self.setCentralWidget(self.baseWidget)
        
        self.baseWidget.addWidget(self.mainWindowWidgets)
        self.baseWidget.addWidget(self.loginWidget)
        
        self.set_app_widgets()
        self.set_login_widgets()
        
        
    def set_app_widgets(self):
        self.mainWidgetsLayout = QHBoxLayout(self.mainWindowWidgets)
        self.leftLayout = QVBoxLayout()
        self.rightLayout = QVBoxLayout()
        self.mainWidgetsLayout.addLayout(self.leftLayout)
        self.mainWidgetsLayout.addLayout(self.rightLayout)
        
        categoriesBox = QGroupBox("Categorias")
        productsBox = QGroupBox("Produtos")
        optionsBox = QGroupBox("Opções")
        salesBox = QGroupBox("Vendas")
        paymentBox = QGroupBox("Pagamento")
        
        optionsBox.setFixedHeight(120)
        paymentBox.setFixedHeight(120)
        categoriesBox.setFixedHeight(150)
        
        self.leftLayout.addWidget(categoriesBox)
        self.leftLayout.addWidget(productsBox)
        self.leftLayout.addWidget(optionsBox)
        self.rightLayout.addWidget(salesBox)
        self.rightLayout.addWidget(paymentBox)
        
        self.categories_section_layout = QHBoxLayout()
        self.products_section_layout = QHBoxLayout()
        self.options_section_layout = QHBoxLayout()
        self.sales_section_layout = QHBoxLayout()
        self.payment_section_layout = QHBoxLayout()
        
        self.options_section_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        categoriesBox.setLayout(self.categories_section_layout)
        productsBox.setLayout(self.products_section_layout)
        optionsBox.setLayout(self.options_section_layout)
        salesBox.setLayout(self.sales_section_layout)
        paymentBox.setLayout(self.payment_section_layout)

        self.mainWidgetsLayout.setStretchFactor(self.leftLayout, 3)
        self.mainWidgetsLayout.setStretchFactor(self.rightLayout, 2)
        
        self.set_options_section()
        self.set_payment_section()
        
    def set_options_section(self):
        user_button = OptionsSectionButton('Utilizador')        
        self.options_section_layout.addWidget(user_button)
        
        user_button.clicked.connect(self.set_login_widget)
        
    def set_login_widget(self):
        self.baseWidget.setCurrentIndex(1)
        self.login_user_combo_box.setCurrentIndex(-1)
        self.setWindowTitle("POS")
    
    def set_payment_section(self):
        print_button = PaymentSectionButton('Imprimir Recibo')
        payment_button = PaymentSectionButton('Pagamento')

        self.payment_section_layout.addWidget(print_button)
        self.payment_section_layout.addWidget(payment_button)
        
    def set_app_widget(self):
        self.baseWidget.setCurrentIndex(0)
        self.setWindowTitle(f"POS - {self.user_info['username']}")
        
    def set_login_widgets(self):
        self.login_layout = QVBoxLayout(self.loginWidget)

        login_fields_layout = QFormLayout()
        login_buttons_layout = QHBoxLayout()
        self.login_layout.addLayout(login_fields_layout)
        self.login_layout.addLayout(login_buttons_layout)
        
        login_user_label = QLabel('Utilizador')
        self.login_user_combo_box = RoundedComboBox()
        self.login_password_label = QLabel('Password')
        self.login_password_line_edit = RoundedLeftLineEdit()
        self.login_enter_button = HighOptionsButton('Login')
        login_close_button = HighOptionsButton('Fechar')
        
        for user in self.users_list:
            self.login_user_combo_box.addItem(user)
        
        self.login_user_combo_box.setCurrentIndex(-1)
        self.login_user_combo_box.currentIndexChanged.connect(self.password_field_check)
        self.login_password_line_edit.setEchoMode(RoundedLeftLineEdit.EchoMode.Password)
        
        login_user_label.setFixedWidth(140)
        self.login_password_label.setFixedWidth(140)
        self.login_user_combo_box.setFixedWidth(240)
        self.login_password_line_edit.setFixedWidth(240)
        login_fields_layout.setFormAlignment(Qt.AlignmentFlag.AlignCenter)
        login_buttons_layout.setContentsMargins(0, 0, 0, 100)
        
        self.login_password_label.hide()
        self.login_password_line_edit.hide()
        
        login_fields_layout.addRow(login_user_label, self.login_user_combo_box)
        login_fields_layout.addRow(self.login_password_label, self.login_password_line_edit)
        login_buttons_layout.addWidget(self.login_enter_button)
        login_buttons_layout.addWidget(login_close_button)
        
        self.login_enter_button.clicked.connect(self.login_check)
        login_close_button.clicked.connect(self.close)
        
    def password_field_check(self):
        self.admin_check = check_if_admin_by_username(session, self.login_user_combo_box.currentText())
        if self.admin_check:
            self.login_password_label.show()
            self.login_password_line_edit.show()
        else:
            self.login_password_label.hide()
            self.login_password_line_edit.hide() 
        
    def login_check(self):
        username =  self.login_user_combo_box.currentText()
        if self.admin_check:
            password = self.login_password_line_edit.text()
            db_hashed_password = get_user_password_by_username(session, username)
            messages = verify_hashed_password(password, db_hashed_password)
            if not messages:
                self.user_info['username'] = username
                self.user_info['admin_status'] = self.admin_check
                self.set_app_widget()
            else:
                self.login_password_line_edit.clear()
                title = 'Password Incorreta'
                window = MessageWindow(title, messages)
                open_new_window(window)
        else:
            self.user_info['username'] = username
            self.user_info['admin_status'] = self.admin_check
            self.set_app_widget()
            
    def set_menubar(self):
        menubar = self.menuBar()
        menubar.setFont(FONT_TYPE)
        
        user_menu = menubar.addMenu('Utilizador')
        cat_prod_menu = menubar.addMenu('Cateorias/Produtos')
        options_menu = menubar.addMenu('Opções')
        
        add_user_action = QAction('Criar Utilizador', self)
        user_options_action = QAction('Opções de Utilizador', self)
        user_menu.addAction(add_user_action)
        user_menu.addAction(user_options_action)
        
        category_action = QAction('Adiconar/Editar Categorias', self)
        add_product_action = QAction('Adiconar Produto', self)
        edit_cat_prod_action = QAction('Editar/Remover Produtos', self)
        cat_prod_menu.addAction(category_action)
        cat_prod_menu.addAction(add_product_action)
        cat_prod_menu.addAction(edit_cat_prod_action)
                
        set_iva_action = QAction('IVA', self)
        options_menu.addAction(set_iva_action)
        
        add_user_action.triggered.connect(lambda: open_new_window(UserWindow()))
        user_options_action.triggered.connect(open_editable_UserWindow)
        category_action.triggered.connect(lambda: open_new_window(SetEditCategoryWindow()))
        add_product_action.triggered.connect(open_AddProductWindow)
        edit_cat_prod_action.triggered.connect(lambda: open_new_window(EditRemoveProdutcsWindow()))
        set_iva_action.triggered.connect(lambda: open_new_window(SetEditIVAWindow()))
                
        # print_button.clicked.connect(lambda: print(CurrentUserInfo.get_user_info(CurrentUserInfo)))
         
# class UserLoginWindow(QMainWindow):
#     def __init__(self, users: list):
#         self.users_list = users
#         super(UserLoginWindow, self).__init__()
#         self.setFont(FONT_TYPE)
#         self.setStyleSheet(STYLE)

        
    
        
#     def set_widgets_placements(self):
#         self.setGeometry(200, 200, 450, 200)
#         self.setWindowTitle('Selecionar Utilizador')
                
#         login_layout = QVBoxLayout()
#         self.setLayout(login_layout)

#         login_fields_layout = QGridLayout()
#         login_buttons_layout = QHBoxLayout()
#         login_layout.addLayout(login_fields_layout)
#         login_layout.addLayout(login_buttons_layout)
        
#         login_user_label = QLabel('Utilizador')
#         self.login_user_combo_box = RoundedComboBox()
#         self.login_password_label = QLabel('Password')
#         self.login_password_line_edit = RoundedLeftLineEdit()
#         self.login_enter_button = HighOptionsButton('Login')
#         login_close_button = HighOptionsButton('Fechar')
        
#         for user in self.users_list:
#             self.login_user_combo_box.addItem(user)
        
#         self.login_user_combo_box.setCurrentIndex(-1)
#         self.login_user_combo_box.currentIndexChanged.connect(self.password_field_check)
#         self.login_password_line_edit.setEchoMode(RoundedLeftLineEdit.EchoMode.Password)
        
#         self.login_password_label.hide()
#         self.login_password_line_edit.hide()
        

        
#         login_fields_layout.addWidget(login_user_label, 0, 0)
#         login_fields_layout.addWidget(self.login_user_combo_box, 0, 1)
#         login_fields_layout.addWidget(self.login_password_label, 1, 0)
#         login_fields_layout.addWidget(self.login_password_line_edit, 1, 1)
#         login_buttons_layout.addWidget(self.login_enter_button)
#         login_buttons_layout.addWidget(login_close_button)
        
#         self.login_enter_button.clicked.connect(self.login_check)
#         login_close_button.clicked.connect(self.close)
        
#     def password_field_check(self):
#         self.admin_check = check_if_admin_by_username(session, self.login_user_combo_box.currentText())
#         if self.admin_check:
#             self.login_password_label.show()
#             self.login_password_line_edit.show()
#         else:
#             self.login_password_label.hide()
#             self.login_password_line_edit.hide() 
        
#     def login_check(self):
#         username =  self.login_user_combo_box.currentText()
#         if self.admin_check:
#             password = self.login_password_line_edit.text()
#             db_hashed_password = get_user_password_by_username(session, username)
#             messages = verify_hashed_password(password, db_hashed_password)
#             if not messages:
#                 CurrentUserInfo.set_user_info(CurrentUserInfo, username, self.admin_check)
#             else:
#                 title = 'Password Incorreta'
#                 window = MessageWindow(title, messages)
#                 open_new_window(window)
#         else:
#             CurrentUserInfo.set_user_info(CurrentUserInfo, username, self.admin_check)
        
#         self.close()
#         window = POSMainWindow()
#         open_new_window()
#         # try:    
#         #     print(CurrentUserInfo.get_user_info(CurrentUserInfo))
#         # except:
#         #     pass
                    
# # def make_login_status(username: str, admin_status: bool):
# #     login_status = LoginUser(username, admin_status)
# #     return login_status

# def login_enter():
#     users = get_users_usernames(session)
#     if not users:
#         no_users_window()
#     else:
#         login = UserLoginWindow(users)
#         open_new_window(login)