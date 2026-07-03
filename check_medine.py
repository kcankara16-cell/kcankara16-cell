import requests
headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.flightlist.io/'}
params = {'fly_from': 'TR', 'fly_to': 'MED', 'date_from': '03/07/2026', 'date_to': '13/07/2026', 'adults': '1', 'curr': 'TRY', 'limit': '100', 'sort': 'price', 'flight_type': 'oneway', 'adult_hand_bag': '0', 'adult_hold_bag': '0'}
r = requests.get('https://www.flightlist.io/api/search.php', params=params, headers=headers, timeout=60)
data = r.json().get('data', [])
akt = [f for f in data if len(f.get('route', [])) - 1 == 1]
print(f'1-aktarma count: {len(akt)}')
for f in akt[:3]:
    first = f['route'][0]
    dep = first.get('local_departure', '')
    date_part = dep.split('T')[0]
    price = f.get('price')
    print(f'  Date: {date_part}, Price: {price}')
