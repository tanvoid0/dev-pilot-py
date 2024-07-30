from py_helper.processor.dashboard_processor import DashboardProcessor
from py_helper.processor.os_commander import OSCommander
from py_helper.processor.print_processor import color_text, BRED_TEXT
from py_helper.service.config_service import ConfigService

if __name__ == '__main__':
    print("Operating System: {}".format(color_text(BRED_TEXT, OSCommander.os)))
    ConfigService().first_time_setup()
    DashboardProcessor().run()
