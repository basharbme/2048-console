
def randint(seed = None, a=0, b=4,  N=10**12, integer=True): # stolen from @user2008484 on stackoverflow and modified (https://stackoverflow.com/questions/22950768/random-int-without-importing-random)
    if seed: 
        global _rand_generator 
        if integer: 
            hash_plus = lambda j: int(a + (b-a)*(abs(hash(str(hash(str(seed) + str(j+1))))) % 10**13)/ 10**13)
        else:
            hash_plus = lambda j: a + (b-a)*(abs(hash(str(hash(str(seed) + str(j+1))))) % 10**13)/ 10**13
        _rand_generator =  (hash_plus(j) for j in range(N))
    try:
        return next(_rand_generator)
    except:
        return None

class Board:
    def __init__(self):
        self.field = Field() 

class Field:
    def __init__(self):
        self.field = None

    def __str__(self):
        return "\n".join([str(list(map(lambda x: str(x), p))) for p in self.field])

    def new(self): # on call reset the field and add a random block
        initfield = []
        for i in range(16):
            #initfield.append(Block(i % 4, int(i / 4), 0))
            initfield.append(" ")
#        initfield[5] = Block(1, 1, 4)
#        initfield[6] = Block(2, 1, 2)
#        initfield[9] = Block(1, 2, 2)
        self.field = Field.fold(initfield)
        self.addrandomblock()
    
    def checkgameover(self):
        if len([x for x in self.flat() if type(x) is Block]) == 16:
            for p in self.flat():
                adjacents = self.adjacentcells(p)
                for a in adjacents:
                    if p.value == a.value:
                        return False 
        else:
            return False 
        return True 

    def adjacentcells(self, block):
        r = []

        xbounds = range(0, len(self.field))
        ybounds = range(0, len(self.field))

        diffx = range(-1, 2, 2)
        diffy = range(-1, 2, 2)

        for x in diffx:
            nx = block.x - x

            if nx in xbounds:
                r.append(self.field[block.y][nx])

        for y in diffy:
            ny = block.y - y

            if ny in ybounds:
                r.append(self.field[ny][block.x])

        return r

    def move_upwards(self):
        for i in range(1, len(self.field)):
            blocks = [p for p in self.field[i] if type(p) is Block]
            for p in blocks:
                targetcol = self.getcolumn(p.x)
                occupied = [x for x in targetcol[:p.y][::-1] if type(x) is Block]

                if len(occupied) == 0:
                    self.resetcell(p.x, p.y)
                    p.y = 0
                    self.setcell(p)
                else:
                    nearestoccupant = occupied[0]
                    if p.value == nearestoccupant.value:
                        self.resetcell(p.x, p.y)
                        p.inherit(nearestoccupant)
                        p.increase()
                        self.setcell(p)
                    else:
                        self.resetcell(p.x, p.y)
                        p.y = nearestoccupant.y + 1
                        self.setcell(p)

    def move_downwards(self):
        for i in range(len(self.field) - 2, 0 - 1, -1):
            blocks = [p for p in self.field[i] if type(p) is Block]
            for p in blocks:
                targetcol = self.getcolumn(p.x)
                occupied = [x for x in targetcol[p.y + 1:] if type(x) is Block]

                if len(occupied) == 0:
                    self.resetcell(p.x, p.y)
                    p.y = 3
                    self.setcell(p)
                else:
                    nearestoccupant = occupied[0]
                    if p.value == nearestoccupant.value:
                        self.resetcell(p.x, p.y)
                        p.inherit(nearestoccupant)
                        p.increase()
                        self.setcell(p)
                    else:
                        self.resetcell(p.x, p.y)
                        p.y = nearestoccupant.y - 1
                        self.setcell(p)

    def move_right(self):
        for i in range(len(self.field) - 2, 0 - 1, -1):
            blocks = [p for p in self.getcolumn(i) if type(p) is Block]
            for p in blocks:
                targetrow = self.field[p.y]
                occupied = [x for x in targetrow[p.x + 1:] if type(x) is Block]

                if len(occupied) == 0:
                    self.resetcell(p.x, p.y)
                    p.x = 3
                    self.setcell(p)
                else:
                    nearestoccupant = occupied[0]
                    if p.value == nearestoccupant.value:
                        self.resetcell(p.x, p.y)
                        p.inherit(nearestoccupant)
                        p.increase()
                        self.setcell(p)
                    else:
                        self.resetcell(p.x, p.y)
                        p.x = nearestoccupant.x - 1
                        self.setcell(p)

    def move_left(self):
        for i in range(1, len(self.field)):
            blocks = [p for p in self.getcolumn(i) if type(p) is Block]
            for p in blocks:
                targetrow = self.field[p.y]
                occupied = [x for x in targetrow[:p.x][::-1] if type(x) is Block]

                if len(occupied) == 0:
                    self.resetcell(p.x, p.y)
                    p.x = 0
                    self.setcell(p)
                else:
                    nearestoccupant = occupied[0]
                    if p.value == nearestoccupant.value:
                        self.resetcell(p.x, p.y)
                        p.inherit(nearestoccupant)
                        p.increase()
                        self.setcell(p)
                    else:
                        self.resetcell(p.x, p.y)
                        p.x = nearestoccupant.x + 1
                        self.setcell(p)

    def getcolumn(self, n):
        return [x[n] for x in self.field]

    def addrandomblock(self):
        nx, ny = randint(), randint()
        while type(self.field[ny][nx]) is Block:
            nx, ny = randint(), randint()

        np = Block(nx, ny, 2, True)
        self.setcell(np)

    def resetcell(self, x, y):
        self.field[y][x] = " "
        # function only exists in case some more fancy symbol were to be added into empty cells

    def setcell(self, block):
        self.field[block.y][block.x] = block

    def flat(self): #return a flat version of the matrix (see np.flat)
        r = []
        for i in range(len(self.field)):
            r.extend([i for i in self.field[i]])
        return r
    
    def fold(x):
        r = []
        for i in range(4):
            r.append(x[i * 4:(i + 1) * 4])
        return r

