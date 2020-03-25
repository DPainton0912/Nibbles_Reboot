class Leaderboard(object):
    def __init__(self, playername):
        self.playername = playername

    def ReadFile(self):
        readfile = open("leaderboard.txt","r")
        fileread = readfile.read()
        readfile.close()
        leaderboard = fileread.split(",")
        return(leaderboard)

    def ShowLeaderboard(self, leaderboard):
        for i in range(0, 19, 2):
            name = str(leaderboard[i])
            score = str(leaderboard[i+1])
            print(name + "\t" + score)

    def NewHighscore(self, s, leaderboard):
        score = (len(s.body)-1)
        for i in range(1,len(leaderboard),2):
            if score >= int(leaderboard[i]):
                print("New highscore!")
                leaderboard.insert((i-1), self.playername)
                leaderboard.insert((i), str(score))

                break
        return(leaderboard)

    def WriteFile(self, leaderboard):
        highscores = []
        for i in range(len(leaderboard)):
            if i == (len(leaderboard) - 1):
                highscores += leaderboard[i]
            else:
                highscores += (leaderboard[i] + ",")
        filewrite = "".join(highscores)
        writefile = open("leaderboard.txt", "w")
        writefile.write(filewrite)
        writefile.close()