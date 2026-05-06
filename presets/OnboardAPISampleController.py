import sys
import time
from pynput import keyboard
import onboardapipython

dds_domain = 2

class HidJoystick_Service_Callback(onboardapipython.M_HidJoystick_IService):
    pass

hidJoyStick_service_callback = HidJoystick_Service_Callback()
hidJoyStickService = onboardapipython.M_HidJoystick_Service.create(dds_domain, "HidJoystick", hidJoyStick_service_callback)

class Camera_Client_Callback(onboardapipython.M_Camera_IClient):
    def ReportCameraSettings(self, settings):
        #print(settings)
        pass
    def ReportCameraStatus (self, status, isRemoved):
        #print(status)
        pass
    pass

camera_client_callback = Camera_Client_Callback()
cameraClient = onboardapipython.M_Camera_Client.create(2, "Camera", camera_client_callback)

internalStateZoomLevel = 0.0

def clamp(n, min, max):
    if n < min:
        return min
    elif n > max:
        return max
    else:
        return n

# ------------------------------------------------------------------
# Define the “press” callbacks
# ------------------------------------------------------------------
def action_w_press():      hidJoyStickService.send().ReportAxis(1, 1.0, bool(0))
def action_a_press():      hidJoyStickService.send().ReportAxis(0, -1.0, bool(0))
def action_s_press():      hidJoyStickService.send().ReportAxis(1, -1.0, bool(0))
def action_d_press():      hidJoyStickService.send().ReportAxis(0, 1.0, bool(0))
def action_q_press():      hidJoyStickService.send().ReportAxis(2, -1.0, bool(0))
def action_e_press():      hidJoyStickService.send().ReportAxis(2, 1.0, bool(0))
def action_r_press(): 
    global internalStateZoomLevel     
    internalStateZoomLevel += 0.1
    internalStateZoomLevel = clamp(internalStateZoomLevel, 0, 7)
    cameraClient.send().ConfigZoomLevel(internalStateZoomLevel)
def action_f_press():      
    global internalStateZoomLevel
    internalStateZoomLevel -= 0.1
    internalStateZoomLevel = clamp(internalStateZoomLevel, 0, 7)
    cameraClient.send().ConfigZoomLevel(internalStateZoomLevel)

def action_left_press():   hidJoyStickService.send().ReportAxis(4, -1.0, bool(0))
def action_up_press():     hidJoyStickService.send().ReportAxis(5, -1.0, bool(0))
def action_right_press():  hidJoyStickService.send().ReportAxis(4, 1.0, bool(0))
def action_down_press():   hidJoyStickService.send().ReportAxis(5, 1.0, bool(0))

def action_space_press():  hidJoyStickService.send().ReportAxis(3, 1.0, bool(0))
def action_ctrl_left_press(): hidJoyStickService.send().ReportAxis(3, -1.0, bool(0))


# ------------------------------------------------------------------
# Define the “release” callbacks
# ------------------------------------------------------------------
def action_w_release():    hidJoyStickService.send().ReportAxis(1, 0, bool(0))
def action_a_release():    hidJoyStickService.send().ReportAxis(0, 0, bool(0))
def action_s_release():    hidJoyStickService.send().ReportAxis(1, 0, bool(0))
def action_d_release():    hidJoyStickService.send().ReportAxis(0, 0, bool(0))
def action_q_release():    hidJoyStickService.send().ReportAxis(2, 0, bool(0))
def action_e_release():    hidJoyStickService.send().ReportAxis(2, 0, bool(0))
def action_r_release():    pass
def action_f_release():    pass

def action_left_release(): hidJoyStickService.send().ReportAxis(4, 0, bool(0))
def action_up_release():   hidJoyStickService.send().ReportAxis(5, 0, bool(0))
def action_right_release():hidJoyStickService.send().ReportAxis(4, 0, bool(0))
def action_down_release(): hidJoyStickService.send().ReportAxis(5, 0, bool(0))

