from flask import Flask

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from aplocation.route import app

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
