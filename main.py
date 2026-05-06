from pathlib import Path
import time

from boyer_moore import boyer_moore_search
from kmp import kmp_search
from rabin_karp import rabin_karp_search

BASE_DIR = Path(__file__).resolve().parent
ENCODING = "cp1251"

ALGORITHMS = {
    "Boyer-Moore": boyer_moore_search,
    "Knuth-Morris-Pratt": kmp_search,
    "Rabin-Karp": rabin_karp_search,
}


def load_text(filename: str) -> str:
    return (BASE_DIR / filename).read_text(encoding=ENCODING)


def time_once(func, text: str, pattern: str) -> float:
    t0 = time.perf_counter()
    func(text, pattern)
    return (time.perf_counter() - t0) * 1000


def main() -> None:
    texts = {
        "article_1": load_text("article_1.txt"),
        "article_2": load_text("article_2.txt"),
    }

    scenarios = {
        "article_1": {
            "існуючий": "Лінійний або послідовний пошук – найпростіший алгоритм пошук",
            "неіснуючий": "Метою роботи є виявлення найбільш популярних алгоритмів у бібліотеках мов програмування",
        },
        "article_2": {
            "існуючий": f"Метою роботи є виявлення найбільш популярних алгоритмів у бібліотеках мов програмування",
            "неіснуючий": "Лінійний або послідовний пошук – найпростіший алгоритм пошук",
        },
    }

    rows = []
    for article, pattern_map in scenarios.items():
        body = texts[article]
        for label, pattern in pattern_map.items():
            timings = {name: time_once(fn, body, pattern) for name, fn in ALGORITHMS.items()}
            rows.append((article, label, timings))

    headers = ["стаття", "сценарій", "Boyer-Moore", "Knuth-Morris-Pratt", "Rabin-Karp"]

    print("| " + " | ".join(headers) + " |")
    print("| " + " | ".join("---" for _ in headers) + " |")

    name_to_col = headers[2:]
    for article, label, timings in rows:
        cells = [article, label] + [f"{timings[n]:.4f}" for n in name_to_col]
        print("| " + " | ".join(cells) + " |")


if __name__ == "__main__":
    main()
