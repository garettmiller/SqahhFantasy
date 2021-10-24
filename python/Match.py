import json
import KickerScore
import stattypes


class Match:

	def __init__(self, match, week_stats_df):
		home_kicker = self.get_kicker(match.home_lineup)
		away_kicker = self.get_kicker(match.away_lineup)

		home_kicker_name = self.format_name(home_kicker.name)
		away_kicker_name = self.format_name(away_kicker.name)

		home_score = self.get_score(home_kicker_name, match.home_team.team_name, week_stats_df)
		away_score = self.get_score(away_kicker_name, match.away_team.team_name, week_stats_df)

		self.home_team = home_score
		self.away_team = away_score

	def get_kicker(self, lineup):
		for player in lineup:
			if 'K' == player.position:
				return player

	def format_name(self, player_name):
		names = player_name.split(' ')
		return names[0][0] + '.' + names[1]

	def get_score(self, player_name, team_name, week_stats_df):
		score = KickerScore.KickerScore(player_name, team_name)

		kicks = self.get_relevant_plays(player_name, stattypes.kicks + stattypes.score, week_stats_df)
		score.add_kick_score(kicks)

		tackles = self.get_relevant_plays(player_name, stattypes.tackles, week_stats_df)
		score.add_tackle_score(tackles)

		return score

	def get_relevant_plays(self, player, columns, week_stats_df):
		return week_stats_df.loc[week_stats_df[columns].eq(player).any(1)][columns]

	def reprJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__,
						  sort_keys=True, indent=4)