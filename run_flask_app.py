from subprocess import check_output
from urllib.parse import unquote
from re import findall
from flask import Flask, escape, request
from sense_hat import SenseHat
from common.return_pattern_list import PatternList

# basic flask application
app = Flask(__name__)  # flask object
sense = SenseHat()  # sense hat object


@app.route("/command")
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
    app.run(host=host_ip, port=8082)
