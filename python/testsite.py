import math


def calculate_mission_reward(eod_merits, merits_goal):
	
	bracket_size = 20
	reward_factor = 1
	reward = 0

	range_end = eod_merits - merits_goal

	if range_end < 0:
		reward_factor = -1
		range_end = -range_end

	for merit in range(0, range_end):
		merit_reward = math.floor(merit/bracket_size) + 1
		reward += merit_reward

	return reward * reward_factor


print calculate_mission_reward(102, 105)

