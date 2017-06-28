side_effect = ''
modifier = 'affected'

def reset_side_effect():
    global side_effect
    side_effect = ''

def times_side_effects_happen():
    global side_effect
    return len(side_effect) / len(modifier)

def side_effected():
    global side_effect
    side_effect = side_effect + modifier

class Tester:
    def __init__(self):
        self.a = 1
        self.b = 2

    def mutate(self):
        self.a = 2 * self.a
        self.b = self.b * self.b
        side_effected()

