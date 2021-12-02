# -*- coding:utf-8 -*-

from bson.objectid import ObjectId


def generate_uuid():
    return str(ObjectId())
