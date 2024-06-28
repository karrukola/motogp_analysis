import re
from datetime import timedelta

import matplotlib.pyplot as plt
from matplotlib import ticker
from pypdf import PdfReader
from rich import print

RESULTS_FILE = "analysisbylap_france_2024.pdf"
_NR_LAPS = 27

RIDER_DICT_24 = {
    "1": "Francesco Bagnaia",
    "5": "Johan Zarco",
    "6": "Stefan Bradl",
    "10": "Luca Marini",
    "12": "Maverick Vinales",
    "20": "Fabio Quartararo",
    "21": "Franco Morbidelli",
    "23": "Enea Bastianini",
    "25": "Raul Fernandez",
    "26": "Daniel Pedrosa",
    "30": "Takaaki Nakagami",
    "31": "Pedro Acosta",
    "32": "Lorenzo Savadori",
    "33": "Brad Binder",
    "36": "Johan Mir",
    "37": "Augusto Fernandez",
    "41": "Aleix Espargaro",
    "42": "Alex Rins",
    "43": "Jack Miller",
    "49": "Fabio Digianantonio",
    "72": "Marco Bezzecchi",
    "73": "Alex Marquez",
    "88": "Miguel Oliveira",
    "89": "Jorge Martin",
    "93": "Marc Marquez",
}

RIDER_DICT_20 = {
    "4": "Andrea Dovizioso",
    "5": "Johan Zarco",
    "9": "Danilo Petrucci",
    "12": "Maverick Vinales",
    "20": "Fabio Quartararo",
    "21": "Franco Morbidelli",
    "27": "Iker Lecuona",
    "30": "Takaaki Nakagami",
    "33": "Brad Binder",
    "36": "Johan Mir",
    "38": "Bradley Smith",
    "41": "Aleix Espargaro",
    "42": "Alex Rins",
    "43": "Jack Miller",
    "44": "Pol Espargaro",
    "46": "Valentino Rossi",
    "53": "Tito Rabat",
    "63": "Francesco Bagnaia",
    "73": "Alex Marquez",
    "88": "Miguel Oliveira",
    "93": "Marc Marquez",
}


laps_data_type = dict[str, list[timedelta | None]]


def pretty_format_lap_time(x: float, pos: float) -> str:
    mins = x // 60
    secs = x % 60
    return f"{mins:.0f}'{secs:.3f}"


def parse() -> laps_data_type:
    laps_data: laps_data_type = {}
    for rider in RIDER_DICT_24:
        laps_data[rider] = []

    reader = PdfReader(RESULTS_FILE)
    lap_nr = 0
    lap_info_regex = re.compile(r"(\d'\d{2}\.\d{3})\s?(\d{1,2})\s(\d+.\d{3})?")
    gp_name = reader.pages[0].extract_text().splitlines()[0]

    for page in reader.pages:
        page_content = page.extract_text()
        laps_info: list[str] = re.findall(lap_info_regex, page_content)
        for lap_info in laps_info:
            # lab info: ("2'03.958", '31', '')

            delta = lap_info[2]
            if delta == "":
                lap_nr += 1

            _lap_time = lap_info[0]
            mins, secs = _lap_time.split("'")
            # lap time is the number of seconds
            lap_time = 60 * int(mins) + float(secs)

            _rider_nr = lap_info[1]
            rider = f"{_rider_nr} {RIDER_DICT_24[_rider_nr]}"
            laps_data[_rider_nr].append(lap_time)

    return laps_data, gp_name


def _plot_info(
    laps_info: laps_data_type,
    gp_name: str,
    skip_first_lap: bool = False,
) -> None:
    start_idx = 1 if skip_first_lap else 0
    riders = ["89", "93", "1", "10"]
    laps = range(1, _NR_LAPS + 1)

    _, ax = plt.subplots()
    ax.yaxis.set_major_formatter(pretty_format_lap_time)
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))

    for rider_nr in riders:
        plt.plot(
            laps[start_idx : len(laps_info[rider_nr])],
            laps_info[rider_nr][start_idx:],
            ".:",
            label=f"[{rider_nr}] {RIDER_DICT_24[rider_nr]}",
        )

    plt.grid(visible=True, axis="y", which="minor")
    plt.title(label=gp_name)
    plt.legend()

    plt.show()


if __name__ == "__main__":
    laps_info, gp_name = parse()
    _plot_info(laps_info, gp_name=gp_name, skip_first_lap=True)
