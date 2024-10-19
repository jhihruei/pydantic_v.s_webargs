from flask import Flask

from blueprints import pydantic_blueprint, webargs_blueprint

app = Flask(__name__)

# 註冊 Blueprints
app.register_blueprint(webargs_blueprint)
app.register_blueprint(pydantic_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
