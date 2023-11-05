# from PyQt6.QtCore import 
# from PyQt6.QtGui import 
import typing
from PyQt6 import QtGui
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QLabel,
                             QStackedWidget, QFormLayout, QGridLayout, QCheckBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QResizeEvent
import sys
from gui.pos_add_models import (UserWindow, SetEditCategoryWindow, open_AddProductWindow,
                                SetEditIVAWindow, open_editable_UserWindow)
from gui.pos_edit_models import EditRemoveProdutcsWindow
from gui.pos_custom_widgets import(STYLE, MessageWindow, OptionsSectionButton, PaymentSectionButton,
                                   FONT_TYPE, RoundedComboBox, RoundedLeftLineEdit, HighOptionsButton, CategorySectionButton,
                                   POSDialog)
from database.pos_crud_and_validations import (get_users_usernames, check_if_admin_by_username, verify_hashed_password,
                                               get_user_password_by_username, create_hash_password, get_categories_list)
from database.mysql_engine import session
    
class POSMainWindow(QMainWindow):
    def __init__(self):
        self.user_info = {}
        self.users_list = get_users_usernames(session)
        super(POSMainWindow, self).__init__()
        self.setFont(FONT_TYPE)
        self.setStyleSheet(STYLE)
        self.set_window_placements()
        self.set_menubar()
        
        # if self.user_info:        ######### disabled for easing of testing
        #     self.set_app_widget()
        # else:
        #     self.set_login_widget()
            
        self.set_app_widget()
        
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
        paymentBox.setFixedSize(390, 120)
        categoriesBox.setMinimumHeight(150)
        categoriesBox.setMaximumHeight(250)
        salesBox.setFixedWidth(390)
        
        
        self.leftLayout.addWidget(categoriesBox)
        self.leftLayout.addWidget(productsBox)
        self.leftLayout.addWidget(optionsBox)
        self.rightLayout.addWidget(salesBox)
        self.rightLayout.addWidget(paymentBox)
        
        self.categories_section_layout = QVBoxLayout()
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
        
        self.categories_header_layout = QGridLayout()
        self.categories_buttons_layout = QGridLayout()
        
        self.categories_section_layout.addLayout(self.categories_header_layout)
        self.categories_section_layout.addLayout(self.categories_buttons_layout)
        
        self.set_categories()
        
        self.mainWidgetsLayout.setStretchFactor(self.leftLayout, 4)
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
    
    def set_categories(self):
        self.favorites_button = CategorySectionButton('Favoritos')
        self.multiple_categories_check_box = QCheckBox('Selecionar Mais que uma Categoria')
        
        self.categories_header_layout.addWidget(self.favorites_button, 0, 0)
        self.categories_header_layout.addWidget(self.multiple_categories_check_box, 0, 1, Qt.AlignmentFlag.AlignRight)
        self.favorites_button.clicked.connect(lambda: print('click'))
        self.multiple_categories_check_box.stateChanged.connect(lambda: print('check'))
                                            
    def clean_categories(self, max_cols: int):
        existing_cols = self.categories_buttons_layout.columnCount()

        for row in range(self.categories_buttons_layout.rowCount()):
            if max_cols < existing_cols:
                for col in range(existing_cols):
                    item = self.categories_buttons_layout.itemAtPosition(row, col)
                    if item:
                        widget = item.widget()
                        self.categories_buttons_layout.removeItem(item)
                        widget.deleteLater()
            else:
                for col in range(max_cols):        
                    item = self.categories_buttons_layout.itemAtPosition(row, col)
                    if item:
                        widget = item.widget()
                        self.categories_buttons_layout.removeItem(item)
                        widget.deleteLater()
    
    def position_categories(self, max_cols: int):
        categories_list = get_categories_list(session)
        
        self.categories_buttons = {}
        row = 1
        col = 0
        for category in categories_list:
            button = CategorySectionButton(category)
            self.categories_buttons[category] = button
            self.categories_buttons_layout.addWidget(self.categories_buttons[category], row, col)
            print(f'{row} --- {col}')
            self.categories_buttons[category].clicked.connect(lambda _, row = row, col = col: print(f'{row}  --  {col}'))
            col += 1
            if col == max_cols:
                col = 0
                row += 1
                
    def set_app_widget(self):
        self.baseWidget.setCurrentIndex(0)
        try:
            self.setWindowTitle(f"POS - {self.user_info['username']}")
        except:
            pass    ## remove try block later
        
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
                self.open_qdialog(window)
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
        
        add_user_action.triggered.connect(lambda: self.open_qdialog(UserWindow()))
        user_options_action.triggered.connect(open_editable_UserWindow)
        category_action.triggered.connect(lambda: self.open_qdialog(SetEditCategoryWindow()))
        add_product_action.triggered.connect(open_AddProductWindow)
        edit_cat_prod_action.triggered.connect(lambda: self.open_qdialog(EditRemoveProdutcsWindow()))
        set_iva_action.triggered.connect(lambda: self.open_qdialog(SetEditIVAWindow()))
                
    def resizeEvent(self, a0: QResizeEvent | None) -> None:        
        self.in_resize()
        return super().resizeEvent(a0)
    
    def in_resize(self):
        window_width = self.width()

        if window_width < 1000:
            max_cols = 3
        elif window_width >= 1000 and window_width < 1200:
            max_cols = 4
        elif window_width >= 1200 and window_width < 1400:
            max_cols = 5
        elif window_width >= 1400:
            max_cols = 6
            
        # print(f'before set {max_cols}')
        if self.categories_buttons_layout.columnCount() > 0:
            self.clean_categories(max_cols)
            self.position_categories(max_cols)
        # print(f'after set {max_cols}')
        
    def update_window_on_signal(self):
        cols = self.categories_buttons_layout.columnCount()
        self.clean_categories(cols)
        self.position_categories(cols)

    def open_qdialog(self, new_window: POSDialog):
        open_qdialog = new_window
        open_qdialog.qdialog_signal.connect(self.update_window_on_signal)
        open_qdialog.exec()
        