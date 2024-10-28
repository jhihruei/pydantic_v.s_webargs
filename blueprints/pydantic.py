import json
from enum import Enum
from typing import Optional

from flask import Blueprint, jsonify, request
from pydantic import BaseModel, Field, ValidationError

pydantic_blueprint = Blueprint("pydantic_blueprint", __name__, url_prefix="/p")


class UserModel(BaseModel):
    name: str
    age: int


# Example: `curl "http://127.0.0.1:5000/p/query-string?name=Ray&age=18"`
@pydantic_blueprint.route("/query-string", methods=["GET"])
def hello_world():
    try:
        # 驗證 JSON 資料
        user = UserModel(**request.args)
        return jsonify({"message": f"Hello {user.name}, you are {user.age} years old!"})
    except ValidationError as e:
        return jsonify(e.errors()), 400


class IntModel(BaseModel):
    default_int: int = 999
    min_zero: int = Field(gt=0)
    max_ten: int = Field(le=10, alias="maxTen")
    # NOTE: 有 default value 的情況等同 allow missing
    missing: Optional[int] = -1
    allow_none: int | None


# Example: `curl -d '{"min_zero":1, "maxTen":10, "allow_none":null}' -H "Content-Type: application/json" -X POST "http://127.0.0.1:5000/p/int-args"`
@pydantic_blueprint.route("/int-args", methods=["POST"])
def int_args_validate():
    try:
        # 驗證 JSON 資料
        args = IntModel(**request.json)
        return jsonify(
            {
                "default_int": args.default_int,
                "min_zero": args.min_zero,
                "max_ten": args.max_ten,
                "missing": args.missing,
                "allow_none": args.allow_none,
            }
        )

    except ValidationError as e:
        return jsonify(e.errors()), 400


class UserRole(str, Enum):
    teacher = "teacher"
    student = "student"


class StringModel(BaseModel):
    allow_none: str | None
    default_list: str = "[]"
    max_length: str = Field(max_length=16)

    user_role: UserRole = Field(alias="userRole")
    # NOTE: 用 Enum 的做法比較漂亮，如果要堅持 str type 的話也可以用 Regex:
    # user_role: str = Field(pattern=r"^(teacher|student)$", alias="userRole")


# Example: `curl -d '{"allow_none":null, "userRole": "student", "max_length": "string len is 16"}' -H "Content-Type: application/json" -X POST "http://127.0.0.1:5000/p/string-args"`
@pydantic_blueprint.route("/string-args", methods=["POST"])
def string_args_validate():
    try:
        # 驗證 JSON 資料
        args = StringModel(**request.json)
        return jsonify(
            {
                "allow_none": args.allow_none,
                "default_list": json.loads(args.default_list),
                "user_role": args.user_role,
                "max_length": args.max_length,
            }
        )

    except ValidationError as e:
        return jsonify(e.errors()), 400
