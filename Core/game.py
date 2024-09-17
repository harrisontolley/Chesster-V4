import time
import chess

from Core.Search.Search import Search


def main():
    board = chess.Board()
    search = Search(time_limit=5)

    move_count = 0
    total_time = 0
    print(board)

    while not board.is_game_over():
        print("Bot is thinking...")
        start = time.time()

        best_move, evaluation = search.search(board, 7)

        end = time.time()

        if best_move:
            move = (
                chess.Move.from_uci(best_move)
                if isinstance(best_move, str)
                else best_move
            )

            print(f"before board push {move}, {type(move)}")
            board.push(move)
            print(f"after board push {move}")

            move_count += 1
            time_taken = end - start
            total_time += time_taken
            print(f"Move {move_count}: {move.uci()} | Time taken: {time_taken:.2f}s")
            print(f"Cumulative Average: {total_time / move_count:.2f}")
            print(f"Nodes Searched: {search.nodes_searched}, Table Hits: {search.table_hits}")
        else:
            print("No valid move found by bot.")
            break

        print(board)

    # Calculate and display the average time per move
    if move_count > 0:
        average_time = total_time / move_count
        print(f"Average time per move: {average_time:.2f}s")

    if board.is_game_over():
        print("Game Over!")
        print(board)

