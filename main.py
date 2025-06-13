from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Data kenangan disimpan di memori (sementara)
kenangan_list = []

# Endpoint untuk dapatkan semua kenangan
@app.route('/kenangan', methods=['GET'])
def get_kenangan():
    return jsonify(kenangan_list)

# Endpoint untuk tambah kenangan baru
@app.route('/kenangan', methods=['POST'])
def add_kenangan():
    data = request.json
    if not data or 'tanggal' not in data or 'pesan' not in data or 'fotoURL' not in data:
        return jsonify({'error': 'Data incomplete'}), 400

    kenangan_list.append(data)
    return jsonify({'message': 'Kenangan berhasil ditambahkan'}), 201

if __name__ == '__main__':
    app.run(debug=True)
