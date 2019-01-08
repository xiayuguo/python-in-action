from flask import Flask, current_app
from lml.loader import scan_plugins


app = Flask(__name__)


def init_plugins_instance():
    scan_plugins("irain_web_plugin", "irain_web_plugin")
    return dict(task=task())


@app.route('/test_plugin')
def test_plugin():
    plugins = current_app.config.get("plugins")
    if plugins and plugins.get("task", None):
        plugins["taks"].done()


if __name__ == "__main__":
    app.config.update(plugins=init_plugins_instance())
    app.run(host="0.0.0.0", port=5000, debug=True)
