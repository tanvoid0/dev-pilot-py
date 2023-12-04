import threading
import tkinter as tk
from functools import partial
from tkinter import ttk
from tkinter.font import Font

from py_helper.service.kubernetes.kubernetes_service import KubernetesService


class KubernetesApp(tk.Tk):
    interrupted = False
    checkboxes = {}
    service = KubernetesService()
    resources = {}
    namespace = "jay"
    watching = False

    def start_watching(self):
        self.watching = True
        print("Starting to watch")
        self.resources = self.service.list_resources(self.namespace, self.resources)

        self.deployment_thread = threading.Thread(target=self.service.watcher_client.watch_deployments,
                                                  args=(self.namespace, self.resources, self.watching))
        self.statefulset_thread = threading.Thread(target=self.service.watcher_client.watch_statefulsets,
                                                   args=(self.namespace, self.resources, self.watching))
        self.deployment_thread.start()
        self.statefulset_thread.start()

    def stop_watching(self):
        print("Stopped to watch")
        self.watching = False
        self.resources = {}

    def my_function(self):
        print("Function executed!")
        if self.interrupted:
            print("Interrupted UI. won't reload")
        else:
            print("Hot Reload")

    def schedule_next_execution(self):
        self.my_function()  # Execute the function
        self.after(5000,
                   self.schedule_next_execution)  # Schedule the function to be executed again after 5000 milliseconds (5 seconds)

    def convert_map_to_tuple(self, resources) -> ([], []):
        resource_list = []
        for key, value in resources.items():
            resource_list.append([
                # value.id,
                value.name,
                value.service_name,
                # value.pod,
                value.stateful_set,
                value.selected
            ])
        headers = [
            # "Id",
            "Name",
            "Service name",
            "StatefulSet",
            "Selection"
        ]
        return headers, resource_list

    def __init__(self):
        super().__init__()

        # Initial data
        self.resources = self.service.list_resources(self.namespace, self.resources)
        self.namespaces, self.current_namespace = self.service.list_namespaces_with_current()
        self.headers, self.table_data = self.convert_map_to_tuple(self.resources)

        root = self
        root.title("Kubernetes Dashboard")

        ## Dropdown
        self.combobox = ttk.Combobox(self, values=self.namespaces)
        self.combobox.set(self.current_namespace)
        self.combobox.bind("<<ComboboxSelected>>", self.on_namespace_change)
        self.combobox.pack()

        ### Dropdown label
        self.namespace_label = tk.Label(self, text=self.current_namespace)
        self.namespace_label.pack()

        # Create a frame for the table
        self.table_frame = tk.Frame(root)
        self.table_frame.pack()

        # Column headers
        self.populate_table([self.headers] + self.table_data)
        # self.populate_table([self.headers] + self.table_data)

        # Create a row for buttons at the bottom of the table
        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        # Buttons
        self.scale_up_button = tk.Button(self.button_frame, text="Scale Up", command=self.batch_scale)
        self.scale_down_button = tk.Button(self.button_frame, text="Scale Down")
        # self.delete_button = tk.Button(self.button_frame, text="Delete")
        # self.save_button = tk.Button(self.button_frame, text="Save")
        self.refresh_button = tk.Button(self.button_frame, text="Refresh")
        #
        self.scale_up_button.pack(side=tk.LEFT)
        self.scale_down_button.pack(side=tk.LEFT)
        # self.delete_button.pack(side=tk.LEFT)
        # self.save_button.pack(side=tk.LEFT)
        self.refresh_button.pack(side=tk.LEFT)

        # # Create an input field and button below the button row
        # self.input_frame = tk.Frame(root)
        # self.input_frame.pack()
        #
        # self.input_label = tk.Label(self.input_frame, text="Input:")
        # self.input_label.pack(side=tk.LEFT)
        #
        # self.input_entry = tk.Entry(self.input_frame)
        # self.input_entry.pack(side=tk.LEFT)
        #
        # self.input_button = tk.Button(self.input_frame, text="Submit")
        # self.input_button.pack(side=tk.LEFT)
        #
        # self.toggle_button = tk.Checkbutton(root, text="Start Watching", command=self.toggle_watching)
        # self.toggle_button.pack()

        # Schedule the next execution
        # self.after(5000, self.schedule_next_execution)
        self.mainloop()

    def on_namespace_change(self, event):
        selected_option = self.combobox.get()
        self.namespace_label.config(text=selected_option)
        self.current_namespace = selected_option
        self.service.config_service.update_namespace(self.current_namespace)
        print(event)

    def toggle_watching(self):
        print("Toggle")
        if self.watching:
            # If currently watching, stop watching
            self.stop_watching()
            # self.toggle_button.config(text="Start Watching")
        else:
            # If not watching, start watching
            self.start_watching()
            # self.toggle_button.config(text="Stop Watching")

    def checkbox_clicked(self, deployment_name):
        print(f"Checkbox in row {deployment_name} clicked")
        self.service.toggle_selection(deployment_name)
        self.resources[deployment_name].selected = not self.resources[deployment_name].selected
        # if row_id in self.checkboxes:
        #     self.checkboxes.pop(row_id)
        # else:
        #     self.checkboxes[row_id] = True
        # if len(self.checkboxes) > 0:
        #     self.interrupted = True
        # else:
        #     self.interrupted = False

    def populate_table(self, data):
        for i, row in enumerate(data):
            for j, item in enumerate(row):
                if j == len(row) - 1 and i != 0:
                    # Create a Checkbutton for the last column
                    checkbox_var = tk.BooleanVar(value=item)
                    checkbox = tk.Checkbutton(self.table_frame, variable=checkbox_var,
                                              command=partial(self.checkbox_clicked, row[0]))
                    checkbox.grid(row=i, column=j, sticky="w")
                else:
                    # For other columns, use labels
                    label_font = Font(family="Arial", size=10,
                                      weight="bold") if i == 0 else None  # Make the first row bold

                    table_label = tk.Label(self.table_frame, text=item, borderwidth=1, relief="solid", anchor="w",
                                           font=label_font)
                    table_label.grid(row=i, column=j, sticky="w")

    def batch_scale(self, up=True):
        print(type(self.resources))
        selected_statefulsets = []
        selected_deployments = []
        for item in self.resources:
            if self.resources[item].selected:
                if self.resources[item].stateful_set:
                    selected_statefulsets.append(item)
                else:
                    selected_deployments.append(item)

                print(self.resources[item].name + " " + str(self.resources[item].selected))

        print("Stateful sets")
        print(selected_statefulsets)

        print("Deployments")
        print(selected_deployments)
