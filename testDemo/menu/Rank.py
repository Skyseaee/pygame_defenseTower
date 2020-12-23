class rank:
    scores = []
    def getScores(self, filename):
        try:
            fp = open(filename, "r")
            for line in fp.readlines():
                rank.scores.append(int(line))
            fp.close()
            if(len(rank.scores) == 0):
                rank.scores = [0, 0, 0]
        except IOError:
            rank.scores = [0, 0, 0]

    def update(self, newscore, filename):
        for score in self.scores:
            if newscore >= score:
                self.scores.insert(self.scores.index(score), newscore)
                self.scores.pop()
                fp = open(filename, "w")
                for scr in self.scores:
                    fp.write(str(scr))
                    fp.write("\n")
                break

    def getRank(self, newscore):
        for score in self.scores:
            if score == newscore:
                return self.scores.index(score)+1
        return -1




