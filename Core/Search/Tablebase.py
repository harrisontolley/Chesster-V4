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
            category = data.get('category', 'unknown')
            # Determine evaluation based on category
            if category == 'win':
                evaluation = 100000  # High positive value
            elif category == 'loss':
                evaluation = -100000  # High negative value
            else:
                evaluation = 0  # Draw
            return best_move_uci, evaluation
        else:
            print("No moves available or not a tablebase position.")
            return None, 0
    else:
        print(f"Error querying tablebase: {response.status_code}")
        return None, 0