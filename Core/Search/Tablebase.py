import requests

def query_tablebase(fen):  # Query the tablebase when 7 pieces or less
    url = "http://tablebase.lichess.ovh/standard"  # table base api
    params = {"fen": fen.replace(" ", "_")}
    return requests.get(url, params=params)

def get_best_move(fen):
    response = query_tablebase(fen)
    if response.ok:
        data = response.json()
        if "moves" in data and data["moves"]:
            best_move_uci = data["moves"][0]["uci"]
            return best_move_uci
        else:
            print("No moves available or not a tablebase position.")
            return None
    else:
        print("Error:", response.status_code)
        return None