from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QScrollArea, QTableWidget, \
    QTableWidgetItem, QSizePolicy, QComboBox, QPushButton, QLabel, QSpacerItem, QCheckBox

from py_helper.service.config_service import ConfigService
from py_helper.service.kubernetes.kubernetes_service import KubernetesService


class MainWindow(QWidget):
    kubernetes_service = KubernetesService()
    namespace_list: [str] = []
    selected_namespace: str = None

    def __init__(self):
        super().__init__()

        ## DB Setup
        ConfigService().first_time_setup()

        ## Variables
        self.namespace_list, self.selected_namespace = self.kubernetes_service.list_namespaces_with_current()

        # Set the initial height and width of the app
        self.setGeometry(0, 0, 600, 400)

        # Create a layout for the window
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create a scroll area for the body
        self.body = QScrollArea()
        self.body.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.body.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.palette = self.body.palette()
        self.palette.setColor(QPalette.Window, Qt.red)
        self.body.setPalette(self.palette)

        # Add the topbar and body to the window layout
        self.top_bar_setup()

        self.table = QTableWidget()
        self.table_setup()

        # Show the window
        self.show()

    def top_bar_setup(self):
        # Create a topbar widget
        self.topbar = QWidget()
        self.topbar.setFixedHeight(50)

        self.layout.addWidget(self.topbar)

        self.topbar_layout = QHBoxLayout()
        self.topbar_layout.setAlignment(Qt.AlignHCenter)

        # Left Alignment
        self.batch_scale_up_button = QPushButton("Scale Up")
        self.batch_scale_down_button = QPushButton("Scale down")

        # Right Alignment
        self.dropdown_label = QLabel("Namespace")
        self.dropdown_button = QComboBox()
        self.dropdown_button.addItems(self.namespace_list)
        self.dropdown_button.setCurrentText(self.selected_namespace)

        self.topbar_layout.addWidget(self.batch_scale_up_button)
        self.topbar_layout.addWidget(self.batch_scale_down_button)

        self.topbar_layout.addItem(QSpacerItem(40, 20))

        self.topbar_layout.addWidget(self.dropdown_label)
        self.topbar_layout.addWidget(self.dropdown_button)

        self.topbar.setLayout(self.topbar_layout)

    # Create a table widget for the body
    def table_setup(self):
        # Set the number of rows and columns in the table
        headers = ["Name", "Service Name", "Selection", "Action"]
        self.table.setRowCount(100)
        self.table.setColumnCount(len(headers))

        # Set the headers for the table
        self.table.setHorizontalHeaderLabels(headers)
        self.selection_checkbox = []

        # Add data to the table
        for i in range(100):
            name_item = QTableWidgetItem(f"Item {i}")
            service_name_item = QTableWidgetItem(f"Service name {i}")

            #### Checkbox Layout
            checkbox = QCheckBox(f"Checkbox {i}")
            self.selection_checkbox.append(checkbox)
            self.selection_checkbox[i].setChecked(True)
            print(i)
            checkbox.stateChanged.connect(partial(self.on_toggle_item, i))

            up_button = QPushButton("Up")
            down_button = QPushButton("Down")
            restart_button = QPushButton("Restart")
            button_widget = QWidget()
            button_layout = QVBoxLayout()
            button_layout.addWidget(up_button)
            button_layout.addWidget(down_button)
            button_layout.addWidget(restart_button)
            button_widget.setLayout(button_layout)

            # table.setItem(i, 0, index_item)
            self.table.setItem(i, 0, name_item)
            self.table.setItem(i, 1, service_name_item)
            self.table.setCellWidget(i, 2, self.selection_checkbox[i])
            self.table.setCellWidget(i, 3, button_widget)

        # Set the table widget as the scroll area's widget
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.layout.addWidget(self.table, Qt.AlignCenter)

    def on_toggle_item(self, resource_name, state):
        print(resource_name)
        print(True if state == 2 else False)

    def scale_up(self):
        print("Scale up")

    def scale_down(self):
        print("Scale down")


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()

    app.exec_()
