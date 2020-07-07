import source.match_miner as mm
import time
import pandas as pd

id_list = pd.read_csv("matchesdata/matches_ids.csv")
id_list = id_list["match_id"].values.tolist()


path = "matchesdata/"

from_position = int(input("From: "))
to_postion = int(input("To: "))

mm.get_matches_data(id_list, from_position, to_postion, path)
