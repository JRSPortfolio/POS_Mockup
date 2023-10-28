# from database.mysql_engine import engine
# from database.pos_models import Base
# from database.populate_db import populate_categorias, populate_tipo_iva, populate_produtos

# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)

# populate_categorias()
# populate_tipo_iva()
# populate_produtos()


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


# from database.pos_crud_and_validations import get_product_by_name_and_category
# from database.mysql_engine import session

# get_product_by_name_and_category(session, 'Sumo Manga', 'Bebidas')