class Block:
    def __init__(self, x, y, value, isnew = False):
        self.x = x
        self.y = y
        self.value = value
        self.isnew = isnew

    def __str__(self):
#        return str(self.value) if self.isnew == False else "\033[92m" + str(self.value) +"\033[0m"
        return str(self.value) if self.isnew == False else "[%s]"%(str(self.value))

    def increase(self):
        self.value *= 2

    def inherit(self, block):
        self.x = block.x
        self.y = block.y

class Game:
    def __init__(self, board):
        self.board = board

    def checkgamestate(self):
        if (len([x for x in self.board.field.flat() if type(x) is Block and x.value == 2048]) >= 1) or self.checkgameover():
            return False
        else:
            return True

    def checkgameover(self):
        return self.board.field.checkgameover()

    def checkgameresult(self):
        if len([x for x in self.board.field.flat() if type(x) is Block and x.value == 2048]) >= 1:
            return True
        elif self.checkgameover():
            return False
        else:
            print("Some weird unexplainable error occured")

    def start(self):
        _running = True
        _round = 1


        while _running:
            print("\033[96m\033[1mRound: %s\033[0m"%(_round))
            print("\033[96mScore: %s\033[0m\n"%(max(list(map(lambda x: x.value, [p for p in self.board.field.flat() if type(p) is Block])))))

            print(str(self.board.field))

            d = input()

            if d.lower() == "w":
                self.board.field.move_upwards()

            if d.lower() == "s":
                self.board.field.move_downwards()

            if d.lower() == "d":
                self.board.field.move_right()
            
            if d.lower() == "a":
                self.board.field.move_left()


            for p in [x for x in self.board.field.flat() if type(x) is Block and x.isnew == True]:
                p.isnew = False

            _running = self.checkgamestate()

            if not len([x for x in self.board.field.flat() if type(x) is Block]) == 16:
                self.board.field.addrandomblock()

            print("\n")
            _round += 1

        gameresult = self.checkgameresult()

        if gameresult == True: # stylize these two messages
            print("YOU WON!")
        else:
            print("YOU LOST!")

def main():
    initrngseed = 85109213745050274563532823495687287
    randint(initrngseed)

    board = Board()
    board.field.new()

    game = Game(board)

    game.start()
    

if __name__ == "__main__":
    main()

# ---- NOTES ----
# for stylization of str(board) see https://en.wikipedia.org/wiki/Box-drawing_character




# ---- TODO ----
# checking if the game is over
# comment everything
