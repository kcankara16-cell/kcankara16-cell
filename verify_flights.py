import requests

h = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.flightlist.io/'}

print('=== JED DIREKT ===')
p = {'fly_from': 'TR', 'fly_to': 'JED', 'date_from': '03/07/2026', 'date_to': '13/07/2026', 'adults': '1', 'curr': 'TRY', 'limit': '100', 'sort': 'price', 'flight_type': 'oneway', 'adult_hand_bag': '0', 'adult_hold_bag': '0'}
r = requests.get('https://www.flightlist.io/api/search.php', params=p, headers=h, timeout=60)
d = r.json().get('data', [])

direct = []
akt = []
for f in d:
    rts = f.get('route', [])
    if len(rts) - 1 == 0:
        direct.append({'price': f.get('price'), 'date': rts[0].get('local_departure','')[:10], 'airline': rts[0].get('airline','?')})
    elif len(rts) - 1 == 1:
        ac = rts[0].get('airline','?')
        ac2 = rts[1].get('airline','?')
        akt.append({'price': f.get('price'), 'date': rts[0].get('local_departure','')[:10], 'airline': ac + '+' + ac2})

direct.sort(key=lambda x: x['price'])
akt.sort(key=lambda x: x['price'])

print('DIRECT:')
for i, f in enumerate(direct[:10]):
    print(str(i+1) + '. ' + str(f['price']) + ' TL | ' + f['date'] + ' | ' + f['airline'])

print()
print('AKTARMA:')
for i, f in enumerate(akt[:10]):
    print(str(i+1) + '. ' + str(f['price']) + ' TL | ' + f['date'] + ' | ' + f['airline'])

print()
print('=== MED DIREKT ===')
p2 = {'fly_from': 'TR', 'fly_to': 'MED', 'date_from': '03/07/2026', 'date_to': '13/07/2026', 'adults': '1', 'curr': 'TRY', 'limit': '100', 'sort': 'price', 'flight_type': 'oneway', 'adult_hand_bag': '0', 'adult_hold_bag': '0'}
r2 = requests.get('https://www.flightlist.io/api/search.php', params=p2, headers=h, timeout=60)
d2 = r2.json().get('data', [])

direct2 = []
akt2 = []
for f in d2:
    rts = f.get('route', [])
    if len(rts) - 1 == 0:
        direct2.append({'price': f.get('price'), 'date': rts[0].get('local_departure','')[:10], 'airline': rts[0].get('airline','?')})
    elif len(rts) - 1 == 1:
        ac = rts[0].get('airline','?')
        ac2 = rts[1].get('airline','?')
        akt2.append({'price': f.get('price'), 'date': rts[0].get('local_departure','')[:10], 'airline': ac + '+' + ac2})

direct2.sort(key=lambda x: x['price'])
akt2.sort(key=lambda x: x['price'])

print('DIRECT:')
for i, f in enumerate(direct2[:10]):
    print(str(i+1) + '. ' + str(f['price']) + ' TL | ' + f['date'] + ' | ' + f['airline'])

print()
print('AKTARMA:')
for i, f in enumerate(akt2[:10]):
    print(str(i+1) + '. ' + str(f['price']) + ' TL | ' + f['date'] + ' | ' + f['airline'])
