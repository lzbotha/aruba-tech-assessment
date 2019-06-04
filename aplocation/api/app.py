#!flask/bin/python
from flask import Flask, jsonify
from flask import request
from flask import abort

app = Flask(__name__)


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    print(task)
    return jsonify({'task': task}), 201

if __name__ == '__main__':
    app.run(debug=True)