
from flask import Flask, render_template, request, jsonify
from process_data import process_data, valid_member

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def get_and_process_data():
    # Get data from client
    data = request.get_json()
    image_data_url = data.get('image_data', '')

    try:
        id = process_data(image_data_url)
        if valid_member(id) == 1:
            return jsonify({'message': 'granted'})
        else:
            return jsonify({'message': 'denied'})
    except:
        return jsonify({'message': 'No QR'})


if __name__ == '__main__':
    app.run(debug=True, port=5500, host='0.0.0.0')
