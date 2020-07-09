# Dota 2 Win Predictor


Mikki Seidenschnur
Edgar Pena
Regina Hunter

Ironhack, Berlin 06/07/2020

# Project Description
Creating a game win predictor based on the specific character wins, to predict the outcome of a given game.

# Dataset


# Organization
Using Trello we designated tasks based on each team members strenght. Trello gave a clear view as to what needed to be done. 

# Problems
Getting the data and a sufficient count of games to make a more accurate predition. 
1. Coundn't get the most more than 100 most recent games due to the API issues.
2. Storage
Filtering the data for it to be analyzed. Then actually counting out the win/loss for each hero vs another hero. 


# Solutions
1. Using this link(3) to get the bigger sample of matches
2. Use Dropbox


# Tactics
1. Data mining 
2. Filtering (MMR)
3. Counts
4. Combined win rate
5. Model testing
# Team Tasks
Mikki - Created Trello, Filtering
Edgar - Data Mining
Regina - Counts


# Links:
1.
2.
3. https://www.opendota.com/explorer?sql=SELECT%0A%20%20%20%20%20%20%20%20%0Amatches.match_id%2C%0Amatches.start_time%2C%0A((player_matches.player_slot%20%3C%20128)%20%3D%20matches.radiant_win)%20win%2C%0Aplayer_matches.hero_id%2C%0Aplayer_matches.account_id%2C%0Aleagues.name%20leaguename%0AFROM%20matches%0AJOIN%20match_patch%20using(match_id)%0AJOIN%20leagues%20using(leagueid)%0AJOIN%20player_matches%20using(match_id)%0AJOIN%20heroes%20on%20heroes.id%20%3D%20player_matches.hero_id%0ALEFT%20JOIN%20notable_players%20ON%20notable_players.account_id%20%3D%20player_matches.account_id%0ALEFT%20JOIN%20teams%20using(team_id)%0AWHERE%20TRUE%0AAND%20matches.start_time%20%3E%3D%20extract(epoch%20from%20timestamp%20%272020-07-03T22%3A00%3A00.000Z%27)%0AORDER%20BY%20matches.match_id%20NULLS%20LAST%0ALIMIT%2020000&format=