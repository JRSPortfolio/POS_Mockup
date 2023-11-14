from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QLabel, QStackedWidget,
                             QFormLayout, QGridLayout, QCheckBox, QTableView, QSpinBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QResizeEvent, QStandardItem

from gui.pos_add_models import (UserWindow, SetEditCategoryWindow, open_AddProductWindow, SetEditIVAWindow, SetCompanyInfo)
from gui.pos_edit_models import EditRemoveProdutcsWindow
from gui.pos_custom_widgets import(STYLE, MessageWindow, SquareOptionsButton, PaymentSectionButton,
                                   FONT_TYPE, RoundedComboBox, RoundedLeftLineEdit, HighOptionsButton, CategorySectionButton,
                                   POSDialog, ReadOnlyItemModel, SmallOptionsButton, TinyAddButton, TinyRemButton, LargeThinButton,
                                   SalesTotalFrame, ProductListingUpButton, ProductListingDownButton, NoUsersOptionWindow)
from database.pos_crud_and_validations import (get_users_usernames, check_if_admin_by_username, verify_hashed_password,
                                               get_user_password_by_username, create_hash_password, get_categories_list,
                                               get_products_from_category, change_favorite_product_stauts,
                                               get_favorite_products, get_product_sale_fields, check_users_exist, get_dados_empresa,
                                               )
from gui.pos_mainwindow_gui_options import FavoritesWindow, ChangeProductSaleQuantity
from database.mysql_engine import session
from decimal import Decimal as dec
    
