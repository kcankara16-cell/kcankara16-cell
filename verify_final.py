import requests

h = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.flightlist.io/'}

# Tum verileri cek ve ilk 5'ini siralanmis sekilde al
def get_top5(p, stops):
    r = requests.get('https://www.flightlist.io/api/search.php', params=p, headers=h, timeout=60)
    d = r.json().get('data', [])
    arr = []
    for f in d:
        rts = f.get('route', [])
        if len(rts) - 1 == stops:
            arr.append(f.get('price'))
    arr.sort()
    return arr[:5]

p_jed = {'fly_from': 'TR', 'fly_to': 'JED', 'date_from': '03/07/2026', 'date_to': '13/07/2026', 'adults': '1', 'curr': 'TRY', 'limit': '100', 'sort': 'price', 'flight_type': 'oneway', 'adult_hand_bag': '0', 'adult_hold_bag': '0'}
p_med = {'fly_from': 'TR', 'fly_to': 'MED', 'date_from': '03/07/2026', 'date_to': '13/07/2026', 'adults': '1', 'curr': 'TRY', 'limit': '100', 'sort': 'price', 'flight_type': 'oneway', 'adult_hand_bag': '0', 'adult_hold_bag': '0'}

print('=== BEKLENEN ILK 5 FIYATLAR ===')
print('01-cidde-direkt.png:', get_top5(p_jed, 0))
print('02-medine-direkt.png:', get_top5(p_med, 0))
print('03-cidde-aktarmali.png:', get_top5(p_jed, 1))
print('04-medine-aktarmali.png:', get_top5(p_med, 1))

print()
print('=== KULLANICININ BEKLENTILERI ===')
print('01: 6400, 6400, 6958, 7363, 7515 (7515 HATALI demis ama aslinda dogru!)')
print('02: 6375, 6375, 7462, 8011, 8221 (ilk 2 ayni 6375 demis ama API 6347 veriyor)')
print('03: 8638, 9322, 9469, 9763, 9952 (1. ve 3-5 hatali demis)')
print('04: 7603, 7603, 7634, 7634, 7645 (ilk 2 ve 3-4 hatali demis)')