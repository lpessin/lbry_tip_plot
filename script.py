import requests
import matplotlib.pyplot as plt


def get_claims_ids():
    ids = []
    for b in range(0, 30):
        call = requests.post("http://localhost:5279", json={"method": "claim_list", "params": {
            "claim_type": ['channel', 'stream'],
            'page_size': 50,
            'page': b,
            'no_totals': True
            }}).json().get('result').get('items')
        for i in call:
            claim_id = i['claim_id']
            ids.append(claim_id)
    print(len(ids))
    return ids


def get_txo_plot(ids, days_back):
    days_back = int(days_back)
    call = requests.post("http://localhost:5279", json={"method": "txo_plot", "params": {
        'type': 'support',
        'claim_id': ids,
        'is_my_output': True,
        'is_not_my_input': True,
        'days_back': days_back,
        'exclude_internal_transfers': True,
    }}).json().get('result')
    return call

# Inputs and calls
print(5*'=' + 'Tip Plot' + 5*'=')
id = input('Claim Id (or type 0 for all claims): ')
days = input('Days back (or type 0 for all time): ')
days = int(days)
days = days - 1
if id == '0':
    id = get_claims_ids()
    if days == -1:
        result = get_txo_plot(ids=id, days_back=10000)
    else:
        result = get_txo_plot(ids=id, days_back=days)
    name = 'Daily Tips from all Claims'
else:
    if days == -1:
        result = get_txo_plot(ids=id, days_back=10000)
    else:
        result = get_txo_plot(ids=id, days_back=days)
    name = 'Daily Tips from Claim ID: ' + id

# Plot
tips = []
date = []
for a in result:
    date.append(a['day'])
    tips.append(float(a['total']))
bars = plt.bar(date, height=tips, width=.4)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x(), yval + 0.1, yval)
plt.ylabel('Tip amount')
name = name + ' Total: ', sum(tips)
plt.title(name)
plt.xticks(rotation=70)
plt.show()
