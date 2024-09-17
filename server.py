# server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import chess
from Core.Search.Search import Search

app = Flask(__name__)
CORS(app)

@app.route("/best-move", methods=["POST"])
def best_move():
    data = request.get_json()
    fen = data.get("fen")
    depth = data.get("depth", 3)  # Default to depth 3 if not provided

    if not fen:
        return jsonify({"error": f"Invalid FEN ({fen})"}), 400

    try:
        depth = int(depth)
    except ValueError:
        return jsonify({"error": f"Invalid depth value ({depth})"}), 400

    board = chess.Board(fen)
    search = Search()

    try:
        best_move, evaluation = search.search(board, max_depth=depth)
        print(best_move, evaluation)
        print(best_move.uci())
        return jsonify({"best_move": best_move.uci()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
