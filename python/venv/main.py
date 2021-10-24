import json

import Match
import jsonpickle
import nfl_data_py as nfl
import stattypes
from decouple import config
from espn_api.football import League
from flask import Flask
from flask_cors import CORS


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)


def get_long_rushes_henry(yards):
    columns = ['qtr', "rusher_player_name", "rushing_yards"]
    years = range(2016, 2022)
    name = "D.Henry"

    data_df = nfl.import_pbp_data(years, columns)
    henry_df = data_df.loc[data_df['rusher_player_name'] == name]
    henry_long_runs_df = henry_df.loc[henry_df['rushing_yards'] >= yards]
    long_runs_by_qtr = henry_long_runs_df.groupby(['qtr']).count()

    print(henry_long_runs_df.sort_values(by=['qtr', 'season', 'rushing_yards']))
    print(long_runs_by_qtr)


# Check vars here https://www.nflfastr.com/articles/beginners_guide.html

app = Flask("__main__")
CORS(app)


@app.route("/", methods=['GET'])
def get_kicker_scores():
    year = 2021
    week = 5
    league = League(league_id=config("league_id"), year=year, espn_s2=config("espn_s2"), swid=config("swid"))

    columns = stattypes.meta + stattypes.tackles + stattypes.kicks + stattypes.score

    data_df = nfl.import_pbp_data([year], columns)
    week_stats_df = data_df.loc[data_df['week'] == week]

    espn_week_info = league.box_scores(week)

    fantasy_matches = [Match.Match(match, week_stats_df) for match in espn_week_info]

    #matches = json.dumps([ob.__dict__ for ob in fantasy_matches], cls=ComplexEncoder)

    response = jsonpickle.encode({
        "matches": fantasy_matches,
        "week": week
    }, unpicklable=False)

    return response


#if __name__ == '__main__':
#     app.run()

get_long_rushes_henry(40)