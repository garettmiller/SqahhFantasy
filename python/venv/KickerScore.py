import Score
import stattypes

class KickerScore(Score.Score):

	fg_40_yd = 3
	fg_50_yd = 4
	fg_60_yd = 6
	fg_70_yd = 8
	kick_failed = -2

	pat_success = 1
	pp_tackle = 5

	def add_kick_score(self, kicks):
		self.add_pat_score(kicks)
		self.add_fg_score(kicks)


	def add_pat_score(self, kicks):
		pats = kicks.loc[kicks["extra_point_attempt"] == 1.0]

		successful_pats = pats.loc[pats["extra_point_result"] == "good"]
		self.calculate_kick_type(successful_pats, self.pat_success, pats, "PAT", "")


	def calculate_kick_type(self, successful_kicks, success_points, all_kicks, kick_type_string, distance_string, sub_miss=True):
		num_successful_kicks = len(successful_kicks.index)
		self.calculate_score(num_successful_kicks, success_points, "Successful " + kick_type_string + " " + distance_string)
		if self.is_game_winning_kick(successful_kicks):
			self.add_game_winning_kick(success_points)

		if sub_miss:
			num_failed_pats = len(self.get_dropped_rows(all_kicks, successful_kicks).index)
			self.calculate_score(num_failed_pats, self.kick_failed, "Failed " + kick_type_string)


	def calculate_score(self, num_scores, point_per, intro):
		if num_scores == 0:
			return
		full_score = num_scores * point_per
		self.add_to_total(full_score)
		self.add_breakdown(intro + ": " + str(full_score))


	def add_fg_score(self, kicks):
		fgs = kicks.loc[kicks["field_goal_attempt"] == 1.0]

		fgs_40 = fgs.loc[fgs["kick_distance"] < 40.0]
		self.calculate_fg_scores(fgs_40, self.fg_40_yd, "<40yds")

		fgs_50 = fgs.loc[(fgs["kick_distance"] >= 40.0) & (fgs["kick_distance"] < 50.0)]
		self.calculate_fg_scores(fgs_50, self.fg_50_yd, "40-49yds")

		fgs_60 = fgs.loc[(fgs["kick_distance"] >= 50.0) & (fgs["kick_distance"] < 60.0)]
		self.calculate_fg_scores(fgs_60, self.fg_60_yd, "50-59yds", False)

		fgs_70 = fgs.loc[fgs["kick_distance"] >= 60.0]
		self.calculate_fg_scores(fgs_70, self.fg_70_yd, ">60yds", False)


	def calculate_fg_scores(self, fgs, success_points, distance_string, sub_miss=True):
		successful_fgs = fgs.loc[fgs["field_goal_result"] == "made"]
		self.calculate_kick_type(successful_fgs, success_points, fgs, "FG", distance_string, sub_miss)


	def is_game_winning_kick(self, fgs):
		final_score = fgs.loc[(fgs["home_score"] == fgs["total_home_score"]) & (fgs["away_score"] == fgs["total_away_score"])]
		is_winning_score = not final_score.loc[(final_score["posteam_score"] < final_score["defteam_score_post"]) & (final_score["posteam_score_post"] > final_score["defteam_score_post"])].empty
		return is_winning_score


	def add_game_winning_kick(self, success_points):
		self.calculate_score(1, success_points, "Game Winning Kick")


	def get_dropped_rows(self, original_df, new_df):
		return original_df[~original_df.index.isin(new_df.index)]


	def add_tackle_score(self, tackles):
		self.calculate_score(len(tackles.index), self.pp_tackle, "Tackles")