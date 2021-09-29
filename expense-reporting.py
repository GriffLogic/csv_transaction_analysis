import csv, time, os

bank_file = open('checkingaug.csv', 'r')
bank_file_reader = csv.reader(bank_file)

CATEGORY = {
    'Groceries': 0,
    'Convenience Stores': 1,
    'Gas': 2,
    'Fast Food': 3,
    'Monthly Expenses': 4,
    'Rent': 5,
    'Miscellaneous': 6,
    'Transfers': 7
}

# https://stackoverflow.com/questions/483666/reverse-invert-a-dictionary-mapping
DESCRIPTION = {v: k for k, v in CATEGORY.items()}

categories_keywords = [['woodmans', 'meijer'], ['road ranger', 'caseys', 'shell',
                        'thorntons', 'marathon', "bucky's", 'fas mart', 'speedway', 'kwik trip'], ['tollway mobil'],
                       ['subway', 'taco bell', 'jimmy johns', 'starbucks', 'arbys', "chubby's", 'fastacos',
                        'chipotle', "mcdonald's", 'culvers', "culver's", 'pp*dognsuds', 'burger king', 'panera bread',
                        'sbarro', 'dunkin', "wendy's"], ['butcherbox', 'delta dental', 'comcast', 'planet fit',
                        'itprotv', 'norton', 'state farm', 'american funds', 'netflix', 'family heritage',
                        'legalshield'], ['rock valley property'], ['bedbath+beyond', 'binnys', 'buffalo wild wings',
                        'amazon', 'dc estate winery', 'smkybones']]


class Entry:
    def __init__(self, data):
        self.data = data


def set_entries(csv_reader):
    temp_entries = []
    for row in csv_reader:
        temp_entries.append(Entry(row))
    del temp_entries[0]    # Get rid of column descriptions.
    return temp_entries


def set_unique_vendors(entry_list):
    temp_unique_vendors = []

    for vendor in entry_list:    # Create list of unique_vendors
        if len(temp_unique_vendors) != 0:
            i = 1
            for listed_vendor in temp_unique_vendors:
                if (vendor.data[3] != listed_vendor) and (i == len(temp_unique_vendors)):
                    temp_unique_vendors.append(vendor.data[3])
                elif vendor.data[3] == listed_vendor:
                    break
                else:
                    i += 1
        else:
            temp_unique_vendors.append(vendor.data[3])
    return temp_unique_vendors


def stack_vendors(entry_list, vendors_list):    # Creates stacks of entries per unique vendor.
    # https://stackoverflow.com/questions/7745562/appending-to-2d-lists-in-python
    temp_stacks = [[] for l in range(len(vendors_list))]    # Original was: [[]] * len(vendors_list) | Caused Duplicates
    t = 0
    while t < len(entry_list):
        i = 0
        while i < len(vendors_list):
            if entry_list[t].data[3] == vendors_list[i]:
                temp_stacks[i].append(entry_list[t])
                t += 1
                break
            else:
                i += 1
    return temp_stacks


def set_groups(stack_list, categories_list):
    temp_groups = [[] for g in range(len(categories_list) + 1)]    # +1 extra list for deposits and transfers.
    for stack in stack_list:
        found = False
        c = 0
        for category in categories_list:
            for keyword in range(len(category)):
                temp_description = stack[0].data[3].lower()
                if temp_description.find(category[keyword]) > -1:
                    temp_groups[c].extend(stack)
                    found = True
                    break
                elif (stack[0].data[5] == 'CR') or (temp_description.find('home banking transfer') > -1):
                    temp_groups[7].extend(stack)
                    found = True
                    break
            if found:
                break
            elif (not found) and (c == (len(categories_list) - 1)):
                temp_groups[c].extend(stack)
                break
            else:
                c += 1
    for group in temp_groups:
        group.sort(key=lambda z: z.data[3])
    return temp_groups


def get_group_costs(group_list):
    group_num = 0
    for group in group_list[0:7]:
        temp_cost = 0
        for transaction in group:
            temp_cost = float(temp_cost) + float(transaction.data[4])
        print(f'Total cost of {DESCRIPTION[group_num]} for August: {round(temp_cost * 100) / 100}')
        group_num += 1


entries = set_entries(bank_file_reader)
bank_file.close()

unique_vendors = set_unique_vendors(entries)
stacks = stack_vendors(entries, unique_vendors)
groups = set_groups(stacks, categories_keywords)
get_group_costs(groups)

for x in entries:
    print(x.data[3])


#total_deposit = 0
#total_transfer = 0
#for transaction in groups[7]:
#    if transaction.data[5] == 'CR':
#        total_deposit += float(transaction.data[4])
#    else:
#        total_transfer += float(transaction.data[4])
#
#print(f'\nTotal deposits: ${round(total_deposit * 100) / 100}')
#print(f'\nTotal transferred to savings: ${round(total_transfer * 100) / 100}')