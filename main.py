from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
CORS(app)

# ─── Database config ───────────────────────────────────────────────
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'kenangan.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ─── Model ─────────────────────────────────────────────────────────
class Kenangan(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    tanggal   = db.Column(db.String(20), nullable=False)
    pesan     = db.Column(db.Text,  nullable=False)
    fotoURL   = db.Column(db.Text)          # boleh kosong
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "tanggal": self.tanggal,
            "pesan": self.pesan,
            "fotoURL": self.fotoURL,
            "createdAt": self.createdAt.isoformat()
        }

# ─── Inisialisasi DB (sekali saja) ────────────────────────────────
with app.app_context():
    db.create_all()

# ─── Routes API ────────────────────────────────────────────────────
@app.route("/kenangan", methods=["GET"])
def get_kenangan():
    # urutkan terbaru dulu
    data = Kenangan.query.order_by(Kenangan.createdAt.desc()).all()
    return jsonify([k.to_dict() for k in data])

@app.route("/kenangan", methods=["POST"])
def add_kenangan():
    data = request.get_json()
    if not data or not all(k in data for k in ("tanggal", "pesan")):
        return jsonify({"error": "Data incomplete"}), 400

    k = Kenangan(
        tanggal  = data["tanggal"],
        pesan    = data["pesan"],
        fotoURL  = data.get("fotoURL", "")
    )
    db.session.add(k)
    db.session.commit()
    return jsonify({"message": "Kenangan berhasil disimpan"}), 201

# (opsional) kalau mau serve HTML langsung dari Flask
@app.route("/")
def index():
    return render_template("index.html")     # pastikan index.html ada di folder templates/

if __name__ == "__main__":
    app.run(debug=True)
