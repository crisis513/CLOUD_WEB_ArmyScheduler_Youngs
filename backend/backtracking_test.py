from copy import deepcopy

class Backtrack:

    def __init__(self, n):
        self.result = list()
        self.best = list()
        self.cur = list()
        self.n = n
        self.bestscore = 0
        self.stop = False

    def backtrack(self, left):
        if self.stop:
            return
        if left == 0:
            r = deepcopy(self.cur)
            self.result.append(r)
            score = self.score()
            if score > self.bestscore:
                self.bestscore = score
                self.best = r
            # self.stop = True
            return
        for i in range(1, self.n+1):
            if i not in self.cur:
                self.cur.append(i)
                self.backtrack(left-1)
                self.cur.pop()
    
    def score(self):
        return max(self.cur) + min(self.cur)
        
def main():
    b = Backtrack(7)
    b.backtrack(5)
    print(b.bestscore)
    print(b.best)

if __name__ == '__main__':
    main()