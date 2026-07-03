"""
TURKISH FLIGHT DESIGN v7.0 - PIXEL PERFECT GRID
8px Grid | 3 Column | Premium Typography
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests
import os
from datetime import datetime

# === Font ===
def ff(size, w="r"):
    for p in {
        "r":  ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"],
        "b":  ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"],
        "bl": ["C:/Windows/Fonts/segoeuiz.ttf", "C:/Windows/Fonts/ariblk.ttf"],
        "l":  ["C:/Windows/Fonts/segoeuil.ttf", "C:/Windows/Fonts/arial.ttf"],
    }.get(w, []):
        try: return ImageFont.truetype(p, size)
        except: pass
    return ImageFont.load_default()

def rr(d, xy, r, **kw): d.rounded_rectangle(xy, radius=r, **kw)

# === Colors ===
BG = (252, 252, 253)
WHITE = (255, 255, 255)
GOLD = (212, 175, 55)
GOLD_LIGHT = (255, 242, 200)
DARK_GREEN = (16, 122, 73)
GREEN = (0, 150, 80)
RED = (220, 50, 50)
ORANGE = (234, 130, 30)
BLUE = (50, 120, 220)
PURPLE = (130, 80, 200)
BLACK = (20, 20, 20)
TEXT_1 = (30, 30, 40)
TEXT_2 = (80, 90, 110)
TEXT_3 = (140, 150, 165)
DIV = (230, 232, 238)
DIV_2 = (245, 246, 250)
BG_CARD = (248, 249, 251)

PRICE_COLS = [GREEN, BLUE, PURPLE, ORANGE, RED]

# === Sizes ===
W, H = 1080, 1350
ML = MR = 48
CW = W - ML - MR

# Grid: 8px base
G = 8  # Grid unit

# === Airlines & Airports ===
AIRLINES = {
    'TK': ('THY', (10, 100, 180)),
    'PC': ('Pegasus', (220, 45, 55)),
    'VF': ('AJet', (30, 155, 210)),
    'F3': ('Flyadeal', (0, 155, 95)),
    'XY': ('flynas', (225, 75, 0)),
    'SV': ('Saudia', (0, 95, 155)),
    'A3': ('Aegean', (15, 135, 200)),
    'SM': ('AirCairo', (0, 140, 200)),
    'MS': ('EgyptAir', (180, 155, 60)),
    'EY': ('Etihad', (175, 125, 45)),
    'RJ': ('Royal', (0, 95, 155)),
}

AIRPORTS = {
    'IST': 'İstanbul', 'SAW': 'İstanbul SAW', 'ESB': 'Ankara', 'ADB': 'İzmir',
    'TZX': 'Trabzon', 'RZV': 'Rize-Artvin', 'AYT': 'Antalya',
    'JED': 'Cidde', 'MED': 'Medine', 'ATH': 'Atina',
    'CAI': 'Kahire', 'RUH': 'Riyad', 'DMM': 'Dammam', 'AMM': 'Amman',
    'KWI': 'Kuveyt', 'DOH': 'Doha', 'AUH': 'Abu Dabi',
}

MONTHS = ['', 'Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
          'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']


def get_airport(code): return AIRPORTS.get(code, code)
def get_airline(code):
    if code in AIRLINES: return AIRLINES[code]
    return (code, (100, 100, 100))

def fmt_date(s):
    try:
        y, m, d = s.split('-')
        return f"{int(d)} {MONTHS[int(m)]} {y}"
    except: return s or "Temmuz 2026"

def fmt_dur(m):
    if not m: return "-"
    h, d = divmod(m, 60)
    return f"{h}sa {d}dk" if h and d else (f"{h} saat" if h else f"{d} dk")

def fmt_wait(m):
    if not m: return None
    h, d = divmod(m, 60)
    return f"{h}sa {d}dk" if h and d else (f"{h} saat" if h else f"{d} dk")


# === Icons 20px ===
def icon(d, x, y, t, c):
    s = 20
    if t == 'plane':
        d.polygon([(x+18,y+10),(x+12,y+7),(x+10,y+10),(x+2,y+11),(x+10,y+11),(x+12,y+13),(x+12,y+10)], fill=c)
    elif t == 'clock':
        d.ellipse([x+1,y+1,x+19,y+19], outline=c, width=2)
        d.line([(x+10,y+10),(x+10,y+4)], fill=c, width=2)
        d.line([(x+10,y+10),(x+14,y+12)], fill=c, width=2)
    elif t == 'cal':
        d.rounded_rectangle([x+2,y+4,x+18,y+18], radius=2, outline=c, width=2)
        d.line([(x+2,y+8),(x+18,y+8)], fill=c, width=2)
        d.line([(x+5,y+1),(x+5,y+5)], fill=c, width=2)
        d.line([(x+15,y+1),(x+15,y+5)], fill=c, width=2)
    elif t == 'seat':
        d.rounded_rectangle([x+1,y+3,x+19,y+17], radius=2, outline=c, width=2)
        d.rectangle([x+4,y+6,x+9,y+12], outline=c, width=1)
        d.rectangle([x+11,y+6,x+16,y+12], outline=c, width=1)
    elif t == 'bag':
        d.rounded_rectangle([x+2,y+5,x+18,y+17], radius=2, outline=c, width=2)
        d.rounded_rectangle([x+6,y+2,x+14,y+6], outline=c, width=2)
    elif t == 'door':
        d.polygon([(x+1,y+6),(x+10,y+1),(x+19,y+6),(x+19,y+18),(x+1,y+18)], outline=c, width=2)
        d.line([(x+5,y+10),(x+15,y+10)], fill=c, width=2)
    elif t == 'ticket':
        d.rounded_rectangle([x+1,y+5,x+19,y+15], radius=2, outline=c, width=2)
        d.line([(x+10,y+5),(x+10,y+15)], fill=c, width=1)


def fetch(fr, to):
    h = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.flightlist.io/'}
    p = {'fly_from': fr, 'fly_to': to, 'date_from': '02/07/2026', 'date_to': '31/12/2026',
         'adults': '1', 'curr': 'TRY', 'limit': '100', 'sort': 'price', 'flight_type': 'oneway',
         'adult_hand_bag': '0', 'adult_hold_bag': '0'}
    r = requests.get('https://www.flightlist.io/api/search.php', params=p, headers=h, timeout=60)
    return r.json().get('data', []) if r.status_code == 200 else []


def parse(flights, stops=None):
    out = []
    for f in flights:
        rts = f.get('route', [])
        if not rts: continue
        n = len(rts) - 1
        if stops is not None and n != stops: continue
        first, last = rts[0], rts[-1]
        price = f.get('price', 0)
        codes = list({r.get('airline', '?') for r in rts})
        legs = []
        tot = 0
        for r in rts:
            dep = r.get('local_departure', '')
            arr = r.get('local_arrival', '')
            td = dep.split('T')[1][:5] if 'T' in dep else '--'
            ta = arr.split('T')[1][:5] if 'T' in arr else '--'
            try:
                d1 = datetime.fromisoformat(dep.replace('Z', '+00:00'))
                d2 = datetime.fromisoformat(arr.replace('Z', '+00:00'))
                tot += int((d2 - d1).total_seconds() / 60)
            except: pass
            ac = r.get('airline', '?')
            an, acr = get_airline(ac)
            legs.append({
                'from': r.get('flyFrom'), 'to': r.get('flyTo'),
                'fn': get_airport(r.get('flyFrom')),
                'tn': get_airport(r.get('flyTo')),
                'td': td, 'ta': ta, 'ac': ac, 'an': an, 'cr': acr
            })
        stype = "Direkt" if n == 0 else f"{n} Aktarmalı"
        date_str = fmt_date(first.get('local_departure', '').split('T')[0])
        waits = []
        for i in range(len(rts) - 1):
            try:
                a = datetime.fromisoformat(rts[i].get('local_arrival','').replace('Z','+00:00'))
                b = datetime.fromisoformat(rts[i+1].get('local_departure','').replace('Z','+00:00'))
                waits.append(int((b - a).total_seconds() / 60))
            except: waits.append(0)
        out.append({
            'price': price, 'legs': legs, 'stops': n,
            'codes': '+'.join(codes[:2]),
            'stype': stype, 'date': date_str,
            'dur': fmt_dur(tot),
            'waits': [fmt_wait(w) for w in waits],
            'cabin': 'Ekonomi', 'bagaj': 'Dahil Değil',
            'terminal': 'Belirtilmemiş', 'sefer': 'Belirtilmemiş',
        })
    return out[:5]


def create(filename, title, subtitle, flights, footer):
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)

    # === HEADER (0-130px) ===
    for y in range(130):
        t = y / 130
        v = int(252 - 2 * t)
        d.line([(0, y), (W, y)], fill=(v, v, v + 1))

    # Logo
    rr(d, (ML, 24, ML + 80, 104), 16, fill=GOLD)
    icon(d, ML + 30, 52, 'plane', WHITE)

    # Title - logo ile 8-10px fazla bosluk
    d.text((ML + 108, 30), title, font=ff(32, 'b'), fill=BLACK, anchor='lm')
    d.text((ML + 108, 72), subtitle, font=ff(14, 'l'), fill=TEXT_3, anchor='lm')

    # Right info
    rr(d, (W - MR - 180, 24, W - MR, 56), 12, fill=DIV_2, outline=DIV, width=1)
    d.text((W - MR - 90, 40), "FLIGHTLIST.IO", font=ff(11, 'b'), fill=BLACK, anchor='mm')
    rr(d, (W - MR - 180, 64, W - MR, 96), 12, fill=WHITE, outline=GOLD, width=1)
    d.text((W - MR - 90, 80), "1 Yetişkin · Ekonomi", font=ff(10, 'l'), fill=TEXT_2, anchor='mm')

    # Legend
    ly = 118
    d.text((ML, ly), "Fiyat Durumu:", font=ff(10, 'b'), fill=TEXT_2, anchor='lm')
    lx = ML + 100
    for c, l in [(GREEN, "En Ucuz"), (BLUE, "Uygun"), (PURPLE, "Orta"), (ORANGE, "Yüksek"), (RED, "En Pahalı")]:
        d.ellipse([lx, ly - 4, lx + 12, ly + 8], fill=c)
        d.text((lx + 16, ly + 2), l, font=ff(10, 'b'), fill=TEXT_2, anchor='lm')
        lx += 88

    # === CARDS ===
    top = 148
    n = min(len(flights), 5)
    if n == 0:
        img.save(filename, "PNG", quality=95)
        print(f"OK {os.path.basename(filename)} | Uçuş bulunamadı")
        return
    gap = 12  # Kartlar arasi bosluk azaltildi
    footer_h = 100
    avail = H - top - footer_h - (n - 1) * gap
    ch = avail // n  # ch ~ 215px

    for i, fl in enumerate(flights):
        cx = ML
        cy = top + i * (ch + gap)

        legs = fl['legs']
        if not legs: continue
        stops = fl['stops']
        pc = PRICE_COLS[i]

        # PREMIUM YUMUSAK GOLGE
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(sh)
        rr(sd, (cx + 4, cy + 10, cx + CW + 4, cy + ch + 10), 20, fill=(0, 0, 0, 15))
        sh1 = sh.filter(ImageFilter.GaussianBlur(20))
        img.paste(sh1, (0, 0), sh1)
        d = ImageDraw.Draw(img)

        # Card
        rr(d, (cx, cy, cx + CW, cy + ch), 20, fill=WHITE, outline=(230, 232, 238), width=1)
        rr(d, (cx, cy + 16, cx + 4, cy + ch - 16), 0, fill=pc)

        pad = 24

        # ==============================================================
        # COL 1: SOL - Havayolu kutusu (fiyat kutusuyla ayni stil)
        # ==============================================================
        c1_x = cx + pad
        c1_y = cy + pad
        c1_w = 150
        c1_h = ch - 2 * pad  # Fiyat kutusuyla ayni yukseklik

        ac = legs[0]['ac']
        an = legs[0]['an']
        cr = legs[0]['cr']

        # Sol kutu - fiyat kutusuyla ayni radius ve stil
        rr(d, (c1_x, c1_y, c1_x + c1_w, c1_y + c1_h), 18, fill=pc)

        # Ust: Havayolu ismi (kucuk, ince)
        d.text((c1_x + c1_w // 2, c1_y + c1_h // 2 - 32), an, font=ff(13, 'b'), fill=(255, 255, 255, 220), anchor='mm')

        # Orta: Havayolu kodu (buyuk, kalin)
        d.text((c1_x + c1_w // 2, c1_y + c1_h // 2 - 4), fl['codes'], font=ff(38, 'bl'), fill=WHITE, anchor='mm')

        # Alt: Direkt Uçuş yazisi - buton stili
        btn_lbl = "Direkt Uçuş" if stops == 0 else fl['stype']
        btn_w = 110
        btn_x = c1_x + c1_w // 2 - btn_w // 2
        btn_y = c1_y + c1_h // 2 + 16
        rr(d, (btn_x, btn_y, btn_x + btn_w, btn_y + 26), 8, fill=(255, 255, 255))
        d.text((c1_x + c1_w // 2, btn_y + 13), btn_lbl, font=ff(12, 'b'), fill=pc, anchor='mm')

        # ==============================================================
        # COL 3: SAG - Fiyat kutusu (tam saga yasli, dikey ortali)
        # ==============================================================
        price_w = 160
        price_x = cx + CW - pad - price_w
        price_h = ch - 2 * pad
        price_y = cy + pad

        rr(d, (price_x, price_y, price_x + price_w, price_y + price_h), 18, fill=pc)
        # Fiyat - ana odak noktasi
        pv = f"{fl['price']:,}".replace(',', '.')
        d.text((price_x + price_w // 2, price_y + price_h // 2 - 20), pv, font=ff(46, "bl"), fill=WHITE, anchor='mm')
        # TL - fiyatin altinda, ortali
        d.text((price_x + price_w // 2, price_y + price_h // 2 + 12), "TL", font=ff(20, "b"), fill=(255, 255, 255, 230), anchor='mm')
        # Baslayan Fiyatlarla - buyuk, Medium, kontrastli, kutunun en altina yakin
        d.text((price_x + price_w // 2, price_y + price_h - 32), "Başlayan Fiyatlarla", font=ff(18, "r"), fill=WHITE, anchor='mm')

        # === COL 2: ORTA - Tarih + Rota + Saat (kart merkezi) ===
        c2_x = c1_x + c1_w + 24
        c2_w = price_x - 24 - c2_x  # fiyat kutusuna kadar
        c2_cx = c2_x + c2_w // 2

        # ALT BILGI SATIRI (kart altinda sabit)
        info_y = cy + ch - 48
        info_h = 36

        # SAAT KUTULARI (info row ustunde, 16px gap)
        time_h = 48
        time_y = info_y - 16 - time_h

        # ROTA (saat kutusunun ustunde, 16px gap)
        route_y = time_y - 16 - 12  # 12px = sehir yarim yukseklik

        # TARIH (rotanin ustunde, 16px gap)
        date_y = route_y - 16 - 28  # 28px = etiket+sehir+yarim kod

        # === TARIH (ustte, merkezde) ===
        date_text = fl['date']
        date_font = ff(15, 'b')
        date_tw = date_font.getbbox(date_text)[2]
        icw = 20  # icon genisligi
        total_dw = icw + 8 + date_tw
        dsx = c2_cx - total_dw // 2
        icon(d, dsx, date_y - 9, 'cal', TEXT_2)
        d.text((dsx + icw + 8, date_y), date_text, font=date_font, fill=BLACK, anchor='lm')

        # === ROTA (tarihin altinda, merkezde) ===
        fc = legs[0]['from']; tc = legs[-1]['to']
        fn = legs[0]['fn']; tn = legs[-1]['tn']

        # Eşit genişlikli iki kolon (c2_w / 2)
        col_half = c2_w // 2

        # Sol şehir - gerçek şehir ismi büyük, kod altında
        city_left_x = c2_x + 16
        d.text((city_left_x, route_y - 22), "KALKIS", font=ff(10, "b"), fill=TEXT_3, anchor='lm')
        d.text((city_left_x, route_y), fn, font=ff(24, "b"), fill=BLACK, anchor='lm')
        d.text((city_left_x, route_y + 22), f"({fc})", font=ff(12, "l"), fill=TEXT_3, anchor='lm')

        # Sağ şehir - gerçek şehir ismi büyük, kod altında
        city_right_x = c2_x + c2_w - 16
        d.text((city_right_x, route_y - 22), "VARIS", font=ff(10, "b"), fill=TEXT_3, anchor='rm')
        d.text((city_right_x, route_y), tn, font=ff(24, "b"), fill=BLACK, anchor='rm')
        d.text((city_right_x, route_y + 22), f"({tc})", font=ff(12, "l"), fill=TEXT_3, anchor='rm')

        # Ucak cizgisi (tam merkezde, 3px)
        fn_bbox_w = ff(24, "b").getbbox(fn)[2]
        tn_bbox_w = ff(24, "b").getbbox(tn)[2]
        line_y = route_y
        left_line_x = city_left_x + fn_bbox_w + 16
        right_line_x = city_right_x - tn_bbox_w - 16

        d.line([(left_line_x, line_y), (c2_cx - 14, line_y)], fill=pc, width=3)
        d.line([(c2_cx + 14, line_y), (right_line_x, line_y)], fill=pc, width=3)
        d.ellipse([c2_cx - 14, line_y - 14, c2_cx + 14, line_y + 14], fill=WHITE, outline=pc, width=2)
        icon(d, c2_cx - 10, line_y - 9, 'plane', pc)

        # === SAAT KUTULARI (tam ortalanmis, esit genislikte) ===
        time_w = 110
        time_gap = 16
        time_total = time_w * 2 + time_gap
        time_start = c2_cx - time_total // 2

        rr(d, (time_start, time_y, time_start + time_w, time_y + time_h), 12, fill=BG_CARD, outline=DIV, width=1)
        d.text((time_start + time_w // 2, time_y + 12), "KALKIS", font=ff(9, "b"), fill=TEXT_3, anchor='mm')
        d.text((time_start + time_w // 2, time_y + 34), legs[0]['td'], font=ff(24, "bl"), fill=BLACK, anchor='mm')

        t2_x = time_start + time_w + time_gap
        rr(d, (t2_x, time_y, t2_x + time_w, time_y + time_h), 12, fill=BG_CARD, outline=DIV, width=1)
        d.text((t2_x + time_w // 2, time_y + 12), "VARIS", font=ff(9, "b"), fill=TEXT_3, anchor='mm')
        d.text((t2_x + time_w // 2, time_y + 34), legs[-1]['ta'], font=ff(24, "bl"), fill=BLACK, anchor='mm')

        # === ALT BILGI SATIRI (2: Sure, Ekonomi - genis, saydam renkli, ortali) ===
        ix_end = price_x - 24
        n_info = 2
        gap_info = 20
        total_info_w = ix_end - cx - pad
        info_item_w = (total_info_w - gap_info) // n_info
        # Ortala
        ix = cx + pad + (total_info_w - (info_item_w * n_info + gap_info * (n_info - 1))) // 2

        # Sure - saydam renkli (yesil tonu)
        rr(d, (ix, info_y, ix + info_item_w, info_y + info_h), 12, fill=(220, 240, 230))
        icon(d, ix + 10, info_y + 8, 'clock', GREEN)
        d.text((ix + 34, info_y + info_h // 2), fl['dur'], font=ff(13, 'b'), fill=(20, 100, 60), anchor='lm')
        ix += info_item_w + gap_info

        # Ekonomi - saydam renkli (mavi tonu)
        rr(d, (ix, info_y, ix + info_item_w, info_y + info_h), 12, fill=(220, 230, 245))
        icon(d, ix + 10, info_y + 8, 'seat', BLUE)
        d.text((ix + 34, info_y + info_h // 2), fl['cabin'], font=ff(13, 'b'), fill=(20, 60, 120), anchor='lm')

    # === FOOTER ===
    fy = H - 80
    d.line([(ML, fy), (W - MR, fy)], fill=DIV, width=1)

    # Center
    d.text((W // 2, fy + 16), "GÜNCELLEME:", font=ff(10, 'b'), fill=TEXT_3, anchor='mm')
    d.text((W // 2, fy + 34), "2 TEMMUZ 2026", font=ff(14, 'b'), fill=BLACK, anchor='mm')

    # Right
    d.text((W - MR, fy + 16), "TRY · TEK YÖN · EKONOMİ", font=ff(10, 'b'), fill=TEXT_3, anchor='rm')
    d.text((W - MR, fy + 34), "GÜNCEL FİYATLAR", font=ff(14, 'b'), fill=BLACK, anchor='rm')

    # Bottom note
    d.text((W // 2, H - 24), footer, font=ff(10, 'l'), fill=TEXT_3, anchor='mm')

    img.save(filename, "PNG", quality=95)
    print(f"OK {os.path.basename(filename)} | {os.path.getsize(filename) // 1024} KB")


# === MAIN ===
print("=" * 50)
print("TURKISH FLIGHT DESIGN v7.0")
print("8px Grid | 3 Column | Pixel Perfect")
print("=" * 50)

c_all = fetch("TR", "JED")
m_all = fetch("TR", "MED")
print(f"Cidde: {len(c_all)} | Medine: {len(m_all)}")

c_dir = parse(c_all, 0)
c_akt = parse(c_all, 1)
m_dir = parse(m_all, 0)
m_akt = parse(m_all, 1)

b = r"C:\Users\birlikgrup\Desktop\proje"

c_footer = "Cidde Havâlimanı'ndan Mekke'ye ~90 km · ulaşım 1-1,5 saat"
m_footer = "Medine Havâlimanı'ndan Mescid-i Nebevi'ye ~20 km · ulaşım 20-30 dk"

create(f"{b}\\01-cidde-direkt.png", "Türkiye → Cidde (JED)", "En Ucuz 5 Direkt Uçuşu", c_dir, c_footer)
create(f"{b}\\02-medine-direkt.png", "Türkiye → Medine (MED)", "En Ucuz 5 Direkt Uçuşu", m_dir, m_footer)
create(f"{b}\\03-cidde-aktarmali.png", "Türkiye → Cidde (JED)", "En Ucuz 5 Aktarmalı Uçuşu", c_akt, c_footer)
create(f"{b}\\04-medine-aktarmali.png", "Türkiye → Medine (MED)", "En Ucuz 5 Aktarmalı Uçuşu", m_akt, m_footer)

print("Tamamlandi!")
