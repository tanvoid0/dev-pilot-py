from py_helper.dashboard_processor import DashboardProcessor
from py_helper.models.base_model import BaseModel
from py_helper.models.runtime_var_model import RuntimeVarModel
from py_helper.processor.db_processor import DBProcessor
from py_helper.processor.file_processor import FileProcessor
from py_helper.processor.print_processor import color_text, BRED_TEXT

if __name__ == '__main__':
    print("Operating System: {}".format(color_text(BRED_TEXT, FileProcessor.get_platform())))
    db = DBProcessor()
    RuntimeVarModel.first_setup()
    dashboard = DashboardProcessor()
    dashboard.run()

