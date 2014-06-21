#! /usr/bin/env python
from app import app
import os

app.run(debug = True)
# app.run(host = "0.0.0.0", debug= True, port=int(os.environ.get('PORT', 5000)))
