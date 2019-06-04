from flask import Flask

from aplocation.api.route import app

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    # app.run()
