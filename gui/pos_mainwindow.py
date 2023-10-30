# from PyQt6.QtCore import 
# from PyQt6.QtGui import 
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
import sys
from gui.pos_add_models import (UserWindow, SetEditCategoryWindow, open_AddProductWindow,
                                SetEditIVAWindow, open_editable_UserWindow)
from gui.pos_edit_models import EditRemoveProdutcsWindow
from gui.pos_custom_widgets import(open_new_window, OptionsSectionButton, PaymentSectionButton, FONT_TYPE)
from gui.pos_custom_widgets import STYLE

class POSMainWindow(QMainWindow):
    def __init__(self):
        super(POSMainWindow, self).__init__()
        self.setFont(FONT_TYPE)
        self.setStyleSheet(STYLE)
        self.set_window_placements()
        self.set_menubar()
        self.set_options_section()
        self.set_payment_section()
        
    def set_window_placements(self):
        self.setGeometry(100, 100, 1000, 600)
        self.setWindowTitle("POS") 
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        
        centralLayout = QHBoxLayout(centralWidget)
        leftLayout = QVBoxLayout()
        rightLayout = QVBoxLayout()
        centralLayout.addLayout(leftLayout)
        centralLayout.addLayout(rightLayout)
        
        categoriesBox = QGroupBox("Categorias")
        productsBox = QGroupBox("Produtos")
        optionsBox = QGroupBox("Opções")
        salesBox = QGroupBox("Vendas")
        paymentBox = QGroupBox("Pagamento")
        
        optionsBox.setFixedHeight(120)
        paymentBox.setFixedHeight(120)
        categoriesBox.setFixedHeight(150)
        
        leftLayout.addWidget(categoriesBox)
        leftLayout.addWidget(productsBox)
        leftLayout.addWidget(optionsBox)
        rightLayout.addWidget(salesBox)
        rightLayout.addWidget(paymentBox)
        
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

        centralLayout.setStretchFactor(leftLayout, 3)
        centralLayout.setStretchFactor(rightLayout, 2)
        
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
        
    def set_options_section(self):
        user_button = OptionsSectionButton('Utilizador')        
        self.options_section_layout.addWidget(user_button)
        
    def set_payment_section(self):
        print_button = PaymentSectionButton('Imprimir Recibo')
        payment_button = PaymentSectionButton('Pagamento')

        self.payment_section_layout.addWidget(print_button)
        self.payment_section_layout.addWidget(payment_button)
    
        

        