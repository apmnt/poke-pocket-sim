import random


class Condition:
    class Minus20DamageReceived:
        def rid(self):
            return True

    class Minus20DamageDealed:
        def rid(self):
            return True

    class Plus10DamageDealed:
        def rid(self):
            return True

    class Plus30DamageDealed:
        def rid(self):
            return True

    class Poison:
        def rid(self):
            return False

    class Asleep:
        def rid(self):
            return random.choice([True, False])

    class Paralyzed:
        def rid(self):
            return random.choice([True, False])
