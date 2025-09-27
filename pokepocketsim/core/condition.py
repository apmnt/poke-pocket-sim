import random


class ConditionBase:
    def rid(self) -> bool:
        raise NotImplementedError("Subclasses should implement this method")

    def serialize(self) -> str:
        return self.__class__.__name__


class Condition:

    class Minus20DamageReceived(ConditionBase):
        def rid(self) -> bool:
            return True

    class Minus20DamageDealed(ConditionBase):
        def rid(self) -> bool:
            return True

    class Plus10DamageDealed(ConditionBase):
        def rid(self) -> bool:
            return True

    class Plus30DamageDealed(ConditionBase):
        def rid(self) -> bool:
            return True

    class Poison(ConditionBase):
        def rid(self) -> bool:
            return False

    class Asleep(ConditionBase):
        def rid(self) -> bool:
            return random.choice([True, False])

    class Paralyzed(ConditionBase):
        def rid(self) -> bool:
            return random.choice([True, False])
