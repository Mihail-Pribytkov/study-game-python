from utils import randbool, randcell, randcell2

# 0 - поле
# 1 - дерево
# 2 - река
# 3 - госпиталь 
# 4 - апгрейд-шоп
# 5 - огонь

CELL_TYPES = "⬜🌲🌊🚑🚀🔥"
TREE_BONUS = 100
UPGRADE_COST = 100
FIRE_DURATION = 3  # Сколько ходов горит огонь

class Map:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.cells = [[0 for i in range(w)] for j in range(h)]
        self.fire_timers = {}  # Словарь для отслеживания времени жизни огня
        self.generate_forest(3, 10)
        self.generate_river(10)
        self.generate_river(10)
        self.generate_upgrade_shop()

    def check_bounds(self, x, y):
        if (x < 0 or y < 0 or y >= self.h or x >= self.w):
            return False
        return True
    def print_map(self, helico):
        print("🏁" * (self.w + 2))
        for ri in range(self.h):
            print("🏁", end="")
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if (helico.x == ri and helico.y == ci):
                    print("🚁", end="")
                elif (cell >= 0 and cell < len(CELL_TYPES)):
                    print(CELL_TYPES[cell], end="")
            print("🏁")
        print("🏁" * (self.w + 2))

    def generate_river(self, l):
        rc = randcell(self.w, self.h)
        rx, ry = rc[0], rc[1]
        if (self.check_bounds(rx, ry)):
            self.cells[ry][rx] = 2
            while l > 0:
                rc2 = randcell2(rx, ry)
                rx2, ry2 = rc2[0], rc2[1]
                if (self.check_bounds(rx2, ry2)):
                    self.cells[ry2][rx2] = 2
                    rx, ry = rx2, ry2
                    l -= 1
    def generate_forest(self, r, mxr):
        for ri in range(self.h):
            for ci in range(self.w):
                if randbool(r, mxr):
                    self.cells[ri][ci] = 1
    def generate_tree(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        if (self.check_bounds(cx, cy) and self.cells[cy][cx] == 0):
            self.cells[cy][cx] = 1

    def generate_upgrade_shop(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        if (self.check_bounds(cx, cy) and self.cells[cy][cx] == 0):
            self.cells[cy][cx] = 4
            print(f"Апгрейд-шоп создан в позиции ({cx}, {cy})")

    def add_fire(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        if self.check_bounds(cx, cy) and self.cells[cy][cx] == 1:
            self.cells[cy][cx] = 5
            self.fire_timers[(cx, cy)] = FIRE_DURATION
    
    def update_fires(self):
        fires_to_remove = []
        for (x, y), timer in self.fire_timers.items():
            if timer <= 1:  # Огонь гаснет
                fires_to_remove.append((x, y))
                self.cells[y][x] = 0
            else:
                self.fire_timers[(x, y)] = timer - 1
        
        for pos in fires_to_remove:
            del self.fire_timers[pos]
        
        for i in range(10):
            self.add_fire()

    def process_helicopter(self, helico):
        if not self.check_bounds(helico.x, helico.y):
            return
            
        c = self.cells[helico.y][helico.x] 
        print(f"Вертолет в позиции ({helico.x}, {helico.y}), клетка: {c}")
        if (c == 2):
            helico.tank = helico.mxtank
        if (c == 5 and helico.tank > 0):
            helico.tank -= 1
            helico.score += TREE_BONUS
            self.cells[helico.y][helico.x] = 1  
            if (helico.x, helico.y) in self.fire_timers:
                del self.fire_timers[(helico.x, helico.y)]
        if (c == 4):
            print(f"Вертолет на апгрейд-шопе! Очки: {helico.score}, нужно: {UPGRADE_COST}")
            if helico.score >= UPGRADE_COST:
                helico.mxtank += 1
                helico.score -= UPGRADE_COST
                self.cells[helico.y][helico.x] = 1
                print(f"Апгрейд! Новый размер бака: {helico.mxtank}")
            else:
                print(f"Недостаточно очков для апгрейда! Нужно: {UPGRADE_COST}, есть: {helico.score}") 