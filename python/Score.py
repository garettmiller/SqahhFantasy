import json

class Score:

	def __init__(self, player_name, team_name):
		self.team_name = team_name
		self.player_name = player_name
		self.total_score = 0
		self.score_breakdown = []

	def add_to_total(self, points):
		self.total_score = self.total_score + points

	def add_breakdown(self, breakdown):
		self.score_breakdown.append(breakdown)

	def print_score(self):
		print(self.team_name + " " + self.player_name + " " + str(self.total_score))
		print(self.score_breakdown)
		print("\n\n")

	def reprJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__,
						  sort_keys=True, indent=4)
