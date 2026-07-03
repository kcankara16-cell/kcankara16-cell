import requests
h = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.flightlist.io/'}
p = {'fly_from': 'TR', 'fly_to': 'MED', 'date_from': '02/07/2026', 'date_to': '31/12/2026', 'adults': '1', 'curr': 'TRY', 'limit': '100', 'sort': 'price', 'flight_type': 'oneway', 'adult_hand_bag': '0', 'adult_hold_bag': '0'}
r = requests.get('https://www.flightlist.io/api/search.php', params=p, headers=h, timeout=60)
d = r.json().get('data', [])
print(f'Total: {len(d)}')
n1 = 0
for f in d:
    if len(f.get('route', [])) - 1 == 1:
        n1 += 1
print(f'1-stop: {n1}')