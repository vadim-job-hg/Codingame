class Area:
    LETTERS_PLUS = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    LETTERS_MINUS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "[::-1]
    letters = {}
    positio = {}
    builded = {}
    magic_phrase = ""
    path = ""
    current_position = 15

    def __init__(self):
        self.magic_phrase = input()

    def closest_plus(self, char):
        return self.LETTERS_PLUS.find(char)

    def closest_minus(self, char):
        return self.LETTERS_MINUS.find(char)

    def get_all_leters(self):
        last_position = 15
        for char in self.magic_phrase:
            letters = self.letters.get(char, None)
            if letters is None:
                self.letters[char] = last_position
                self.positio[last_position] = char
                self.builded[char] = False
                last_position += 1

    def build_path(self):
        for char in self.magic_phrase:
            step = (-1, 1)[self.current_position < self.letters[char]]
            while self.current_position != self.letters[char]:
                if step > 0:
                    self.path += ">"
                    self.current_position += 1
                else:
                    self.path += "<"
                    self.current_position -= 1
            if (not (self.builded[char])):
                self.builded[char] = True
                plus = self.closest_plus(char)
                minus = self.closest_minus(char)
                sight, count = (["-", minus], ["+", plus])[plus < minus]
                self.path += (sight * count)
            self.path += "."
        print(self.path)


act = Area()
act.get_all_leters()
act.build_path()