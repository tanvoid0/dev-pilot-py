import os

from py_helper.processor.file_processor import FileProcessor

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from py_helper.processor.print_processor import RED_TEXT, GREEN_TEXT, YELLOW_TEXT, color_text

db_file = os.path.join(FileProcessor.current_path(), "db.sqlite")
db_engine = create_engine("sqlite:///{}".format(db_file), echo=False)


def get_session():
    return sessionmaker(bind=db_engine)()


class DBProcessor:

    def init(self, base_model):
        session = get_session()
        config_data = FileProcessor.read_json(
            os.path.join(FileProcessor.current_path(), "config.json")
        )
        print(
            f"Database Reset mode: {color_text(RED_TEXT, 'On') if config_data['db']['reset'] else color_text(GREEN_TEXT, 'Off')}")
        if config_data['db']['reset']:
            try:
                FileProcessor.remove(db_file)
            except:
                print("Database File doesn't exist")

        if not self.db_exists():
            print(f"Database {color_text(RED_TEXT, 'does not exist...')}")
            FileProcessor.save(db_file)

            try:
                base_model.metadata.create_all(db_engine)
                print(color_text(YELLOW_TEXT, "Creating ") + "database")
                print("Database " + color_text(GREEN_TEXT, "created\n"))

                print(color_text(GREEN_TEXT, "Setting up") + " runtime vars")

                session.commit()

                # countdown_timer("Booting up Dev Pilot", config_data['vars']['startup-time'])
                print("System Booted...")
            except Exception as ex:
                print("Database Connection Failed {}".format(ex))
            return True
        return False

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

    def db_exists(self):
        return FileProcessor.file_exists(db_file)
