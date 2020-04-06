from subprocess import check_output
from urllib.parse import unquote
from re import findall
from flask import Flask, request, render_template
from sense_hat import SenseHat
from common.return_pattern_list import PatternList, GeneratePatternFromList
from common.translate_data import ProcessMultiDict

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


@app.route("/ui-command/", methods=['POST'])
def ui_command(red=None, green=None, blue=None, qtype=None):
    """
    ui page
    """
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


@app.route("/post-command/", methods=['POST'])
def post_command(base=None, red=None, green=None, blue=None) -> str:
    """
    Dict of post key, values.
    Creates a list of nested RGB lists and sends it to sense hat
    If successful, sent list is returned as a str (blame flask)
    :return: str
    """
    sense.set_pixels(PatternList(request.get_json(), False).create_pattern_list())
    return str(sense.get_pixels())


@app.route("/")
def test_flask() -> str:
    """
    simply for test
    :return: str
    """
    return "/command is where you really want to be"


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
    app.run(host=host_ip, port=8082, debug=True)
