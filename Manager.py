"""
This program mediates between the AI instructions and the game itself through stdin and stdout
"""
import sys
import subprocess


class Manager:
    ai = ""
    game_name = ""
    best = 0

    def __init__(self, game, ai, gens=50):
        self.gens = gens
        self.game_name = game

    def openAI(self):
        self.ai = "" #subprocess.Popen(['python', ai], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def openGame(self):
        self.game = subprocess.Popen(['python', self.game_name, "t"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def write(self, input, proc):
        proc.stdin.flush()
        proc.stdin.write((input+"\n").encode("ASCII"))
        proc.stdin.flush()

    def read(self, proc):
        return proc.stdout.readline().decode("ASCII")

    def train(self):
        # self.openAI()
        for x in range(int(self.gens)):
            print("Running generation:", str(x) + ".")
            self.openGame()
            running = True
            while running:
                reading = self.read(self.game)
                if "Score" in reading:
                    # Game ended
                    print("End of gen", str(x) + ".")
                    self.write("OK", self.game)
                    self.best = max(self.best, int(reading[7:]))
                    running = False
                    # send AI that game is done and score if needed
                else:
                    #feed reading to ai and send instruction to game
                    self.write("r", self.game)



if __name__ == "__main__":

    if not len(sys.argv) == 4:
        print("Usage: python Manager.py Game.py AI.py gens")
    else:
        # AI = subprocess.Popen(['python',sys.argv[2]], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        manager = Manager(sys.argv[1], sys.argv[2], sys.argv[3])
        manager.train()


