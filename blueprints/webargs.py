from flask import Blueprint, jsonify
from marshmallow import Schema
from webargs import fields
from webargs.flaskparser import use_args

webargs_blueprint = Blueprint("webargs_blueprint", __name__, url_prefix="/w")

query_args = {"name": fields.Str(required=True), "age": fields.Int(required=True)}


# Example: `curl "http://127.0.0.1:5000/w/query-string?name=Ray&age=18"`
@webargs_blueprint.route("/query-string", methods=["GET"])
@use_args(query_args, location="query")  # 驗證 query 參數
def hello_world(args):
    return jsonify(
        {"message": f"Hello {args['name']}, you are {args['age']} years old!"}
    )


class UserSchema(Schema):
    name = fields.Str(required=True)
    age = fields.Int(required=True)


# Example: `curl "http://127.0.0.1:5000/w/schema/query-string?name=Ray&age=18"`
@webargs_blueprint.route("/schema/query-string", methods=["GET"])
@use_args(UserSchema, location="query")  # 驗證 query 參數
def schema_hello_world(args):
    return jsonify(
        {"message": f"Hello {args['name']}, you are {args['age']} years old!"}
    )
