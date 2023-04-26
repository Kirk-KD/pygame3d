"""Main entry point of the game."""

# import the main Game object forom game.py
from game import Game


def main() -> None:
    """Main entry point function."""

    # initialize the game
    doom = Game("DOOOOOOM")
    # run the game
    doom.run()


# prevents running if this file is accidentally imported
if __name__ == "__main__":
    main()
