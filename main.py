from flask import Flask, render_template, jsonify
from datetime import time, datetime

app = Flask(__name__, static_folder="/")
app.config["SECRET_KEY"] = "secret_key"
j = 0
ticker = 1
current_element = 0


class Element:
    def __init__(self, number, type, duration, src):
        self.src = src
        self.duration = duration
        self.number = number
        self.type = type

    def get_duration(self):
        return self.duration

    def get_src(self):
        return self.src

    def get_number(self):
        return self.number

    def get_type(self):
        return self.type


class Ticker:
    pass


def get_elements():
    elements = []
    f = open("cfg/time.cfg")
    i = 0
    for elem in f.readlines():
        if elem.strip():
            conf = elem.split()
            if conf[0] == "image":
                typ = "image"
                path = "\\images\\"
            elif conf[0] == "video":
                typ = "video"
                path = "\\videos\\"
            elif conf[0] == "text":
                typ = "text"
                path = "\\texts\\"
            if not elem[0] == ";":
                if not conf[2] == "default":
                    # hours = int(conf[2].split(":")[0])
                    # minutes = int(conf[2].split(":")[1])
                    # seconds = int(conf[2].split(":")[2])
                    el = Element(i, typ, int(conf[2]), path + conf[1])
                    i += 1
                    elements.append(el)
    return elements


def test():
    global j
    j = (j + 1) % 2
    return j


@app.route("/", methods=["GET"])
def index():
    global current_element
    current_element = 0
    elements = get_elements()
    return render_template("index.html", elements=enumerate(elements))


@app.route("/api/current_element", methods=["GET"])
def get_image():
    global ticker, current_element
    elements = get_elements()
    # for elem in get_elements()[current_element:]:
    #     # if (elem.time.hour == datetime.now().hour
    #     #         and elem.time.minute == datetime.now().minute
    #     #         and elem.time.second == datetime.now().second):
    if elements[current_element].get_duration() == ticker:
        ticker = 1
        current_element += 1
        if current_element >= len(elements):
            return jsonify({"element": "stop",
                            "type": ""})
        return jsonify({"element": str(elements[current_element].get_number()),
                        "type": elements[current_element].get_type()})
    ticker += 1
    return jsonify({"element": "",
                    "type": ""})


if __name__ == "__main__":
    app.run(debug=True)