def action_space_release():  hidJoyStickService.send().ReportAxis(3, 0, bool(0))
def action_ctrl_left_release(): hidJoyStickService.send().ReportAxis(3, -0, bool(0))

# ------------------------------------------------------------------
# Map keys to the press/release callbacks
# ------------------------------------------------------------------
# Printable letters are referenced by their lowercase string.
# Arrow keys are the `pynput.keyboard.Key` enum members.
KEY_TO_PRESS_ACTION = {
    'w': action_w_press,
    'a': action_a_press,
    's': action_s_press,
    'd': action_d_press,
    'q': action_q_press,
    'e': action_e_press,
    'r': action_r_press,
    'f': action_f_press,
    keyboard.Key.left:  action_left_press,
    keyboard.Key.up:    action_up_press,
    keyboard.Key.right: action_right_press,
    keyboard.Key.down:  action_down_press,
    keyboard.Key.space:  action_space_press,
    keyboard.Key.ctrl_l:  action_ctrl_left_press,
}

KEY_TO_RELEASE_ACTION = {
    'w': action_w_release,
    'a': action_a_release,
    's': action_s_release,
    'd': action_d_release,
    'q': action_q_release,
    'e': action_e_release,
    'r': action_r_release,
    'f': action_f_release,
    keyboard.Key.left:  action_left_release,
    keyboard.Key.up:    action_up_release,
    keyboard.Key.right: action_right_release,
    keyboard.Key.down:  action_down_release,
    keyboard.Key.space:  action_space_release,
    keyboard.Key.ctrl_l:  action_ctrl_left_release,
}

# ------------------------------------------------------------------
# Filter out the key‑repeat spam (press events only)
# ------------------------------------------------------------------
REPEAT_THRESHOLD_MS = 30          # ignore repeats fired <30 ms apart
_last_press_time = {}

def _should_filter_press(key):
    """Return True if this press event should be ignored (repeat)."""
    now = time.time() * 1000  # ms
    last = _last_press_time.get(key, 0)
    if now - last < REPEAT_THRESHOLD_MS:
        return True
    _last_press_time[key] = now
    return False

# ------------------------------------------------------------------
# Helper: Resolve a key into a key‑identifier we can use in our maps
# ------------------------------------------------------------------
def _key_identifier(key):
    """
    For printable keys return the lowercase character string.
    For non‑printable keys (arrows, function keys, etc.) return the Key enum.
    """
    try:
        return key.char.lower()
    except AttributeError:
        return key          # e.g. keyboard.Key.left

# ------------------------------------------------------------------
# Listener callbacks
# ------------------------------------------------------------------
def on_press(key):
    # filter repeated press events
    if _should_filter_press(key):
        return  # ignore repeated press events

    # Normal key mapping
    key_id = _key_identifier(key)
    press_action = KEY_TO_PRESS_ACTION.get(key_id)
    if press_action:
        press_action()

    # ESC terminates the listener
    if key == keyboard.Key.esc:
        print("\nESC pressed – terminating listener.")
        return False

def on_release(key):
    # Normal key mapping
    key_id = _key_identifier(key)
    release_action = KEY_TO_RELEASE_ACTION.get(key_id)
    if release_action:
        release_action()
        

# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
def main():
    print(f"🎮 OnboardAPI sample controller on domain {dds_domain} started.")
    print("Available inputs:")
    print("  • W         - Fly forward")
    print("  • A         - Fly left")
    print("  • S         - Fly backward")
    print("  • D         - Fly right")
    print("  • Q         - Turn left")
    print("  • E         - Turn right")
    print("  • Space     - Fly upwards")
    print("  • Left Ctrl - Fly downwards")
    print("  • Left      - Move camera left")
    print("  • Up        - Move camera up")
    print("  • Right     - Move camera right")
    print("  • Down      - Move camera down")
    print("  • ESC       - Exit.")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()  # block until the listener stops

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:  # allow Ctrl‑C to kill the program cleanly
        sys.exit(0)
