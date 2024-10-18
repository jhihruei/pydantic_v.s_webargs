from flask import Flask, jsonify, request
from pydantic import BaseModel, ValidationError
from webargs import fields
from webargs.flaskparser import use_args

app = Flask(__name__)

# 定義 webargs 的參數驗證
query_args = {"name": fields.Str(required=True), "age": fields.Int(required=True)}


# 定義 pydantic 的資料模型
class UserModel(BaseModel):
    name: str
    age: int


@app.route("/hello", methods=["GET"])
@use_args(query_args, location="query")
def hello(args):
    try:
        user = UserModel(**args)  # 使用 Pydantic 驗證資料
        return jsonify({"message": f"Hello {user.name}, you are {user.age} years old!"})
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400


if __name__ == "__main__":
    app.run(debug=True)
