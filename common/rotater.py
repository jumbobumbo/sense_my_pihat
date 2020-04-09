from sense_hat import SenseHat
from threading import Thread
from time import sleep
from common import global_vals

class Rotate:
    def __init__(self, sense: object, rotate_vals: list = [], re_draw: bool = True):
        """
        :param sense: object (sense hat connection object)
        :param rotate_vals: list - degrees to rotate: [0, 90, 180, 270]
        :param re_draw: bool  - re_draw the currently displayed image?
        """
        self.sense = sense
        self.rotate_vals = rotate_vals
        self.re_draw = re_draw

    def _thread_runner(self, target_func: object) -> object:
        """
        this is called to start a thread
        :param target_function: value from func_runner dict (funcs)
        we will keep the passed function alive until global_vals.t_status is False
        """
        def _keep_alive():
            """
            Keeps the process running
            """
            while global_vals.t_status:  # if True, we keep rotating the display image
                if type(target_func) == list:
                    target_func[0](target_func[1])
                else:
                    target_func()

        th = Thread(target=_keep_alive, args=())
        th.daemon = True
        # below global variable controls the life and death of the thread in _keep_alive()
        # it is only initlised if run_flask_app is main
        global_vals.t_status = True  # set active thread status to True
        return th.start()  # start the thread

    def _simple_rotation(self) -> str:
        """
        flips the currently displayed image - conforming to values in 'rotate_vals'
        :param background: do you want this task to run in the background
        """
        for val in self.rotate_vals:
            self.sense.set_rotation(val, self.re_draw)
            if len(self.rotate_vals) > 1:
                sleep(0.5)
        return f"rotated (degrees): {self.rotate_vals}"

    def _flipper(self, vertical: bool = True):
        """
        Vertical if True else Horizontal
        :param vertical: bool
        :return: the flip
        """
        return self.sense.flip_v() if vertical else self.sense.flip_h()
        
    def _smooth_rotation(self):
        return "not implemented"
    
    def func_runner(self, run_func: str, back_ground: bool = False) -> object:
        """
        Provide this function a key to run desired function (some additional params) and
        if you want this task to run in the background
        :param run_func: str
        :param back_ground: bool
        :return:
        """
        funcs = {
            "simple": self._simple_rotation,
            "flip_v": self._flipper,
            "flip_h": [self._flipper, False],
            "smooth": self._smooth_rotation
        }
        
        # fetch function to run from above dict
        called_func = funcs[run_func]
        # check if its a function with an addition param
        if back_ground:
            return self._thread_runner(called_func)
        else:
            return called_func[0](called_func[1]) if type(called_func) == list else called_func()
