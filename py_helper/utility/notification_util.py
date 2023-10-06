from plyer import notification


class Notification:
    @staticmethod
    def send(title="", message="", app_icon=None, timeout=10):
        notification.notify(title, message, app_icon, timeout)