class POSMainWindow(QMainWindow):
    def __init__(self):
        self.user_info = {'admin_status' : False}
        self.users_list = get_users_usernames(session)
        self.dados_empresa = get_dados_empresa(session)
        super(POSMainWindow, self).__init__()
        self.setFont(FONT_TYPE)
        self.setStyleSheet(STYLE)
        self.set_window_placements()
        self.set_menubar()
        
        # if self.user_info:
        #     self.set_app_widget()
        # else:
        self.set_login_options()
            
        # self.set_app_widget()
        
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
        mainWidgetsLayout = QHBoxLayout(self.mainWindowWidgets)
        leftLayout = QVBoxLayout()
        rightLayout = QVBoxLayout()
        mainWidgetsLayout.addLayout(leftLayout)
        mainWidgetsLayout.addLayout(rightLayout)
        
        categoriesBox = QGroupBox("Categorias")
        productsBox = QGroupBox("Produtos")
        optionsBox = QGroupBox("Opções")
        salesBox = QGroupBox("Vendas")
        paymentBox = QGroupBox("Pagamento")
        
        optionsBox.setFixedHeight(120)
        paymentBox.setFixedSize(400, 120)
        categoriesBox.setMinimumHeight(150)
        categoriesBox.setMaximumHeight(250)
        salesBox.setFixedWidth(400)
        
        
        leftLayout.addWidget(categoriesBox)
        leftLayout.addWidget(productsBox)
        leftLayout.addWidget(optionsBox)
        rightLayout.addWidget(salesBox)
        rightLayout.addWidget(paymentBox)
        
        categories_section_layout = QVBoxLayout()
        products_section_layout = QVBoxLayout()
        self.options_section_layout = QHBoxLayout()
        sales_section_layout = QVBoxLayout()
        self.payment_section_layout = QHBoxLayout()
                
        categoriesBox.setLayout(categories_section_layout)
        productsBox.setLayout(products_section_layout)
        optionsBox.setLayout(self.options_section_layout)
        salesBox.setLayout(sales_section_layout)
        paymentBox.setLayout(self.payment_section_layout)
                
        self.categories_header_layout = QGridLayout()
        self.categories_buttons_layout = QGridLayout()
        self.products_buttons_layout = QGridLayout()
        self.product_quantities_layout = QHBoxLayout()
        sales_listing_layout = QHBoxLayout()
        self.sales_table_items_layout = QVBoxLayout()
        self.sales_table_button_layout = QVBoxLayout()
        self.sales_total_layout = QHBoxLayout()
        self.sales_buttons_layout = QHBoxLayout()
        
        categories_section_layout.addLayout(self.categories_header_layout)
        categories_section_layout.addLayout(self.categories_buttons_layout)
        products_section_layout.addLayout(self.products_buttons_layout)
        products_section_layout.addLayout(self.product_quantities_layout)
        sales_section_layout.addLayout(sales_listing_layout)
        sales_section_layout.addLayout(self.sales_total_layout)
        sales_section_layout.addLayout(self.sales_buttons_layout)
        
        sales_listing_layout.addLayout(self.sales_table_items_layout)
        sales_listing_layout.addLayout(self.sales_table_button_layout)
        
        self.sales_total_value = SalesTotalFrame()
        self.sales_total_layout.addWidget(self.sales_total_value)
                
        self.set_categories()
                
        self.set_options_section()
        self.set_payment_section()
        self.set_sales_section()
        
        mainWidgetsLayout.setStretchFactor(leftLayout, 4)
        mainWidgetsLayout.setStretchFactor(rightLayout, 2)
        
    def set_sales_section(self):
        self.set_sales_table()
                
        change_product_quantity = LargeThinButton('Alterar Quantidade')
        remove_single_product = TinyRemButton('')
        add_single_product = TinyAddButton('')
        remove_product = SmallOptionsButton('Remover')
        clean_sales_list = SmallOptionsButton('Limpar')
        
        self.sales_buttons_layout.addWidget(change_product_quantity, alignment = Qt.AlignmentFlag.AlignHCenter)
        self.sales_buttons_layout.addWidget(remove_single_product, alignment = Qt.AlignmentFlag.AlignHCenter)
        self.sales_buttons_layout.addWidget(add_single_product, alignment = Qt.AlignmentFlag.AlignLeft)
        self.sales_buttons_layout.addWidget(remove_product, alignment = Qt.AlignmentFlag.AlignHCenter)
        self.sales_buttons_layout.addWidget(clean_sales_list, alignment = Qt.AlignmentFlag.AlignRight)
                
        self.sales_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        
        change_product_quantity.clicked.connect(self.open_change_quantity_window)
        remove_single_product.clicked.connect(self.remove_single_quantity_from_sales)
        add_single_product.clicked.connect(lambda: self.add_product_quantity_in_sales_table(1))
        remove_product.clicked.connect(self.remove_product_from_sales)
        clean_sales_list.clicked.connect(self.clean_sales_listing)
        
        upper_product_selection = ProductListingUpButton()
        down_product_selection = ProductListingDownButton()
        
        self.sales_table_button_layout.addWidget(upper_product_selection, alignment = Qt.AlignmentFlag.AlignBottom)
        self.sales_table_button_layout.addWidget(down_product_selection, alignment = Qt.AlignmentFlag.AlignTop)
        
        upper_product_selection.clicked.connect(self.select_upper_product)
        down_product_selection.clicked.connect(self.select_down_product)
        
        
    def set_sales_table(self):
        self.sales_table_view = QTableView()
        self.sales_table_view.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.sales_table_model = ReadOnlyItemModel()
        
        headers = ['Produto', 'IVA', 'Qtd.', 'Preço']
        
        self.sales_table_model.setColumnCount(4)
        self.sales_table_model.setHorizontalHeaderLabels(headers)
                
        self.sales_table_view.setModel(self.sales_table_model)
        self.sales_table_view.verticalHeader().hide()
        self.sales_table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        
        self.sales_table_view.setColumnWidth(0, 180)
        self.sales_table_view.setColumnWidth(1, 50)
        self.sales_table_view.setColumnWidth(2, 50)
        self.sales_table_view.setColumnWidth(3, 72)
        
        self.sales_table_items_layout.addWidget(self.sales_table_view)
        self.sales_table_view.show()
        
    def mousePressEvent(self, event):
        if not self.sales_table_view.rect().contains(self.sales_table_view.mapFromGlobal(event.globalPosition()).toPoint()):
            self.sales_table_view.clearSelection()
                
    def set_options_section(self):
        user_button = SquareOptionsButton('Utilizador')
        favorites_button = SquareOptionsButton('Favoritos')
        
        self.options_section_layout.addWidget(user_button)
        self.options_section_layout.addWidget(favorites_button)
        
        self.options_section_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        user_button.clicked.connect(self.set_login_options)
        favorites_button.clicked.connect(lambda: self.open_qdialog(FavoritesWindow(self.user_info['username'])))
        
    def set_login_options(self):
        if not check_users_exist(session):
            self.no_users_window()
        self.baseWidget.setCurrentIndex(1)
        self.login_user_combo_box.setCurrentIndex(-1)
        self.setWindowTitle("POS")
    
    def set_payment_section(self):
        print_button = PaymentSectionButton('Imprimir Recibo')
        payment_button = PaymentSectionButton('Pagamento')

        self.payment_section_layout.addWidget(print_button)
        self.payment_section_layout.addWidget(payment_button)
        
        print_button.clicked.connect(self.print_sales_listed_items)
    
    def set_categories(self):
        self.favorites_button = CategorySectionButton('Favoritos')
        self.multiple_categories_check_box = QCheckBox('Selecionar Mais que uma Categoria')
        
        self.favorites_button.setCheckable(True)
        
        self.categories_header_layout.addWidget(self.favorites_button, 0, 0)
        self.categories_header_layout.addWidget(self.multiple_categories_check_box, 0, 1, Qt.AlignmentFlag.AlignRight)
        self.favorites_button.clicked.connect(lambda _, category = 'favorites': self.select_categories(category))
        self.multiple_categories_check_box.stateChanged.connect(self.multiple_categories_set_check)
                                            
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
        
        try:
            checked_categories = self.check_checked_categories()
        except AttributeError:
            checked_categories = None
        
        self.categories_buttons = {'favorites' : self.favorites_button}
        row = 1
        col = 0
        for category in categories_list:
            button = CategorySectionButton(category)
            self.categories_buttons[category] = button
            self.categories_buttons_layout.addWidget(self.categories_buttons[category], row, col)
            self.categories_buttons[category].setCheckable(True)
            self.categories_buttons[category].clicked.connect(lambda _, category = category: self.select_categories(category))
            if checked_categories:
                if category in checked_categories:
                    self.categories_buttons[category].setChecked(True)
            col += 1
            if col == max_cols:
                col = 0
                row += 1
                
    def check_checked_categories(self):
        categories = []
        for category in self.categories_buttons.keys():
            if self.categories_buttons[category].isChecked():
                categories.append(category)
        return categories
                    
    def multiple_categories_set_check(self):
        if not self.multiple_categories_check_box.isChecked():
            for category in self.categories_buttons.keys():
                self.categories_buttons[category].setChecked(False)
                                                 
    def select_categories(self, category: str):
        cols = self.products_buttons_layout.columnCount()
        self.clean_product_buttons(cols)
        
        if not self.multiple_categories_check_box.isChecked():
            for button in self.categories_buttons.keys():
                if button != category:
                    self.categories_buttons[button].setChecked(False)
            
                    
        self.set_products_positions(6)
        
    def set_products_quantities_options(self):
        quantity_label = QLabel('Quantidade:')
        self.product_quantity_spin_box = QSpinBox()
        
        self.product_quantity_spin_box.setFixedWidth(50)
        self.product_quantity_spin_box.setMinimum(1)
        self.product_quantity_spin_box.setValue(1)
                
        self.product_quantities_layout.addWidget(quantity_label)
        self.product_quantities_layout.addWidget(self.product_quantity_spin_box)
        
        self.product_quantities_layout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
        
    def clean_product_quantities_options(self):
        while self.product_quantities_layout.count() > 0:
            item = self.product_quantities_layout.takeAt(0)
            if item:
                widget = item.widget()
                self.product_quantities_layout.removeItem(item)
                widget.deleteLater()
         
    def set_products_positions(self, max_cols: int): 
        row = 0
        col = 0    
        
        products_listing_button = {}
        
        if self.categories_buttons['favorites'].isChecked():
            favorites_dict = get_favorite_products(session, self.user_info['username'])
            if col != 0:
                col = 0
                row += 1
                
            for prod_id in favorites_dict.keys():
                button = SquareOptionsButton(f'{favorites_dict[prod_id][0]} ({favorites_dict[prod_id][1]}€)')
                products_listing_button[prod_id] = button
                self.products_buttons_layout.addWidget(products_listing_button[prod_id], row, col)
                products_listing_button[prod_id].clicked.connect(lambda _, prod_id = prod_id: self.add_product_to_sale_table(prod_id))
                col += 1
                if col == max_cols:
                    col = 0
                    row += 1
    
        products_dict = {}
        for category in self.categories_buttons.keys():
            if category != 'favorites':
                if self.categories_buttons[category].isChecked():
                    products_dict[category] = get_products_from_category(session, category)
                    if col != 0:
                        col = 0
                        row += 1
                    
                    for prod_id in products_dict[category].keys():
                        if prod_id not in products_listing_button.keys():
                            button = SquareOptionsButton(f'{products_dict[category][prod_id][0]} ({products_dict[category][prod_id][1]}€)')
                            products_listing_button[prod_id] = button
                            self.products_buttons_layout.addWidget(products_listing_button[prod_id], row, col)
                            products_listing_button[prod_id].clicked.connect(lambda _, prod_id = prod_id: self.add_product_to_sale_table(prod_id))
                            col += 1
                            if col == max_cols:
                                col = 0
                                row += 1
        
        if self.product_quantities_layout.count() == 0 and products_listing_button:
            self.set_products_quantities_options()
        elif not products_listing_button:
            self.clean_product_quantities_options()
            
    def add_product_to_sale_table(self, prod_id: int):
        if self.sales_table_model.rowCount() == 0:
            self.transaction_products = []
        
        product = get_product_sale_fields(session, prod_id)
        product[2] += self.product_quantity_spin_box.value()
        product.append(prod_id)
        self.transaction_products.append(product)
        
        total_price = str(dec(product[2]) * product[3])
        
        row_items = [QStandardItem(product[0]), QStandardItem(str(product[1])), QStandardItem(str(product[2])), QStandardItem(total_price)]
        
        for item in row_items[1:]:
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.sales_table_model.appendRow(row_items)
        
        self.product_quantity_spin_box.setValue(1)
        
        self.get_total_values()
        
    def update_product_sale_row(self, row):
        col_index = self.sales_table_view.selectedIndexes()
        self.sales_table_model.setData(col_index[2], self.transaction_products[row][2], Qt.ItemDataRole.EditRole)
        total_price = str(self.transaction_products[row][2] * self.transaction_products[row][3])
        self.sales_table_model.setData(col_index[3], total_price, Qt.ItemDataRole.EditRole)
        
    def remove_single_quantity_from_sales(self):
        row = self.get_selected_sales_listing_row()
        if row or row == 0:
            if self.transaction_products[row][2] > 1:
                self.transaction_products[row][2] -= 1
                self.update_product_sale_row(row)
                self.get_total_values()
            else:
                self.remove_product_from_sales()
                            
    def remove_product_from_sales(self):
        row = self.get_selected_sales_listing_row()
        if row or row == 0:
            self.sales_table_model.removeRow(row)
            self.transaction_products.pop(row)
            self.get_total_values()
        
        
    def add_product_quantity_in_sales_table(self, quantity: int):
        row = self.get_selected_sales_listing_row()
        if row or row == 0:
            self.transaction_products[row][2] += quantity
            self.update_product_sale_row(row)
            self.get_total_values()
            
    def replace_product_quantity_in_sales_table(self, quantity: int):
        row = self.get_selected_sales_listing_row()
        if quantity == 0:
            self.remove_product_from_sales()
        else:
            self.transaction_products[row][2] = quantity
            self.update_product_sale_row(row)
            self.get_total_values()
            
    def select_upper_product(self):
        row = self.get_selected_sales_listing_row()
        row_number = self.sales_table_model.rowCount()
            
        if row:
            if row == 0:
                row = row_number - 1
            else:
                row -= 1
            self.sales_table_view.selectRow(row)
        else:
            self.sales_table_view.selectRow(row_number - 1)
                
    def select_down_product(self):
        row = self.get_selected_sales_listing_row()
        if row or row == 0:
            if row == self.sales_table_model.rowCount() - 1:
                row = 0
            else:
                row += 1   
            self.sales_table_view.selectRow(row)
        else:
            self.sales_table_view.selectRow(0)
            
    def get_selected_sales_listing_row(self):
        index = self.sales_table_view.selectionModel().selectedRows()
        if index:
            row = index[0].row()
            return row
        else:
            return None
            
    def get_total_values(self):
        total = 0
        for product in self.transaction_products:
            total += (product[2] * product[3])

        self.sales_total_value.update_value(total)
        
    def open_change_quantity_window(self):
        row = self.get_selected_sales_listing_row()
        if row or row == 0:
            product = self.transaction_products[row][0]
            quantity = self.transaction_products[row][2]
            window = ChangeProductSaleQuantity(product, quantity)
            self.open_qdialog(window)
            
    def clean_sales_listing(self):
        while self.sales_table_model.rowCount():
            self.sales_table_model.removeRow(0)
            self.transaction_products.pop(0)
        self.get_total_values()
                                                                
    def clean_product_buttons(self, max_cols: int):
        existing_cols = self.products_buttons_layout.columnCount()
        for row in range(self.products_buttons_layout.rowCount()):
            if max_cols < existing_cols:
                for col in range(existing_cols):
                    item = self.products_buttons_layout.itemAtPosition(row, col)
                    if item:
                        widget = item.widget()
                        self.products_buttons_layout.removeItem(item)
                        widget.deleteLater()
            else:
                for col in range(max_cols):        
                    item = self.products_buttons_layout.itemAtPosition(row, col)
                    if item:
                        widget = item.widget()
                        self.products_buttons_layout.removeItem(item)
                        widget.deleteLater()
                        
    def set_app_widget(self):
        self.baseWidget.setCurrentIndex(0)
        self.setWindowTitle(f"{self.dados_empresa['nome']} - {self.user_info['username']}")
        
    def set_login_widgets(self):
        login_layout = QVBoxLayout(self.loginWidget)

        login_fields_layout = QFormLayout()
        login_buttons_layout = QHBoxLayout()
        login_layout.addLayout(login_fields_layout)
        login_layout.addLayout(login_buttons_layout)
        
        login_user_label = QLabel('Utilizador')
        self.login_user_combo_box = RoundedComboBox()
        self.login_password_label = QLabel('Password')
        self.login_password_line_edit = RoundedLeftLineEdit()
        login_enter_button = HighOptionsButton('Login')
        login_close_button = HighOptionsButton('Fechar')
        
        self.set_user_login_combo_box()

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
        login_buttons_layout.addWidget(login_enter_button)
        login_buttons_layout.addWidget(login_close_button)
        
        login_enter_button.clicked.connect(self.login_check)
        login_close_button.clicked.connect(self.close)
        
    def set_user_login_combo_box(self):
        self.login_user_combo_box.clear()
        for user in self.users_list:
            self.login_user_combo_box.addItem(user)
        self.login_user_combo_box.setCurrentIndex(-1)
        
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
        if username:
            if self.admin_check:
                password = self.login_password_line_edit.text()
                db_hashed_password = get_user_password_by_username(session, username)
                messages = verify_hashed_password(password, db_hashed_password)
                if not messages:
                    self.user_info['username'] = username
                    self.user_info['admin_status'] = self.admin_check
                    self.login_password_line_edit.clear()
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
            
            

            prod_cols = self.products_buttons_layout.columnCount()
            for category in self.categories_buttons.keys():
                self.categories_buttons[category].setChecked(False)
            if prod_cols:
                self.clean_product_buttons(prod_cols)
            if self.sales_table_model.rowCount() != 0:
                self.clean_sales_listing()
                
    def open_editable_UserWindow(self):
        title = 'Utilizador'
        user_cb = 'Ativo'
        create_button = 'Editar Utilizador'
        edit = check_users_exist(session)
        if not edit:
            self.no_users_window()
        else:   
            window = UserWindow(title = title, user_cb = user_cb, create_button = create_button,
                                edit = edit)
            self.open_qdialog_admin(window)

    def no_users_window(self):
        title = 'Sem Utilizadores'
        message = 'Sem Utilizadore criados, criar Utilizador?'
        create_button = 'Criar Utilizador'
        options_window = NoUsersOptionWindow(self.open_qdialog, title, message, create_button, UserWindow())
        self.open_qdialog(options_window)
            
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
        
        set_edit_company = QAction('Dados Empresa', self)
        set_iva_action = QAction('IVA', self)
        options_menu.addAction(set_edit_company)
        options_menu.addAction(set_iva_action)
        
        add_user_action.triggered.connect(lambda: self.open_qdialog(UserWindow()))
        user_options_action.triggered.connect(self.open_editable_UserWindow)
        category_action.triggered.connect(lambda: self.open_qdialog_admin(SetEditCategoryWindow()))
        add_product_action.triggered.connect(lambda: open_AddProductWindow(self.open_qdialog_admin))
        edit_cat_prod_action.triggered.connect(lambda: self.open_qdialog_admin(EditRemoveProdutcsWindow()))
        set_edit_company.triggered.connect(self.set_company_data)
        set_iva_action.triggered.connect(lambda: self.open_qdialog_admin(SetEditIVAWindow()))
    
    def set_company_data(self):
        self.open_qdialog_admin(SetCompanyInfo(self.dados_empresa))
        self.dados_empresa = get_dados_empresa(session)
        self.setWindowTitle(f"{self.dados_empresa['nome']} - {self.user_info['username']}")
              
    def resizeEvent(self, a0: QResizeEvent | None) -> None:        
        self.in_resize()
        return super().resizeEvent(a0)
    
    def in_resize(self):
        window_width = self.width()

        if window_width < 1000:
            cat_max_cols = 3
        elif window_width >= 1000 and window_width < 1200:
            cat_max_cols = 4
        elif window_width >= 1200 and window_width < 1400:
            cat_max_cols = 5
        elif window_width >= 1400:
            cat_max_cols = 6
        
        if window_width < 900:
            product_max_cols = 4  
        if window_width >= 900 and window_width < 1000:
            product_max_cols = 5
        elif window_width >= 1000 and window_width < 1100:
            product_max_cols = 6
        elif window_width >= 1100 and window_width < 1200:
            product_max_cols = 7
        elif window_width >= 1200 and window_width < 1300:
            product_max_cols = 8
        elif window_width >= 1300 and window_width < 1400:
            product_max_cols = 9
        elif window_width > 1400:
            product_max_cols = 10
            
        if self.categories_buttons_layout.columnCount() > 0:
            self.clean_categories(cat_max_cols)
            self.position_categories(cat_max_cols)
            if self.products_buttons_layout.columnCount() > 0:
                self.clean_product_buttons(product_max_cols)
                self.set_products_positions(product_max_cols)
        
    def update_window_on_signal(self, data):
        if isinstance(data, int):
            self.replace_product_quantity_in_sales_table(data)
        else:
            match data:
                case 'categories':
                    cols = self.categories_buttons_layout.columnCount()
                    self.clean_categories(cols)
                    self.position_categories(cols)
                case 'products' | 'favorites':
                    cols = self.products_buttons_layout.columnCount()
                    self.clean_product_buttons(cols)
                    self.set_products_positions(cols)
                case 'username':
                    self.users_list = get_users_usernames(session)
                    self.set_user_login_combo_box()
                    if not self.users_list:
                        self.set_login_options()
              
    def open_qdialog_admin(self, new_window: POSDialog):
        if self.user_info['admin_status']:
            self.open_qdialog(new_window)
        else:
            title = 'Sem Permissão'
            message = ['É necessário permissões de administrador para efectuar esta acção!']
            window = MessageWindow(title, message)
            self.open_qdialog(window)

    def open_qdialog(self, new_window: POSDialog):
        open_qdialog = new_window
        open_qdialog.qdialog_signal.connect(self.update_window_on_signal)
        open_qdialog.exec()

    def print_sales_listed_items(self):        
        ...

