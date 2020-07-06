import time
import pandas as pd
import requests as req


def get_matches_sample(max_requests: int, folder: str, mmr=3850) -> pd.DataFrame:
    """
    Does a a number of requests to the api denoted by the max_requests argument.
    Returns a .csv file containing all the data found.
    NOTE: Does not group by unique findings.
    NOTE: Number of requests is limited by 50 000 per month
    """
    # data container
    matches_data = []
    count = 0
    while count < max_requests:
        # make request
        res = req.get(
            f"https://api.opendota.com/api/publicMatches?mmr_descending={mmr}")
        # check for errors in response
        if res.status_code == 200:
            # extend our data object with response obtained
            matches_data.extend(res.json())
        else:
            # break the loop and end the function
            print f"There was an error with status_code: {res.status_code}"
            break
        count += 1
        # waits a second before continuing to limit the number of requests per minute to 60
        print(f"request n° {count}")
        time.sleep(1)
    # create DataFrame Object
    data = pd.DataFrame(matches_data)
    # correct format in heroes list
    data = data.replace(r"\,", "-", regex=True)
    # return our object!
    print("Saving file..")
    return data.to_csv(f"{folder}{int(time.time())}.csv", index=False)
