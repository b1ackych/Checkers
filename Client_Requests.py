import requests
import time
import MinMax


def getGameCondition():
    return requests.get(f'http://localhost:8081/game').json()


if __name__ == '__main__':
    # Our team name ;)
    team_name = 'KEKW'

    # Connecting to the server.
    registration = requests.post(f'http://localhost:8081/game', params={'team_name': team_name})
    registration_response = registration.json()

    # Color of our team.
    team_color = registration_response['data']['color']
    # According to color, deciding in which turn our bot makes move.
    team_turn = 1 if team_color == 'RED' else 2
    # Our player's token.
    team_token = registration_response['data']['token']

    # Our game.
    game = MinMax.Game()
    last_move = None
    # Game process.
    game_condition = getGameCondition()['data']
    while not game_condition['is_finished']:
        if game_condition['whose_turn'] == team_color:
            # Enemy's move.

            enemy_move = game_condition['last_move']
            if enemy_move is not None and last_move not in enemy_move['last_moves']:
                for m in enemy_move['last_moves']:
                    game.move(m)
            # Make our move.

            time_to_move = getGameCondition()['data']['available_time']
            #print(time_to_move)
            start = time.time()
            our_move = MinMax.bestMove(game, time_to_move - 2.5)
            #print("finding move took: ", time.time() - start)
            print(our_move)

            # Send our best move to the server.
            make_move = requests.post(f'http://localhost:8081/move', json={'move': our_move},
                                      headers={'Authorization': f'Token {team_token}'})
            last_move = our_move
            game.move(our_move)

        else:
            # Sleep for 0.1 seconds waiting for enemy's turn.
            time.sleep(1)
        game_condition = getGameCondition()['data']

    print(getGameCondition()['data']['winner'])
