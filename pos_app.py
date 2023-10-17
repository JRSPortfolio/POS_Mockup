# from database.pos_models import Base
# from database.mysql_engine import engine

# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)


from gui.pos_mainwindow import POSMainWindow
from PyQt6.QtWidgets import QApplication
import sys




def main():
    app = QApplication(sys.argv)  
    window = POSMainWindow()
    window.show()
    sys.exit(app.exec())




if __name__ == '__main__':
    main()    
