from PyQt6.QtWidgets import (QHBoxLayout, QVBoxLayout, QLabel, QGridLayout, QTableView, QSpinBox, QHeaderView)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QStandardItem
from gui.pos_custom_widgets import(RoundedComboBox, HighOptionsButton, POSDialog, ReadOnlyItemModel,
                                   TableSelectionUpButton, TableSelectionDownButton,FavoritesAddButton,
                                   FavoritesRemButton)
from database.pos_crud_and_validations import (get_categories_list, get_products_from_category, 
                                               change_favorite_product_stauts, get_favorite_products)
from database.mysql_engine import session
from decimal import Decimal as dec

class ChangeProductSaleQuantity(POSDialog):
    qdialog_signal = pyqtSignal(int)
    def __init__(self, product: str, quantity: int, *args, **kwargs):
        self.product = product
        self.quantity = quantity
        super(ChangeProductSaleQuantity, self).__init__(*args, **kwargs)

    def set_widgets_placements(self):
        self.setGeometry(200, 200, 300, 200)
        self.setWindowTitle('Editar Quantidade')
        
        base_layout = QVBoxLayout()
        self.setLayout(base_layout)
        
        quantity_items_layout = QGridLayout()
        quantity_button_layout = QHBoxLayout()
        base_layout.addLayout(quantity_items_layout)
        base_layout.addLayout(quantity_button_layout)
        
        
        quantity_product_label = QLabel(self.product)
        quantity_amount_label = QLabel('Quantidade')
        self.quantity_spin_box = QSpinBox()
        self.quantity_change_button = HighOptionsButton('Alterar')
        quantity_close_button = HighOptionsButton('Fechar')
        
        self.quantity_spin_box.setMinimum(0)
        self.quantity_spin_box.setValue(self.quantity)
        
        quantity_items_layout.addWidget(quantity_product_label, 0, 0)
        quantity_items_layout.addWidget(quantity_amount_label, 1, 0)
        quantity_items_layout.addWidget(self.quantity_spin_box, 1, 1)
        quantity_button_layout.addWidget(self.quantity_change_button)
        quantity_button_layout.addWidget(quantity_close_button)
        
        self.quantity_change_button.clicked.connect(self.change_quantity)
        quantity_close_button.clicked.connect(self.close)
        
    def change_quantity(self):
        quantity = self.quantity_spin_box.value()
        self.emit_signal(quantity)
        self.close()
        
    def emit_signal(self, signal: int):
        self.qdialog_signal.emit(signal)


class FavoritesWindow(POSDialog):
    def __init__(self, username: str, *args, **kwargs):
        self.username = username
        super(FavoritesWindow, self).__init__(*args, **kwargs)
        
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
        
        self.select_product_table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.favorites_table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        
        category_list = get_categories_list(session)
        for category in category_list:
            self.edit_favorites_category_combo_box.addItem(category)
            
        self.edit_favorites_category_combo_box.setCurrentIndex(-1)
        
        
        self.products_row_number = 0
        self.favorites_row_number = 0
        
        favorites_labels_layout.addWidget(edit_favorites_category_label)
        favorites_labels_layout.addWidget(self.edit_favorites_category_combo_box)
        favorites_labels_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
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
        self.product_contents = get_products_from_category(session, self.category)
        favorite_products = get_favorite_products(session, self.username)
        
        self.products_row_number = len(self.product_contents.keys())
        
        self.products_table_model.setColumnCount(4)
        self.products_table_model.setRowCount(self.products_row_number)
        
        self.products_table_model.setHorizontalHeaderLabels(headers)
        
        row = 0
        for key in self.product_contents.keys():
            for col in range(3):
                value = self.product_contents[key][col]
                if isinstance(value, dec):
                    value = str(value)
                item = QStandardItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.products_table_model.setItem(row, col, item)
            if key in favorite_products.keys():
                mark = QStandardItem('X')
                mark.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.products_table_model.setItem(row, 3, mark)
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
        self.favorite_contents = get_favorite_products(session, self.username)        
        
        self.favorites_row_number = len(self.favorite_contents.keys())
        
        self.favorites_table_model.setColumnCount(4)
        self.favorites_table_model.setRowCount(self.favorites_row_number)
        
        self.favorites_table_model.setHorizontalHeaderLabels(headers)
        
        row = 0
        for key in self.favorite_contents.keys():
            for col in range(3):
                value = self.favorite_contents[key][col]
                if isinstance(value, dec):
                    value = str(value)
                item = QStandardItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.favorites_table_model.setItem(row, col, item)
            mark = QStandardItem('X')
            mark.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.favorites_table_model.setItem(row, 3, mark)
            row += 1
                
        self.favorites_table.setModel(self.favorites_table_model)
        self.favorites_table.verticalHeader().hide()
        self.favorites_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        
        for col in range(len(headers)):
            self.favorites_table.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)

        self.favorites_table.show()
        
    def mousePressEvent(self, event):
        if not self.select_product_table.rect().contains(self.select_product_table.mapFromGlobal(event.globalPosition()).toPoint()):
            self.select_product_table.clearSelection()
        if not self.favorites_table.rect().contains(self.favorites_table.mapFromGlobal(event.globalPosition()).toPoint()):
            self.favorites_table.clearSelection()
        
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
                for prod_id, product in self.product_contents.items():
                    if product[0] == name:
                        if prod_id in self.favorite_contents.keys():
                            change_favorite_product_stauts(session, prod_id, self.username, False)
                        else:
                            change_favorite_product_stauts(session, prod_id, self.username, True)
            else:
                name = self.favorites_table_model.index(row, 0).data()
                for prod_id, product in self.favorite_contents.items():
                    if product[0] == name:
                        change_favorite_product_stauts(session, prod_id, self.username, False)

            self.set_products_table_model()
            self.set_favorites_table_model()       
            self.emit_signal()

    def emit_signal(self):
        self.qdialog_signal.emit('favorites')