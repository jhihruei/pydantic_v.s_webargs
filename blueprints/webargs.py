import json
from datetime import datetime

from flask import Blueprint, jsonify
from marshmallow import Schema
from webargs import fields, validate
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


# NOTE:
# 1. 不太確定 missing 和 load_default 具體的差異
int_args = {
    "default_int": fields.Int(load_default=999),
    "min_zero": fields.Int(required=True, validate=validate.Range(min=0)),
    "max_ten": fields.Int(
        data_key="maxTen", required=True, validate=validate.Range(max=10)
    ),
    "missing": fields.Int(missing=-1),
    "allow_none": fields.Int(allow_none=True),
}


# Example: `curl -d '{"min_zero":1, "maxTen":10, "allow_none":null}' -H "Content-Type: application/json" -X POST "http://127.0.0.1:5000/w/int-args"`
@webargs_blueprint.route("/int-args", methods=["POST"])
@use_args(int_args)
def int_args_validate(args):
    return jsonify(
        {
            "default_int": args["default_int"],
            "min_zero": args["min_zero"],
            "max_ten": args["max_ten"],
            "missing": args["missing"],
            "allow_none": args["allow_none"],
        }
    )


string_args = {
    "allow_none": fields.Str(required=True, allow_none=True),
    "default_list": fields.Str(required=False, load_default="[]"),
    "user_role": fields.Str(
        data_key="userRole", validate=validate.OneOf(["teacher", "student"])
    ),
    "max_length": fields.Str(required=True, validate=validate.Length(max=16)),
}


# Example: `curl -d '{"allow_none":null, "userRole": "student", "max_length": "string len is 16"}' -H "Content-Type: application/json" -X POST "http://127.0.0.1:5000/w/string-args"`
@webargs_blueprint.route("/string-args", methods=["POST"])
@use_args(string_args)
def string_args_validate(args):
    return jsonify(
        {
            "allow_none": args["allow_none"],
            "default_list": json.loads(args["default_list"]),
            "user_role": args["user_role"],
            "max_length": args["max_length"],
        }
    )


bool_args = {
    "default_bool": fields.Bool(load_default=False),
    "allow_none": fields.Bool(allow_none=True, data_key="allowNone"),
}


# Example: `curl -d '{"allowNone": null}' -H "Content-Type: application/json" -X POST "http://127.0.0.1:5000/w/bool-args"`
@webargs_blueprint.route("/bool-args", methods=["POST"])
@use_args(bool_args)
def bool_args_validate(args):
    return jsonify(
        {
            "default_bool": args["default_bool"],
            "allow_none": args["allow_none"],
        }
    )


datetime_args = {
    "default_min": fields.Bool(load_default=datetime.min),
    "allow_none": fields.DateTime(required=True, allow_none=True),
    "ymd": fields.DateTime("%Y/%m/%d"),
    "default_format": fields.DateTime(required=True),  # ISO 8601
}


# Example: `curl -d '{"allow_none": null, "ymd": "2024/04/04", "default_format":"2024-04-04 00:00:00"}' -H "Content-Type: application/json" -X POST "http://127.0.0.1:5000/w/datetime-args"`
@webargs_blueprint.route("/datetime-args", methods=["POST"])
@use_args(datetime_args)
def datetime_args_validate(args):
    return jsonify(
        {
            "allow_none": args["allow_none"],
            "default_min": args["default_min"],
            "default_format": args["default_format"],
            "ymd": args["ymd"],
        }
    )
