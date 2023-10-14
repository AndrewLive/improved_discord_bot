from CardGame import GameState

if __name__ == '__main__':
    game = GameState(player = 'player')
    print(game)

    while True:
        game.start_game()
        print('Game Start!')
        print(game)

        while game.game_stage == 'player_turn':
            action = input('stand or hit\n')
            if action == 'stand':
                game.stand()
            elif action == 'hit':
                game.hit()
            else:
                print('invalid action')
            
            print(game)
        
        if game.game_stage == 'dealer_turn':
            game.play_dealer()
            print('Dealer turn:')
            print(game)

        game.evaluate_game()
        print('Final evaluation:')
        print(game)

        if (input('play again? y/n\n') == 'n'):
            break

    