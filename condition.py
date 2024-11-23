import random


class Condition:
    class Minus20DamageReceived:
        def rid():
            return True

    class Minus20DamageDealed:
        def rid():
            return True

    class Plus10DamageDealed:
        def rid():
            return True

    class Plus30DamageDealed:
        def rid():
            return True

    class Poison:
        def rid():
            return False

    class Asleep:
        def rid():
            return random.choice([True, False])

    class Paralyzed:
        def rid():
            return random.choice([True, False])
