import requests

h = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.flightlist.io/'}

p_jed = {'fly_from': 'TR', 'fly_to': 'JED', 'date_from': '03/07/2026', 'date_to': '13/07/2026', 'adults': '1', 'curr': 'TRY', 'limit': '100', 'sort': 'price', 'flight_type': 'oneway', 'adult_hand_bag': '0', 'adult_hold_bag': '0'}
p_med = {'fly_from': 'TR', 'fly_to': 'MED', 'date_from': '03/07/2026', 'date_to': '13/07/2026', 'adults': '1', 'curr': 'TRY', 'limit': '100', 'sort': 'price', 'flight_type': 'oneway', 'adult_hand_bag': '0', 'adult_hold_bag': '0'}

def get_top5(p, stops):
    r = requests.get('https://www.flightlist.io/api/search.php', params=p, headers=h, timeout=60)
    d = r.json().get('data', [])
    arr = []
    for f in d:
        rts = f.get('route', [])
        if len(rts) - 1 == stops:
            rts_list = rts
            dep = rts[0].get('local_departure','')
            frm = rts[0].get('cityFrom','')
            ac = rts[0].get('airline','?')
            arr.append({'price': f.get('price'), 'date': dep[:10], 'from': frm, 'airline': ac})
    arr.sort(key=lambda x: x['price'])
    return arr[:5]

print('=== 01-CIDDE-DIREKT ===')
for i, f in enumerate(get_top5(p_jed, 0)):
    print(str(i+1) + '. ' + str(f['price']) + ' TL | ' + f['date'] + ' | ' + f['airline'] + ' | ' + f['from'])

print()
print('=== 02-MEDINE-DIREKT ===')
for i, f in enumerate(get_top5(p_med, 0)):
    print(str(i+1) + '. ' + str(f['price']) + ' TL | ' + f['date'] + ' | ' + f['airline'] + ' | ' + f['from'])

print()
print('=== 03-CIDDE-AKTARMALI ===')
for i, f in enumerate(get_top5(p_jed, 1)):
    print(str(i+1) + '. ' + str(f['price']) + ' TL | ' + f['date'] + ' | ' + f['airline'] + ' | ' + f['from'])

print()
print('=== 04-MEDINE-AKTARMALI ===')
for i, f in enumerate(get_top5(p_med, 1)):
    print(str(i+1) + '. ' + str(f['price']) + ' TL | ' + f['date'] + ' | ' + f['airline'] + ' | ' + f['from'])
