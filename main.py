from game import Game  # import the Game class from game.py


if __name__ == "__main__":  # run if main.py is being run directly
    main_game = Game("PygOOM", 10, 10, 5)  # create the game object
    main_game.run()  # run the game
