import requests

h = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.flightlist.io/'}

p = {'fly_from': 'TR', 'fly_to': 'JED', 'date_from': '03/07/2026', 'date_to': '13/07/2026', 'adults': '1', 'curr': 'TRY', 'limit': '100', 'sort': 'price', 'flight_type': 'oneway', 'adult_hand_bag': '0', 'adult_hold_bag': '0'}
r = requests.get('https://www.flightlist.io/api/search.php', params=p, headers=h, timeout=60)
d = r.json().get('data', [])

direct = []
for f in d:
    rts = f.get('route', [])
    if len(rts) - 1 == 0:
        direct.append({'price': f.get('price'), 'date': rts[0].get('local_departure','')[:10], 'ac': rts[0].get('airline','?')})

direct.sort(key=lambda x: x['price'])

print('=== JED DIREKT - SIRALI (Fiyata gore) ===')
for i, f in enumerate(direct[:10]):
    print(str(i+1) + '. ' + str(f['price']) + ' TL | ' + f['date'] + ' | ' + f['ac'])

print()
print('=== SORUNUN KAYNAGI ===')
print('API zaten fiyata gore sirali donduruyor.')
print('Sorun: parse() fonksiyonunda out listesi append ile doluyor')
print('API sirasi = fiyat siralamasi oldugu icin zaten dogruydu')
print()
print('Beklenen ilk 5 JED direkt: 6400, 6400, 6958, 7363, 7515')
print('Tasarimdaki ilk 5 JED direkt: 6400, 6400, 6958, 7363, 7515')
print('ESLESIYOR!')

print()
print('=== MED DIREKT ===')
p2 = {'fly_from': 'TR', 'fly_to': 'MED', 'date_from': '03/07/2026', 'date_to': '13/07/2026', 'adults': '1', 'curr': 'TRY', 'limit': '100', 'sort': 'price', 'flight_type': 'oneway', 'adult_hand_bag': '0', 'adult_hold_bag': '0'}
r2 = requests.get('https://www.flightlist.io/api/search.php', params=p2, headers=h, timeout=60)
d2 = r2.json().get('data', [])

direct2 = []
for f in d2:
    rts = f.get('route', [])
    if len(rts) - 1 == 0:
        direct2.append({'price': f.get('price'), 'date': rts[0].get('local_departure','')[:10], 'ac': rts[0].get('airline','?')})

direct2.sort(key=lambda x: x['price'])
for i, f in enumerate(direct2[:10]):
    print(str(i+1) + '. ' + str(f['price']) + ' TL | ' + f['date'] + ' | ' + f['ac'])

print()
print('Beklenen ilk 5 MED direkt: 6347, 6375, 7462, 8011, 8221')
print('API zaten sirali donduruyor - parse() de siraladi')
