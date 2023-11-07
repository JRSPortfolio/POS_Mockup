from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QLabel, QStackedWidget,
                             QFormLayout, QGridLayout, QCheckBox, QTableView, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QResizeEvent, QStandardItem

from gui.pos_add_models import (UserWindow, SetEditCategoryWindow, open_AddProductWindow,
                                SetEditIVAWindow, open_editable_UserWindow)
from gui.pos_edit_models import EditRemoveProdutcsWindow
from gui.pos_custom_widgets import(STYLE, MessageWindow, SquareOptionsButton, PaymentSectionButton,
                                   FONT_TYPE, RoundedComboBox, RoundedLeftLineEdit, HighOptionsButton, CategorySectionButton,
                                   POSDialog, ReadOnlyItemModel, TableSelectionUpButton, TableSelectionDownButton,FavoritesAddButton,
                                   FavoritesRemButton)
from database.pos_crud_and_validations import (get_users_usernames, check_if_admin_by_username, verify_hashed_password,
                                               get_user_password_by_username, create_hash_password, get_categories_list,
                                               get_products_from_category, get_products_for_favorite_listing, get_favorite_marked_products,
                                               change_favorite_product_stauts)
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
        self.products_section_layout = QGridLayout()
        self.options_section_layout = QHBoxLayout()
        self.sales_section_layout = QHBoxLayout()
        self.payment_section_layout = QHBoxLayout()
                
        self.options_section_layout.setContentsMargins(5, 0, 5, 0)
        self.options_section_layout.setAlignment(Qt.AlignmentFlag.AlignHorizontal_Mask)
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
        user_button = SquareOptionsButton('Utilizador')
        favorites_button = SquareOptionsButton('Favoritos')
        
        self.options_section_layout.addWidget(user_button)
        self.options_section_layout.addWidget(favorites_button)
        
        user_button.clicked.connect(self.set_login_widget)
        favorites_button.clicked.connect(lambda: self.open_qdialog(FavoritesWindow()))
        
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
        self.favorites_button.clicked.connect(lambda: print('Favorites click'))
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
        
        self.categories_buttons = {}
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
        cols = self.products_section_layout.columnCount()
        self.clean_products(cols)
        
        if not self.multiple_categories_check_box.isChecked():
            for button in self.categories_buttons.keys():
                if button != category:
                    self.categories_buttons[button].setChecked(False)
                    
        self.set_products_positions(6)
         
    def set_products_positions(self, max_cols: int):
        row = 0
        col = 0    
        
        self.products_listing_button = {}
        products_dict = {}
        
        for category in self.categories_buttons.keys():
            if self.categories_buttons[category].isChecked():
                products_dict[category] = get_products_from_category(session, category)
                if col != 0:
                    col = 0
                    row += 1
                
                for product in products_dict[category].keys():
                    button = SquareOptionsButton(products_dict[category][product])
                    self.products_listing_button[product] = button
                    self.products_section_layout.addWidget(self.products_listing_button[product], row, col)
                    self.products_listing_button[product].clicked.connect(lambda _, category = category, product = product: print(f'{category} -- {products_dict[category][product]}'))
                    col += 1
                    if col == max_cols:
                        col = 0
                        row += 1
        
    def clean_products(self, max_cols: int):
        existing_cols = self.products_section_layout.columnCount()
        for row in range(self.products_section_layout.rowCount()):
            if max_cols < existing_cols:
                for col in range(existing_cols):
                    item = self.products_section_layout.itemAtPosition(row, col)
                    if item:
                        widget = item.widget()
                        self.products_section_layout.removeItem(item)
                        widget.deleteLater()
            else:
                for col in range(max_cols):        
                    item = self.products_section_layout.itemAtPosition(row, col)
                    if item:
                        widget = item.widget()
                        self.products_section_layout.removeItem(item)
                        widget.deleteLater()
                        
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
            if self.products_section_layout.columnCount() > 0:
                self.clean_products(product_max_cols)
                self.set_products_positions(product_max_cols)
        
    def update_window_on_signal(self):
        cols = self.categories_buttons_layout.columnCount()
        self.clean_categories(cols)
        self.position_categories(cols)

    def open_qdialog(self, new_window: POSDialog):
        open_qdialog = new_window
        open_qdialog.qdialog_signal.connect(self.update_window_on_signal)
        open_qdialog.exec()
        
