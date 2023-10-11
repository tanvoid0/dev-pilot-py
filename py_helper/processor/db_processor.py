import os

from py_helper.processor.file_processor import FileProcessor

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from py_helper.processor.print_processor import RED_TEXT, GREEN_TEXT, YELLOW_TEXT, color_text

db_engine = create_engine("sqlite:///{}".format(os.path.join(FileProcessor.current_path(), "db.sqlite")), echo=False)


def get_db_engine():
    return db_engine


def get_session():
    return sessionmaker(bind=db_engine)()


class DBProcessor:
    def insert(self, model):
        session = get_session()
        session.add(model)
        session.commit()
        return model.id

    def get(self, model):
        session = get_session()
        return session.query(model).all()

    def find_by_id(self, model, id):
        session = get_session()
        return session.query(model).filter_by(id=id).first()

    # TODO: requires additional work
    def update(self, model, update_data):
        session = get_session()
        session.commit()
