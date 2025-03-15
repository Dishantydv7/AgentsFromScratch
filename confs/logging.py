import time
from colorama import Fore
from colorama import Style


def fancy_print(message: str) -> None:
    print(Style.BRIGHT + Fore.CYAN + f"\n{'=' * 50}")
    print(Fore.MAGENTA + f"{message}")
    print(Style.BRIGHT + Fore.CYAN + f"{'=' * 50}\n")
    time.sleep(0.5)


def fancy_step_tracker(step: int, total_steps: int) -> None:
    fancy_print(f"STEP {step + 1}/{total_steps}")