from flask import Flask, render_template, jsonify

app = Flask(__name__, static_folder="/")
app.config["SECRET_KEY"] = "secret_key"


i = 0


class Image:
    def __init__(self, image, time):
        self.image = image
        self.time = time

    def get_time(self):
        return self.time

    def get_image(self):
        return self.image


def test():
    global i
    i = (i + 1) % 2
    return i


@app.route("/", methods=["GET"])
def index():
    default = None
    images = []
    f = open("cfg/time.cfg")
    for elem in f.readlines():
        if elem.strip():
            if not elem.strip()[0] == ";":
                args = elem.split()
                if not args[1] == "default":
                    img = Image("/images/" + args[0], args[1])
                    images.append(img)
                else:
                    default = args[0]
    return render_template("index.html", images=enumerate(images), default=default)


@app.route("/api/current_image", methods=["GET"])
def get_image():
    return jsonify({"image": str(test())})


if __name__ == "__main__":
    app.run(debug=True)
