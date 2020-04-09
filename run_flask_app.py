from subprocess import check_output
from urllib.parse import unquote
from re import findall
from flask import Flask, request, render_template
from sense_hat import SenseHat
from common.return_pattern_list import PatternList, GeneratePatternFromList
from common.translate_data import ProcessMultiDict
from common.rotater import Rotate
from common import global_vals


# basic flask application
app = Flask(__name__, static_url_path="", template_folder='web_pages')  # flask object
sense = SenseHat()  # sense hat object


@app.route("/get-command/", methods=['GET'])
def send_command() -> str:
    """
    set: patterns
    a: preloaded json file (in repo, or just patterns dir)
    jumble.json

    b: directly from input - nested lists [R, G, B] - 64 elements
    [[255, 255, 255]] * 64

    get: pattern values
    RGB values as nested lists:
    [[255, 255, 255]] * 64
    :return: str
    """
    if len(request.args) != 1:
        return f"number of commands must equal 1: number received: {len(request.args)}"

    for cmd, value in request.args.items():
        if cmd == "set":
            img = PatternList(value).create_pattern_list() if "json" in value else list_decoder(value)
            return str(sense.set_pixels(img))

        elif cmd == "get":
            return str(sense.get_pixels())

        else:
            return f"invalid args: {request.args}"


@app.route("/ui-command/", methods=['POST', 'GET'])
def ui_command(red=None, green=None, blue=None, qtype=None):
    """
    ui page
    """
    if request.method == "POST":
        form_copy = request.form.copy()  # we make a copy so its mutable

        # qtype is used to define what pattern quartering we want (square or stripe) not for the colour values
        # since we also support the entire screen being one colour (and therefore qtype not being in the form data)
        # we either fetch qtype and set it to an appropriate varaible or set the var as 0 if it doesn't exist
        if form_copy.get("qtype") is not None:
            pattern_type = int(form_copy.get("qtype"))
            form_copy.pop("qtype")

        else:
            pattern_type = 0

        # process the user inputted data so it can be used for list generation 
        processed_data = ProcessMultiDict(form_copy).post_data_to_nested_lists()
        # send img data to hat - GeneratePatternFromList creates the required list of nested list for qtype 0 or 1
        sense.set_pixels(GeneratePatternFromList(processed_data, pattern_type).pattern_gen())

    # return html page
    return render_template("config.html", red=red, green=green, blue=blue, qtype=qtype)


@app.route("/post-set-img/", methods=['POST'])
def post_set_img() -> str:
    """
    Expects args to be in json format, example:
      requests.post("http://IP/post-set-img/", json=args)
    Creates a list of nested RGB lists and sends it to sense hat
    If successful, sent list is returned as a str (blame flask)
    :return: str
    """
    sense.set_pixels(PatternList(request.get_json(), False).create_pattern_list())
    return str(sense.get_pixels())


@app.route("/post_rotation/", methods=['POST'])
def post_rotation() -> str:
    """
    Sets rotation of image

    Expects cmd to be in json format, example:
      requests.post("http://IP/post-command/", json=cmd)
    Example json: {"cmd": "simple", "background": True, "rotate_vals": [0, 90], "re_draw": True}
    Minimum required keys: "cmd"
    Optional: "rotate_vals", "re_draw", "background"
    To kill the rotation, send the following json: {"cmd": kill"}
    """
    post_data = request.get_json()

    # check we have our required key
    if post_data.get("cmd") == None:
        raise ValueError(f"{key} is a required key")

    # the below three ifs allow only "cmd" to be the required key in the post data
    if not post_data.get("re_draw"):
        post_data["re_draw"] = True  # Redrawing the image is default to True

    r_vals = post_data.get("rotate_vals") if post_data.get("rotate_vals") else []  

    bg = post_data.get("background") if post_data.get("background") else False

    # if cmd is not kill, we start the rotation
    if post_data.get("cmd") != "kill":
        return str(Rotate(sense, r_vals, post_data.get("re_draw")).func_runner(post_data.get("cmd"), bg)) 
    else:
        global_vals.t_status = False  # terminate active thread
        # return last rotation value
        return f"Thread terminated, last rotation value: {sense._rotation}"


@app.route("/")
def test_flask() -> str:
    """
    simply for test
    :return: str
    """
    return "<h1>Pages:</h1><p>/ui-command/</p><p>/get-command/</p><p>/post_rotation/</p>" \
            "<p>/post-set-img/</p>"


def list_decoder(list_to_decode: str) -> list:
    """
    parses the list supplied via the URL and makes it into a readable format for sense.set_pixels()
    :param list_to_decode: str
    :return: list
    """
    decoded_list = []
    sub_list = []

    for index, value in enumerate(unquote(list_to_decode).split(",")):
        sub_list.append(int(findall(r"\d+", value)[0]))

        if (index + 1) % 3 == 0:
            decoded_list.append(sub_list)
            sub_list = []

    return decoded_list


# get ip address of device
host_ip = str(check_output(['hostname', '-I'])).strip("b'").split(" ")[0]


if __name__ == "__main__":
    global_vals.initialize()  # start global values function
    app.run(host=host_ip, port=8082, debug=True)
