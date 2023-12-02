from cookies import cookies
import pathlib
import requests

# loads the data for a given day and year
# as a list of the lines. tries to cache the data as well.
# uses the cookie data from the hidden util/cookies file
def load_data(day: int, year: int, cache_location: str ="/data", testing=False, test_file="tmp.txt") -> str:
    if testing:
        with open(test_file, 'r') as f:
            data = f.read()
        return data.strip()

    # try to load file
    target_name = f"{cache_location}/{year}_{day:02d}.txt"

    data = None
    try:
        with open(f"{pathlib.Path(__file__).parent.resolve()}/{target_name}", 'r') as f:
            data = f.read()
    except FileNotFoundError as _:
        print("Downloading!")
        data = requests.get(
            f"https://adventofcode.com/{year}/day/{day}/input",
            cookies=cookies
        ).text

        # save it to file
        with open(f"{pathlib.Path(__file__).parent.resolve()}/{target_name}", 'w') as f:
            f.write(data)

    return data.strip()


