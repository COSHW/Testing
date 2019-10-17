from flask import *


class Site:
    def __init__(self):
        self.app = Flask(__name__)

        @self.app.route("/")
        def main():
            return render_template("index.html")

        @self.app.route("/download")
        def download():
            return send_file("9.png", attachment_filename='10.png', as_attachment=True)

        self.app.run()


if __name__ == "__main__":
    Start = Site()


