import io
import csv
import json
import jsonschema
import random
import string
from app import app
from flask import abort, flash, redirect, session, url_for
from jsonschema import validate
from datetime import date


def write_json(data):
    writer_file = io.StringIO()
    json.dump(data, writer_file, indent=4, sort_keys=False)
    outfile = io.BytesIO()
    outfile.write(writer_file.getvalue().encode("utf-8"))
    outfile.seek(0)
    writer_file.close()
    return outfile

def read_json(json_data):
    data = json.load(json_data)
    return data


def read_data_file(filepath):
    with open(filepath, "r") as f:
        line = f.read().splitlines()
    return line