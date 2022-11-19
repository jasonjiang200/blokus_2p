class Piece():
    
    def __init__(self, symbol='', rep=[[' ' for _ in range(5)] for _ in range(5)], dirs=[]):
        self.orientation = 0
        self.symbol = symbol
        self.rep = rep
        self.dirs = dirs

    def display(self):
        print('Selected Piece: {}'.format(self.symbol))
        print(' _________')
        for row in self.rep:
            print('|', end='')
            for i in range(4):
                print('{} '.format(row[i]), end='')
            print('{}|'.format(row[-1]))  
        print(' ‾‾‾‾‾‾‾‾‾')       
 
    def rotateOnce(self):
        self.rep = list(zip(*self.rep[::-1]))
        for i in range(len(self.dirs)):
            self.dirs[i] = [self.dirs[i][1], -self.dirs[i][0]]

    def rotate(self, dir):
        if dir == 'cw':
            self.rotateOnce()
        elif dir == '180':
            for _ in range(2):
                self.rotateOnce()
        elif dir == 'ccw':
            for _ in range(3):
                self.rotateOnce()

    def reflect(self, dir):
        if dir == 'v':
            self.rep = self.rep[::-1]
            for i in range(len(self.dirs)):
                self.dirs[i][0] = -self.dirs[i][0]
        elif dir == 'h':
            for i in range(5):
                self.rep[i] = self.rep[i][::-1]
            for i in range(len(self.dirs)):
                self.dirs[i][1] = -self.dirs[i][1]
    
    def __repr__(self):
        return self.symbol

    def __eq__(self, other):
        return self.symbol == other

        


