#!/usr/bin/env python
import sys

from sampleapp import app, init_for

application = init_for('dev')

try:
    port = int(sys.argv[1])
except (IndexError, ValueError):
    port = 8080

app.run(port=port, debug=True)
