# Pokemon TCG Pocket Simulator

Under development!

Currently features almost every mechanic except abilities and evolutions. Most of the implementations need improvement code qua
lity and performance wise. Manual work included adding attacks with special effects, abilities, and trainers. Pokemon can be added by scraping the pokemon list and generating necessary code.


Roadmap:

- Add abilities
- Add evolutions
- Add data collection for match analysis
- Add user based inputs to make it user/bot playable

Output snippet:

```
Turn 1, p1's turn, 0 - 0
Possible actions:
         Action(Name: Set Mewtwo EX as active card, Type: ActionType.SET_ACTIVE_CARD)
         Action(Name: Set Mewtwo EX as active card, Type: ActionType.SET_ACTIVE_CARD)
Acting: Set Mewtwo EX as active card
Setting active card from hand to Mewtwo EX
Current active card of p1 is Card(Mewtwo EX with 150 hp, Energies: )
Current active card of p2 is None

Turn 2, p2's turn, 0 - 0
Possible actions:
         Action(Name: Set Mewtwo EX as active card, Type: ActionType.SET_ACTIVE_CARD)
         Action(Name: Set Mewtwo EX as active card, Type: ActionType.SET_ACTIVE_CARD)
Acting: Set Mewtwo EX as active card
Setting active card from hand to Mewtwo EX
Current active card of p2 is Card(Mewtwo EX with 150 hp, Energies: )
Current active card of p1 is Card(Mewtwo EX with 150 hp, Energies: )

Turn 3, p1's turn, 0 - 0
Possible actions:
         Action(Name: Add Mewtwo EX to bench, Type: ActionType.ADD_CARD_TO_BENCH)
         Action(Name: Add water energy to Card(Mewtwo EX with 150 hp, Energies: ), Type: ActionType.ADD_ENERGY)
Acting: Add Mewtwo EX to bench
Acting: Add water energy to Card(Mewtwo EX with 150 hp, Energies: )
Current active card of p1 is Card(Mewtwo EX with 150 hp, Energies: water: 1)
Current active card of p2 is Card(Mewtwo EX with 150 hp, Energies: )
```
