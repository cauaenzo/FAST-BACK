import pyfiglet
from colorama import init

# Inicializa colorama (importante no Windows)
init(autoreset=True)

RESET = "\033[0m"


def _neon(text: str) -> str:
    colors = [
        "\033[38;2;0;200;255m",   # azul neon
        "\033[38;2;80;150;255m",  # azul médio
        "\033[38;2;140;100;255m", # azul-roxo
        "\033[38;2;180;60;255m",  # roxo neon
        "\033[38;2;220;40;255m",  # roxo intenso
    ]

    lines = text.splitlines()
    result = []

    for i, line in enumerate(lines):
        color = colors[i % len(colors)]
        result.append(f"{color}{line}{RESET}")

    return "\n".join(result)


def print_banner() -> None:
    # Fonte menor e mais compacta
    ascii_art = pyfiglet.figlet_format(
        "FAST-BACK",
        font="small",
        width=80
    )

    print()
    print(_neon(ascii_art))

    line = "=" * 30

    print(f"\033[38;2;180;60;255m  {line}{RESET}")
    print(
        f"\033[38;2;0;200;255m  >> Queue System API  "
        f"\033[38;2;180;60;255mv1.0.0{RESET}"
    )
    print(f"\033[38;2;180;60;255m  {line}{RESET}")
    print()


# Executa direto (opcional)
if __name__ == "__main__":
    print_banner()