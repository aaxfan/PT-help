# ！/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (c) 2017-2020 Rhilip <rhilipruan@gmail.com>

import json

from pymysql import escape_string
from flask import Blueprint, request, jsonify, redirect

from app import mysql
from .gen import Gen

getinfo_blueprint = Blueprint('infogen', __name__, url_prefix="/movieinfo")


@getinfo_blueprint.route("/gen", methods=["GET", "POST"])
def gen():
    if request.method == "POST":
        url = request.form["url"]
    elif request.method == "GET":
        url = request.args.get("url")
    else:
        url = ""

    if url:
        _gen = Gen(url=url)

        row, data = mysql.exec(
            "SELECT * FROM `api`.`gen_info` WHERE `site`='{}' AND `sid`='{}'".format(_gen.site, _gen.sid),
            r_dict=True, ret_row=True
        )

        if int(row) == 0:
            data = _gen.gen()
            if data["success"]:  # 正确获取的情况下缓存请求结果
                mysql.exec(
                    "INSERT INTO `api`.`gen_info` (`site`, `sid`, `data`)"
                    " VALUES ('{}', '{}', '{}')".format(_gen.site, _gen.sid, escape_string(json.dumps(data)))
                )
        else:
            data_str = data.get("data")
            data = json.loads(data_str)

        return jsonify(data)
    else:
        return redirect("https://git.io/vFvmP", code=301)
