# Pokemon TCG Pocket Simulator

A Python library for Pokemon TCG Pocket battles.

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/apmnt/poke-pocket-sim.git
cd poke-pocket-sim

# Install dependencies
pip install -e .
```

### Run demo games

```bash
# Play against a bot
python examples/demo_single_player.py

# Or make bots play against eachother
python examples/demo_single_player.py --bot
```

## Roadmap

- [x] Core game mechanics (attacks, items, supporters, abilities)
- [x] Single turn simulation and evaluation
- [x] Human and bot players
- [ ] Improved text-based UI
- [ ] More Pokemon cards and abilities
- [ ] PyPI package distribution
- [ ] Web-based interface

## Contributing

Contributions are welcome! The project is under (on and off) active development.

Any ideas/bugs? [Create an issue](https://github.com/apmnt/poke-pocket-sim/issues)!