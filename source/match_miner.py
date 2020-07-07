import requests as req
import pandas as pd
import time


def get_match_ids(folder: str):

    # our dates
    dates = [
        ("2019-07-01", "2019-08-01"),
        ("2019-08-02", "2019-09-01"),
        ("2019-09-02", "2019-10-01"),
        ("2019-10-02", "2019-11-01"),
        ("2019-11-02", "2019-12-01"),
        ("2019-12-02", "2020-01-01"),
        ("2020-01-02", "2020-02-01"),
        ("2020-02-02", "2020-03-01"),
        ("2020-03-02", "2020-04-01"),
        ("2020-04-02", "2020-05-01"),
        ("2020-05-02", "2020-06-01"),
        ("2020-06-02", "2020-07-06"), ]

    # data container
    match_ids = []

    # get ids
    for from_date, to_date in dates:
        try:
            url = f"https://api.opendota.com/api/explorer?sql=SELECT%0A%20%20%20%20%20%20%20%20matches.match_id%20%2C%0Aavg(kills)%20%22AVG%20Kills%22%2C%0Acount(distinct%20matches.match_id)%20count%2C%0Asum(case%20when%20(player_matches.player_slot%20%3C%20128)%20%3D%20radiant_win%20then%201%20else%200%20end)%3A%3Afloat%2Fcount(1)%20winrate%2C%0A((sum(case%20when%20(player_matches.player_slot%20%3C%20128)%20%3D%20radiant_win%20then%201%20else%200%20end)%3A%3Afloat%2Fcount(1))%20%0A%2B%201.96%20*%201.96%20%2F%20(2%20*%20count(1))%20%0A-%201.96%20*%20sqrt((((sum(case%20when%20(player_matches.player_slot%20%3C%20128)%20%3D%20radiant_win%20then%201%20else%200%20end)%3A%3Afloat%2Fcount(1))%20*%20(1%20-%20(sum(case%20when%20(player_matches.player_slot%20%3C%20128)%20%3D%20radiant_win%20then%201%20else%200%20end)%3A%3Afloat%2Fcount(1)))%20%2B%201.96%20*%201.96%20%2F%20(4%20*%20count(1)))%20%2F%20count(1))))%0A%2F%20(1%20%2B%201.96%20*%201.96%20%2F%20count(1))%20winrate_wilson%2C%0Asum(kills)%20sum%2C%0Amin(kills)%20min%2C%0Amax(kills)%20max%2C%0Astddev(kills%3A%3Anumeric)%20stddev%0A%20%20%0AFROM%20matches%0AJOIN%20match_patch%20using(match_id)%0AJOIN%20leagues%20using(leagueid)%0AJOIN%20player_matches%20using(match_id)%0AJOIN%20heroes%20on%20heroes.id%20%3D%20player_matches.hero_id%0ALEFT%20JOIN%20notable_players%20ON%20notable_players.account_id%20%3D%20player_matches.account_id%0ALEFT%20JOIN%20teams%20using(team_id)%0AWHERE%20TRUE%0AAND%20kills%20IS%20NOT%20NULL%20%0AAND%20matches.start_time%20%3E%3D%20extract(epoch%20from%20timestamp%20%27{from_date}T22%3A00%3A00.000Z%27)%0AAND%20matches.start_time%20%3C%3D%20extract(epoch%20from%20timestamp%20%27{to_date}T22%3A00%3A00.000Z%27)%0AGROUP%20BY%20matches.match_id%0AHAVING%20count(distinct%20matches.match_id)%20%3E%3D%201%0AORDER%20BY%20%22AVG%20Kills%22%20DESC%2Ccount%20DESC%20NULLS%20LAST"
            res = req.get(url)
            match_ids.extend([x["match_id"] for x in res.json()["rows"]])
        except:
            print(f"There was an error code {res.status_code}")
            break
    data = pd.DataFrame({"match_id": match_ids})
    data = data.drop_duplicates()
    data.to_csv(f"{folder}matches_ids.csv", index=False)
    return "Done."


def get_matches_data(id_list: list, from_position: int, to_position: int, folder: str):
    done = False
    error = ""

    # containers
    match_ids = []
    victor_teams = []
    radiant_teams = []
    dire_teams = []

    # extract each match in the list
    for i, match_id in enumerate(id_list[from_position:to_position]):

        # make request
        res = req.get(f"https://api.opendota.com/api/matches/{match_id}")

        # log request number
        print(f"request n° {i+1}")

        # check for errors
        try:
            if res.status_code == 200:
                # extract useful data
                match_ids.append(res.json()["match_id"])
                victor_teams.append("Radiant" if res.json()[
                                    "radiant_win"] == True else "Dire")
                radiant_teams.append(
                    '-'.join([str(x["hero_id"]) for x in res.json()["players"] if x["isRadiant"] == True]))
                dire_teams.append(
                    '-'.join([str(x["hero_id"]) for x in res.json()["players"] if x["isRadiant"] == False]))

                done = True
            else:
                error = f"{res.status_code}"
                done = False
                break
        except:
            error = "There was an exception"
            done = False
            break

        # wait a second
        time.sleep(1)
    # create data frame
    print("Creating DataFrame..")
    data = pd.DataFrame({
        "match_id": match_ids,
        "victor_team": victor_teams,
        "radiant_team": radiant_teams,
        "dire_team": dire_teams,
    })

    # export csv file
    print("Saving file..")
    data.to_csv(f"{folder}{int(time.time())}.csv", index=False)

    # end
    return "Done" if done == True else f"Error {error}"
