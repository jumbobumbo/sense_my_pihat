
def initialize():
    # see rotater.py for more details
    global t_status
    t_status = False  # active thread status - default as False (none alive)
    global t_name  # thread name, updated by during thread creation
    global rotation_deg  # degrees the screen is rotated at (int) [0, 90, 180, 270]
    rotation_deg = 270