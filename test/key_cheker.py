from pynput import keyboard, mouse


# Keyboard event handler
def on_key_press(key):
    try:
        print(f"Key {key.char} pressed")
    except AttributeError:
        print(f"Special Key {key} pressed")


def on_key_release(key):
    print(f"Key {key} released")
    if key == keyboard.Key.esc:  # Stop listener with 'Esc' key
        return False


# Mouse event handler
def on_click(x, y, button, pressed):
    action = "pressed" if pressed else "released"
    print(f"Mouse {button} {action} at ({x}, {y})")


def on_scroll(x, y, dx, dy):
    print(f"Mouse scrolled at ({x}, {y}) with delta ({dx}, {dy})")


# Setting up listeners
with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as kb_listener, \
        mouse.Listener(on_click=on_click, on_scroll=on_scroll) as ms_listener:
    print("Listening for keyboard and mouse events... Press 'Esc' to stop.")
    kb_listener.join()  # Blocks until 'Esc' is pressed
    ms_listener.join()
