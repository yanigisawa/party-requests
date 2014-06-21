from app import app
from flask import render_template, request, flash, jsonify, url_for, redirect

@app.route('/')
def index():
    return render_template("index.html", url = "/")
