import requests
headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.flightlist.io/'}
params = {'fly_from': 'TR', 'fly_to': 'MED', 'date_from': '02/07/2026', 'date_to': '31/12/2026', 'adults': '1', 'curr': 'TRY', 'limit': '100', 'sort': 'price', 'flight_type': 'oneway', 'adult_hand_bag': '0', 'adult_hold_bag': '0'}
r = requests.get('https://www.flightlist.io/api/search.php', params=params, headers=headers, timeout=60)
data = r.json().get('data', [])
akt = [f for f in data if len(f.get('route', [])) - 1 == 1]
print(f'Total: {len(data)}, 1-stop: {len(akt)}')
for f in akt[:3]:
    price = f.get('price')
    routes = f.get('route', [])
    print(f'  Price: {price}, Routes: {len(routes)}')
    for r in routes:
        dep = r.get('local_departure', '')
        arr = r.get('local_arrival', '')
        print(f'    {r.get("flyFrom")}->{r.get("flyTo")} | {dep[:16]}->{arr[:16]} | {r.get("airline")}')