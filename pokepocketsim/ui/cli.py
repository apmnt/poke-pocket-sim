"""
Command-line interface for Pokemon Pocket Simulator.
"""

import argparse
import sys
from typing import Optional


def main(argv: Optional[list] = None) -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="poke-sim",
        description="Pokemon TCG Pocket Simulator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Play command
    play_parser = subparsers.add_parser("play", help="Play a game")
    play_parser.add_argument(
        "--mode", choices=["cli", "tui", "bot"], default="cli", help="UI mode (default: cli)"
    )
    play_parser.add_argument("--deck", help="Deck configuration (not yet implemented)")

    # Version command
    version_parser = subparsers.add_parser("version", help="Show version")

    args = parser.parse_args(argv)

    if args.command == "version":
        print("poke-pocket-sim version 0.2.0")
        return 0

    elif args.command == "play":
        print(f"Starting game in {args.mode} mode...")
        print("Note: Use 'python3 demo_tui.py' for now")
        print("Full CLI integration coming soon!")
        return 0

    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
