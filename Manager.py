"""
This program mediates between the AI instructions and the game itself through stdin and stdout
"""
import sys
import subprocess


# class Manager:



if __name__ == "__main__":

    if not len(sys.argv) == 4:
        print("Usage: python Manager.py Game.py AI.py gens")
    else:
        # AI = subprocess.Popen(['python',sys.argv[2]], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        gens =  sys.argv[3]

        for n in range(1):
            game = subprocess.Popen(['python', sys.argv[1]], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            for n in range(35):
                reading = game.stdout.readline().decode("ASCII")
                print(reading)
                game.stdin.flush()
                game.stdin.write("l\n".encode("ASCII"))
                game.stdin.flush()


