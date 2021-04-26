from flask import Flask, render_template, jsonify
from datetime import time, datetime

app = Flask(__name__, static_folder="/")
app.config["SECRET_KEY"] = "secret_key"
j = 0


class Element:
    def __init__(self, number, type, time, src):
        self.src = src
        self.time = time
        self.number = number
        self.type = type

    def get_time(self):
        return self.time

    def get_src(self):
        return self.src

    def get_number(self):
        return self.number

    def get_type(self):
        return self.type


def get_elements():
    default = None
    elements = []
    f = open("cfg/time.cfg")
    i = 0
    for elem in f.readlines():
        if elem.strip():
            conf = elem.split()
            if conf[0] == "image":
                typ = "image"
                path = "/images/"
            elif conf[0] == "video":
                typ = "video"
                path = "/videos/"
            if not elem[0] == ";":
                if not conf[2] == "default":
                    hours = int(conf[2].split(":")[0])
                    minutes = int(conf[2].split(":")[1])
                    seconds = int(conf[2].split(":")[2])
                    el = Element(i, typ, time(hours, minutes, seconds), path + conf[1])
                    i += 1
                    elements.append(el)
                else:
                    default = path + conf[1]
                    i += 1
    return elements, default


def test():
    global j
    j = (j + 1) % 2
    return j


@app.route("/", methods=["GET"])
def index():
    elements, default = get_elements()
    return render_template("index.html", elements=enumerate(elements), default=default)


@app.route("/api/current_element", methods=["GET"])
def get_image():
    for elem in get_elements()[0]:
        if (elem.time.hour == datetime.now().hour
                and elem.time.minute == datetime.now().minute
                and elem.time.second == datetime.now().second):
            return jsonify({"element": str(elem.get_number()),
                            "type": elem.get_type()})
    return jsonify({"element": "",
                    "type": ""})


if __name__ == "__main__":
    app.run(debug=True)
