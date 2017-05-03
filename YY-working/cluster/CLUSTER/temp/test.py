import csv
with open('test.csv', 'rb') as f:
	reader = csv.reader(f)
	your_list = list(reader)

	print your_list
