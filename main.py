import source.match_miner as mm
import time
import pandas as pd

id_list = pd.read_csv("matchesdata/matches_ids.csv")
id_list = id_list["match_id"].values.tolist()


# adjust to start where you want.
from_position = 0
until_position = 5000

while from_position < until_position:
    try:
        mm.get_matches_data(
            id_list[from_position:until_position], "matchesdata/")
        from_position += 1
    except:
        print("trying again...")
        time.sleep(5)
