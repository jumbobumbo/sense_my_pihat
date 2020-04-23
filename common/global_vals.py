
def initialize():
    # see rotater.py for more details
    global t_status
    t_status = False  # active thread status - default as False (none alive)
    global t_name  # thread name, updated by during thread creation