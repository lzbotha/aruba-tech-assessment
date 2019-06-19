from flask import Flask

from aplocation.route import app

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    # app.run()
