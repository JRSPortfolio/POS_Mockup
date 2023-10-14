from database.pos_models import Base
from database.mysql_engine import engine


Base.metadata.create_all(engine)
