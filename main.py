from flask import Flask, render_template, jsonify
from datetime import time, datetime

app = Flask(__name__, static_folder="/")
app.config["SECRET_KEY"] = "secret_key"
j = 0


class Image:
    def __init__(self, image, time, number):
        self.image = image
        self.time = time
        self.number = number

    def get_time(self):
        return self.time

    def get_image(self):
        return self.image

    def get_number(self):
        return self.number


def get_images():

    default = None
    images = []
    f = open("cfg/time.cfg")
    i = 0
    for elem in f.readlines():
        if elem.strip():
            if not elem.strip()[0] == ";":
                args = elem.split()
                if not args[1] == "default":
                    hours = int(args[1].split(":")[0])
                    minutes = int(args[1].split(":")[1])
                    seconds = int(args[1].split(":")[2])
                    img = Image("/images/" + args[0], time(hours, minutes, seconds), i)
                    i += 1
                    images.append(img)
                else:
                    default = "/images/" + args[0]
                    i += 1
    return images, default


def test():
    global j
    j = (j + 1) % 2
    return j


@app.route("/", methods=["GET"])
def index():
    images, default = get_images()
    return render_template("index.html", images=enumerate(images), default=default)


@app.route("/api/current_image", methods=["GET"])
def get_image():
    for elem in get_images()[0]:
        if (elem.time.hour == datetime.now().hour
                and elem.time.minute == datetime.now().minute
                and elem.time.second == datetime.now().second):
            return jsonify({"image": str(elem.get_number())})
    return jsonify({"image": ""})


if __name__ == "__main__":
    app.run(debug=True)
