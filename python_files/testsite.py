import math

text_string = 'Define what would you have to do today to consider the day a success'
def determine_rows(ksu_description):
	return int(math.ceil((len(text_string)/50.0)))

print determine_rows(text_string)