class FavoritesWindow(POSDialog):
    def set_widgets_placements(self):
        self.setGeometry(200, 200, 500, 700)
        self.setWindowTitle('Editar Favoritos')
        
        edit_favorites_layout = QVBoxLayout()
        self.setLayout(edit_favorites_layout)
        favorites_labels_layout = QHBoxLayout()
        favorites_tables_layout = QGridLayout()
        favorites_close_button_layout = QHBoxLayout()
        edit_favorites_layout.addLayout(favorites_labels_layout)
        edit_favorites_layout.addLayout(favorites_tables_layout)
        edit_favorites_layout.addLayout(favorites_close_button_layout)
        
        edit_favorites_category_label = QLabel('Categoria:')
        self.edit_favorites_category_combo_box = RoundedComboBox()
        self.select_product_table = QTableView()
        self.products_selection_up_button = TableSelectionUpButton()
        self.products_selection_down_button = TableSelectionDownButton()
        self.remove_favorite_button = FavoritesRemButton('')
        self.add_favorite_button = FavoritesAddButton('')
        self.favorites_table = QTableView()
        self.favorites_selection_up_button = TableSelectionUpButton()
        self.favorites_selection_down_button = TableSelectionDownButton()
        favorites_close_button = HighOptionsButton('Fechar')
        
        self.edit_favorites_category_combo_box.setFixedWidth(240)
        
        favorites_labels_layout.setContentsMargins(30, 0, 10, 0)
        self.select_product_table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.favorites_table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        
        category_list = get_categories_list(session)
        for category in category_list:
            self.edit_favorites_category_combo_box.addItem(category)
            
        self.edit_favorites_category_combo_box.setCurrentIndex(-1)
        
        
        self.products_row_number = 0
        self.favorites_row_number = 0
        
        favorites_labels_layout.addWidget(edit_favorites_category_label, Qt.AlignmentFlag.AlignRight)
        favorites_labels_layout.addWidget(self.edit_favorites_category_combo_box, Qt.AlignmentFlag.AlignLeft)
        
        favorites_tables_layout.addWidget(self.select_product_table, 0, 0, 2, 4)
        favorites_tables_layout.addWidget(self.products_selection_up_button, 0, 4, Qt.AlignmentFlag.AlignVCenter)
        favorites_tables_layout.addWidget(self.products_selection_down_button, 1, 4, Qt.AlignmentFlag.AlignVCenter)
        favorites_tables_layout.addWidget(self.remove_favorite_button, 2, 1, Qt.AlignmentFlag.AlignRight)
        favorites_tables_layout.addWidget(self.add_favorite_button, 2, 2, Qt.AlignmentFlag.AlignLeft)
        favorites_tables_layout.addWidget(self.favorites_table, 3, 0, 2, 4)
        favorites_tables_layout.addWidget(self.favorites_selection_up_button, 3, 4, Qt.AlignmentFlag.AlignVCenter)
        favorites_tables_layout.addWidget(self.favorites_selection_down_button, 4, 4, Qt.AlignmentFlag.AlignVCenter)
        
        favorites_close_button_layout.addWidget(favorites_close_button, Qt.AlignmentFlag.AlignHCenter)
        
        self.edit_favorites_category_combo_box.currentIndexChanged.connect(self.set_products_table_model)
        
        self.products_selection_up_button.clicked.connect(lambda: self.select_upper_row(self.select_product_table, self.products_row_number))
        self.products_selection_down_button.clicked.connect(lambda: self.select_down_row(self.select_product_table, self.products_row_number))
        
        self.remove_favorite_button.clicked.connect(self.set_favorite_stauts)
        self.add_favorite_button.clicked.connect(self.set_favorite_stauts)
        
        self.favorites_selection_up_button.clicked.connect(lambda: self.select_upper_row(self.favorites_table, self.favorites_row_number))
        self.favorites_selection_down_button.clicked.connect(lambda: self.select_down_row(self.favorites_table, self.favorites_row_number))
        
        self.select_product_table.clicked.connect(lambda: (self.favorites_table.clearSelection(), self.enable_disable_add_rem_buttons()))
        self.favorites_table.clicked.connect(lambda: (self.select_product_table.clearSelection(), self.enable_disable_add_rem_buttons()))
        
        favorites_close_button.clicked.connect(self.close)
        
        self.set_favorites_table_model()
        
    def set_products_table_model(self):
        self.products_table_model = ReadOnlyItemModel()        
        self.category = self.edit_favorites_category_combo_box.currentText().strip()
        
        headers = ['Produto', 'Preço', 'IVA', 'Favorito']
        self.product_contents = get_products_for_favorite_listing(session, self.category)
        
        self.products_row_number = len(self.product_contents.keys())
        
        self.products_table_model.setColumnCount(4)
        self.products_table_model.setRowCount(self.products_row_number)
        
        self.products_table_model.setHorizontalHeaderLabels(headers)
        
        row = 0
        for key in self.product_contents.keys():
            for col in range(4):
                item = QStandardItem(self.product_contents[key][col])
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.products_table_model.setItem(row, col, item)
            row += 1
                
        self.select_product_table.setModel(self.products_table_model)
        self.select_product_table.verticalHeader().hide()
        self.select_product_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        
        for col in range(len(headers)):
            self.select_product_table.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)

        self.select_product_table.show()

    def set_favorites_table_model(self):
        self.favorites_table_model = ReadOnlyItemModel()        
        
        headers = ['Produto', 'Preço', 'IVA', 'Favorito']
        self.favorite_contents = get_favorite_marked_products(session)
        
        self.favorites_row_number = len(self.favorite_contents.keys())
        
        self.favorites_table_model.setColumnCount(4)
        self.favorites_table_model.setRowCount(self.products_row_number)
        
        self.favorites_table_model.setHorizontalHeaderLabels(headers)
        
        row = 0
        for key in self.favorite_contents.keys():
            for col in range(4):
                item = QStandardItem(self.favorite_contents[key][col])
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.favorites_table_model.setItem(row, col, item)
            row += 1
                
        self.favorites_table.setModel(self.favorites_table_model)
        self.favorites_table.verticalHeader().hide()
        self.favorites_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        
        for col in range(len(headers)):
            self.favorites_table.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)

        self.favorites_table.show()
        
    def select_upper_row(self, table_view: QTableView, row_number: int):
        if table_view == self.select_product_table:
            self.favorites_table.clearSelection()
        else:
            self.select_product_table.clearSelection()
        
        row = self.get_selected_rows()
        if row or row == 0:
            if row == 0:
                row = row_number - 1
            else:
                row -= 1
            table_view.selectRow(row)
            self.enable_disable_add_rem_buttons()
        else:
            table_view.selectRow(row_number - 1)
            self.enable_disable_add_rem_buttons()

    def select_down_row(self, table_view: QTableView, row_number: int):
        if table_view == self.select_product_table:
            self.favorites_table.clearSelection()
        else:
            self.select_product_table.clearSelection()
        
        row = self.get_selected_rows()
        if row or row == 0:
            if row == row_number - 1:
                row = 0
            else:
                row += 1   
            table_view.selectRow(row)
            self.enable_disable_add_rem_buttons()
        else:
            table_view.selectRow(0)
            self.enable_disable_add_rem_buttons()
                 
    def get_selected_rows(self):
        if self.select_product_table.model() and self.select_product_table.selectionModel().selectedRows():
            rows = self.select_product_table.selectionModel().selectedRows()
        else:
            rows = self.favorites_table.selectionModel().selectedRows()
            
        if rows:
            index = rows[0]
            row = index.row()
            return row
        else:
            return None
        
    def enable_disable_add_rem_buttons(self):
        if self.favorites_table.model() and self.favorites_table.selectionModel().selectedRows():
            rows = self.favorites_table.selectionModel().selectedRows()
            if rows:
                self.add_favorite_button.setEnabled(False)
                self.remove_favorite_button.setEnabled(True)    
                
        elif self.select_product_table.model() is not None and self.select_product_table.selectionModel().selectedRows():
            rows = self.select_product_table.selectionModel().selectedRows()
            if rows:
                row = rows[0].row()
                value_index = self.products_table_model.index(row, 3)
                check = self.products_table_model.itemFromIndex(value_index).text()
            if check:
                self.add_favorite_button.setEnabled(False)
                self.remove_favorite_button.setEnabled(True)
            else:
                self.add_favorite_button.setEnabled(True)
                self.remove_favorite_button.setEnabled(False)
                    
    def set_favorite_stauts(self):
        row = self.get_selected_rows()
        if row or row == 0:
            if self.select_product_table.model() and self.select_product_table.selectionModel().selectedRows():
                name = self.products_table_model.index(row, 0).data()
                for key, product in self.product_contents.items():
                    if product[0] == name:
                        prod_id = key
                        if self.product_contents[key][3]:
                            set_favorite = False
                        else:
                            set_favorite = True
                        change_favorite_product_stauts(session, prod_id, set_favorite)
                        self.set_products_table_model()
                        self.set_favorites_table_model()
                        
            else:
                name = self.favorites_table_model.index(row, 0).data()
                for key, product in self.favorite_contents.items():
                    if product[0] == name:
                        prod_id = key
                        change_favorite_product_stauts(session, prod_id, False)
                        self.set_products_table_model()
                        self.set_favorites_table_model()

        
