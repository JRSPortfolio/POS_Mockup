from PyQt6.QtWidgets import QDialog

class AddUserWindow(QDialog):
    def __init__(self):
        super(AddUserWindow, self).__init__()
        
        self.set_window_placements()
    
    def set_window_placements(self):
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle('Adicionar Utilizador')
        
class AddCategoryWindow(QDialog):
    def __init__(self):
        super(AddCategoryWindow, self).__init__()
        
        self.set_window_placements()
    
    def set_window_placements(self):
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle('Adicionar Categoria')

class AddProductWindow(QDialog):
    def __init__(self):
        super(AddProductWindow, self).__init__()
        
        self.set_window_placements()
    
    def set_window_placements(self):
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle('Adicionar Produto')

