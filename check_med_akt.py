import requests

h = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.flightlist.io/'}

p_med = {'fly_from': 'TR', 'fly_to': 'MED', 'date_from': '03/07/2026', 'date_to': '13/07/2026', 'adults': '1', 'curr': 'TRY', 'limit': '100', 'sort': 'price', 'flight_type': 'oneway', 'adult_hand_bag': '0', 'adult_hold_bag': '0'}
r = requests.get('https://www.flightlist.io/api/search.php', params=p_med, headers=h, timeout=60)
d = r.json().get('data', [])

akt = []
for f in d:
    rts = f.get('route', [])
    if len(rts) - 1 == 1:
        first = rts[0]
        price = f.get('price')
        dep_city = first.get('cityFrom', '')
        dep_airport = first.get('flyFrom', '')
        arr_city = first.get('cityTo', '')
        arr_airport = first.get('flyTo', '')
        ac = first.get('airline', '?')
        dep_time = first.get('local_departure', '')[:16]
        akt.append({'price': price, 'dep_city': dep_city, 'dep_airport': dep_airport, 'arr_city': arr_city, 'arr_airport': arr_airport, 'airline': ac, 'dep_time': dep_time})

akt.sort(key=lambda x: x['price'])

print('=== MED 1-AKTARMA - ILK 5 ===')
for i, f in enumerate(akt[:5]):
    print(str(i+1) + '. ' + str(f['price']) + ' TL')
    print('   Kalkis: ' + f['dep_city'] + ' (' + f['dep_airport'] + ')')
    print('   Varis: ' + f['arr_city'] + ' (' + f['arr_airport'] + ')')
    print('   Havayolu: ' + f['airline'] + ' | Saat: ' + f['dep_time'])
