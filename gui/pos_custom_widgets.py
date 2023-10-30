from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QWidget, QComboBox, QTableView)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QStandardItemModel
from database.mysql_engine import session
from database.pos_crud_and_validations import get_stylesheet, get_last_product_order

FONT_TYPE = QFont("Segoe UI", 10, weight = -1)
FONT_TYPE_BOLD = QFont("Segoe UI", 10)
FONT_TYPE_BOLD.setWeight(QFont.Weight.Bold)
STYLE = get_stylesheet()

class POSDialog(QDialog):
    def __init__(self):
        super(POSDialog, self).__init__()
        self.setFont(FONT_TYPE)
        self.setStyleSheet(STYLE)
        if self.set_widgets_placements():
            self.set_widgets_placements()
            
class SetEditOptionsWindow(POSDialog):
    ###
    ### Required fileds in __init__:
    ### self.first_title_label_text -> str
    ### self.second_title_label_text -> str
    ### self.get_types_list -> get listing function
    ### self.list_label_text ->  str
    ### self.get_value_by_name -> retrieve value by name function
    ### self.change_by_name -> change row by name function
    ### self.remove_by_name -> remove by name function
    ###
    ### Usefull fields in super:
    ### self.setWindowTitle = 'Adicionar Taxa de IVA'
    ### self.setGeometry(200, 200, 500, 100)
    ###
    ###Required methods:
    ###def self.create_type(self):
    ###def self.validate_row(self, name:str , new_name: str, value: str, new_value: str):
    ###
    def set_widgets_placements(self):
        base_layout = QVBoxLayout()
        self.setLayout(base_layout)
        
        self.fields_layout = QGridLayout()
        buttons_layout = QHBoxLayout()
        base_layout.addLayout(self.fields_layout)
        base_layout.addLayout(buttons_layout)
        
        first_title_label = QLabel(self.first_title_label_text)
        self.first_line_edit = RoundedCenterLineEdit()
        second_title_label = QLabel(self.second_title_label_text)
        self.second_line_edit = RoundedCenterLineEdit()
        create_button = RoundedButton('Adicionar')
        placeholder = QWidget()
        close_button = HighOptionsButton('Fechar')
        
        first_title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        second_title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        create_button.setFixedSize(160, 22)
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
            edit_button = SmallOptionsButton('Editar')
            remove_button = SmallOptionsButton('Remover')
            
            name_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            value_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

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
        
        name_edit = RoundedCenterLineEdit()
        value_edit = RoundedCenterLineEdit()
        modify_button = SmallOptionsButton('Alterar')
        cancel_button = SmallOptionsButton('Cancelar')
        
        name_edit.setText(name_label.text())
        value_edit.setText(value_label.text())
        
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
        
        message_close_button = HighOptionsButton('Fechar')
        
        add_message_layout.addWidget(message_close_button, alignment = Qt.AlignmentFlag.AlignCenter)
        
        message_close_button.clicked.connect(lambda: self.close())
        
class MissingValueWindow(POSDialog):
    def __init__(self, title: str, message: str, button_title: str, add_value_window: POSDialog, aditional_button_title = None,
                 add_aditional_window = None):
        self.title = title
        self.message = message
        self.button_title = button_title
        self.add_value_window = add_value_window
        self.aditional_button_title = aditional_button_title
        self.add_aditional_window = add_aditional_window
        super(MissingValueWindow, self).__init__()
    
    def set_widgets_placements(self):
        self.setGeometry(200, 200, 300, 200)
        self.setWindowTitle(self.title)
        missing_value_layout = QGridLayout()
        self.setLayout(missing_value_layout)
        
        missing_value_message_label = QLabel(self.message)
        missing_value_window_button = HighLargeOptionsButton(self.button_title)
        missing_value_close_button = HighLargeOptionsButton('Fechar')
        
        missing_value_message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        missing_value_layout.addWidget(missing_value_message_label,0 ,0, 1, 2)
        
        if self.add_aditional_window is not None:
            aditional_window_button = HighLargeOptionsButton(self.aditional_button_title)
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
        
class NewProductOrderWindow(MissingValueWindow):
    def __init__(self, product_name = None, price = None, category = None, iva_value = None,
                 order_num = None, description = None, iva_checkbox = None, new_order_num = None,
                 existing_product_name = None, *args, **kwargs):
        self.product_name = product_name
        self.price = price
        self.category = category
        self.iva_value = iva_value
        self.order_num = order_num
        self.description = description
        self.iva_checkbox = iva_checkbox
        self.new_order_num = new_order_num
        self.existing_product_name = existing_product_name
        super(NewProductOrderWindow, self).__init__(*args, **kwargs)
        
    def open_window(self):
        self.close()
        self.add_value_window(self.product_name, self.price, self.category, self.iva_value, self.new_order_num, 
                              self.description, self.iva_checkbox)
    
    def open_aditional_window(self):
        self.close()
        self.add_aditional_window(self.product_name, self.price, self.category, self.iva_value, self.order_num,
                                  self.description, self.iva_checkbox, self.new_order_num, self.existing_product_name)
        
