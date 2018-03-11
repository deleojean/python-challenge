import sys, os, csv
# sys.path.append('../Plugins')
# from DateTranslator    import DateTranslator
# from DateValidator     import DateValidator
# from NumericTranslator import NumericTranslator
# from NumericValidator  import NumericValidator

def csv_collector(*files):
    new_dataset = []

    for file in files:
        if os.path.isfile(file): # validate file exist

            with open(file, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader: new_dataset.append(row)

        else:
            print(f"ERROR [Collection] No such file or directory: '{file}'")
            print(f"ERROR [Collection] Fail csv data merge to dataset: '{file}'")

    return new_dataset

# collection
election_data = []
election_data = csv_collector('raw_data/election_data_1.csv', 'raw_data/election_data_2.csv')

# for i, j in enumerate(election_data):
#        print(f"{i}  {j}")

key1 = 'Voter ID'
key2 = 'County'
key3 = 'Candidate'

# The total number of votes cast
votes = [data[key1] for data in election_data]
total_votes = len(votes)

# A complete list of candidates who received votes
candidates = [data[key3] for data in election_data]
candidates = set(candidates) # set to unqiue values

# The total number of votes each candidate won
candidate_votes = {}

for candidate in candidates:
    votes = [data for data in election_data if data[key3] == candidate]
    candidate_votes.update({candidate: len(votes)})

candidate_votes

candidate_percentage = {}
percentage           = 0

# The percentage of votes each candidate won
for candidate in candidates:
    percentage = (candidate_votes[candidate] / total_votes) * 100 if candidate_votes[candidate] > 0 else percentage
    candidate_percentage.update({candidate: round(percentage, 1)})

candidate_percentage

# The winner of the election based on popular vote.
votes = 0

for key, value in candidate_votes.items():
    if value > votes:
        votes  = value
        winner = key

winner

def election_table(**kwargs):
    print(f"\n {kwargs['title'].title()}") # column headers
    print('-' * 60)

    print(f" Total Votes: {kwargs['total']}")
    print('-' * 60)

    for key, value in kwargs['percentage'].items():
        print(f" {key}: ".ljust(11) + f"{value}%".ljust(6) + f" ({kwargs['votes'][key]})")
    print('-' * 60)

    print(f" Winner: {kwargs['winner']}")
    print('-' * 60)

election_table(title='election results', total=total_votes, percentage=candidate_percentage, votes=candidate_votes, winner=winner)
