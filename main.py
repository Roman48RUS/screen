from flask import Flask, render_template, redirect, request, make_response, session, url_for, \
    send_from_directory

app = Flask(__name__, static_folder="/")
app.config["SECRET_KEY"] = "secret_key"


class Image:
    def __init__(self, image, time):
        self.image = image
        self.time = time

    def get_time(self):
        return self.time

    def get_image(self):
        return self.image


@app.route("/", methods=["GET", "POST"])
def index():
    default = None
    images = []
    f = open("cfg/time.cfg")
    for elem in f.readlines():
        if not elem.strip()[0] == ";":
            args = elem.split()
            if not args[1] == "default":
                img = Image("/images/" + args[0], args[1])
                images.append(img)
            else:
                default = args[0]
    return render_template("index.html", images=images, default=default)


if __name__ == "__main__":
    app.run(debug=True)