class EditProductOrderWindow(MissingValueWindow):
    def __init__(self, existing_name = None, category = None, existing_order = None, 
                 new_order = None, values = None, previous_category = None,
                 check = None, *args, **kwargs):
        self.existing_name = existing_name
        self.category = category
        self.existing_order = existing_order
        self.new_order = new_order
        self.values = values
        self.previous_category = previous_category
        self.check = check
        super(EditProductOrderWindow, self).__init__(*args, **kwargs)
        
    def open_window(self):
        self.close()

        if self.check:
            order_name = self.category + str(self.new_order)
            self.values['ordem'] = order_name
            
        if not self.values['ordem']:
            self.values['ordem'] = self.category + str(self.new_order)
  
        self.add_value_window(self.values, self.category)
    
    def open_aditional_window(self):
        self.close()
        if self.previous_category:
            self.add_aditional_window(self.existing_order, self.new_order, self.category,
                                      self. existing_name, self.values, self.previous_category)
        else:
            self.add_aditional_window(self.existing_order, self.new_order, self.category,
                                      self. existing_name, self.values)


class RoundedButton(QPushButton):
    def __init__(self, *args):
        super(RoundedButton, self).__init__(*args)
        
class SmallOptionsButton(RoundedButton):
    def __init__(self, *args):
        super(SmallOptionsButton, self).__init__(*args)
        self.setFont(FONT_TYPE)
        self.setFixedSize(80, 22)

class HighOptionsButton(RoundedButton):
    def __init__(self, *args):
        super(HighOptionsButton, self).__init__(*args)
        self.setFont(FONT_TYPE_BOLD)
        self.setFixedSize(140, 40)
        
class HighLargeOptionsButton(RoundedButton):
    def __init__(self, *args):
        super(HighLargeOptionsButton, self).__init__(*args)
        self.setFont(FONT_TYPE_BOLD)
        self.setFixedSize(170, 65)
        
class OptionsSectionButton(RoundedButton):
    def __init__(self, *args):
        super(OptionsSectionButton, self).__init__(*args)
        self.setFont(FONT_TYPE_BOLD)
        self.setFixedSize(75, 75)
        
class PaymentSectionButton(RoundedButton):
    def __init__(self, *args):
        super(PaymentSectionButton, self).__init__(*args)
        self.setFont(FONT_TYPE_BOLD)
        self.setFixedSize(140, 75)
        
class TableSelectionUpButton(RoundedButton):
    def __init__(self, *args):
        super(TableSelectionUpButton, self).__init__(*args)
        self.setFont(FONT_TYPE_BOLD)
        self.setFixedSize(30, 50)
        self.setIcon(QIcon("assets//move_up_arrow.png"))
        self.setIconSize(QSize(30, 45))
        
class TableSelectionDownButton(TableSelectionUpButton):
    def __init__(self, *args):
        super(TableSelectionUpButton, self).__init__(*args)
        self.setFont(FONT_TYPE_BOLD)
        self.setFixedSize(30, 50)
        self.setIcon(QIcon("assets//move_down_arrow.png"))
        self.setIconSize(QSize(30, 45))
        
class RoundedCenterLineEdit(QLineEdit):
    def __init__(self, *args):
        super(RoundedCenterLineEdit, self).__init__(*args)
        self.setFont(FONT_TYPE)
        self.setFixedHeight(22)
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        
class RoundedLeftLineEdit(QLineEdit):
    def __init__(self, *args):
        super(RoundedLeftLineEdit, self).__init__(*args)
        self.setFont(FONT_TYPE)
        self.setFixedHeight(22)

class RoundedComboBox(QComboBox):
    def __init__(self, *args):
        super(RoundedComboBox, self).__init__(*args)
        self.setFont(FONT_TYPE)
        self.setFixedHeight(22)
        
class ReadOnlyItemModel(QStandardItemModel):
    # def __init__(self, *args, **kwargs):
    #     super(ReadOnlyItemModel, self).__init__(*args, **kwargs)
    #     self.set_selection()
        
    def flags(self, index):
        flags = super().flags(index)
        flags &= ~Qt.ItemFlag.ItemIsEditable
        return flags

def open_new_window(new_window: POSDialog):
    open_qdialog = new_window
    open_qdialog.exec()
