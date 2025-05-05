# mock_trucks.py

MOCK_TRUCKS = {
    "İstanbul": [
        {
            "company": "Metro Lojistik",
            "trucks": 15,
            "capacity_per_truck": 5000,
            "status": "available",
            "location": "Çekmeköy Depo"
        },
        {
            "company": "Anadolu Transport",
            "trucks": 20,
            "capacity_per_truck": 7000,
            "status": "available",
            "location": "Hadımköy Liman"
        }
    ],
    "Ankara": [
        {
            "company": "Başkent Nakliyat",
            "trucks": 12,
            "capacity_per_truck": 5000,
            "status": "available",
            "location": "Ostim Depo"
        },
        {
            "company": "Ankara Lojistik",
            "trucks": 10,
            "capacity_per_truck": 6000,
            "status": "available",
            "location": "Sincan Depo"
        }
    ],
    "İzmir": [
        {
            "company": "Ege Lojistik",
            "trucks": 10,
            "capacity_per_truck": 6000,
            "status": "available",
            "location": "Aliağa Liman"
        },
        {
            "company": "Aegean Transport",
            "trucks": 8,
            "capacity_per_truck": 5500,
            "status": "available",
            "location": "Torbalı Depo"
        }
    ],
    "Bursa": [
        {
            "company": "Uludağ Transport",
            "trucks": 8,
            "capacity_per_truck": 5000,
            "status": "available",
            "location": "Organize Sanayi"
        }
    ],
    "Antalya": [
        {
            "company": "Akdeniz Lojistik",
            "trucks": 7,
            "capacity_per_truck": 5500,
            "status": "available",
            "location": "Alanya Depo"
        }
    ],
    "Adana": [
        {
            "company": "Çukurova Transport",
            "trucks": 9,
            "capacity_per_truck": 6000,
            "status": "available",
            "location": "Seyhan Depo"
        }
    ],
    "Konya": [
        {
            "company": "Anadolu Nakliyat",
            "trucks": 6,
            "capacity_per_truck": 5000,
            "status": "available",
            "location": "Organize Sanayi"
        }
    ],
    "Şanlıurfa": [
        {
            "company": "Güneydoğu Lojistik",
            "trucks": 5,
            "capacity_per_truck": 4500,
            "status": "available",
            "location": "Eyyübiye Depo"
        }
    ],
    "Gaziantep": [
        {
            "company": "Antep Nakliyat",
            "trucks": 8,
            "capacity_per_truck": 5500,
            "status": "available",
            "location": "Organize Sanayi"
        }
    ],
    "Diyarbakır": [
        {
            "company": "Dicle Transport",
            "trucks": 7,
            "capacity_per_truck": 5000,
            "status": "available",
            "location": "Sur Depo"
        }
    ],
    "Kocaeli": [
        {
            "company": "Marmara Lojistik",
            "trucks": 9,
            "capacity_per_truck": 6000,
            "status": "available",
            "location": "Gebze Liman"
        }
    ],
    "Mersin": [
        {
            "company": "Mersin Liman Taşımacılık",
            "trucks": 11,
            "capacity_per_truck": 7000,
            "status": "available",
            "location": "Liman Depo"
        }
    ],
    "Eskişehir": [
        {
            "company": "Porsuk Nakliyat",
            "trucks": 5,
            "capacity_per_truck": 5000,
            "status": "available",
            "location": "Organize Sanayi"
        }
    ],
    "Samsun": [
        {
            "company": "Karadeniz Lojistik",
            "trucks": 6,
            "capacity_per_truck": 5500,
            "status": "available",
            "location": "Liman Depo"
        }
    ],
    "Denizli": [
        {
            "company": "Pamukkale Transport",
            "trucks": 5,
            "capacity_per_truck": 5000,
            "status": "available",
            "location": "Organize Sanayi"
        }
    ],
    "Sakarya": [
        {
            "company": "Sakarya Nakliyat",
            "trucks": 7,
            "capacity_per_truck": 5500,
            "status": "available",
            "location": "Adapazarı Depo"
        }
    ],
    "Kayseri": [
        {
            "company": "Erciyes Transport",
            "trucks": 6,
            "capacity_per_truck": 5000,
            "status": "available",
            "location": "Organize Sanayi"
        }
    ],
    "Van": [
        {
            "company": "Van Gölü Lojistik",
            "trucks": 5,
            "capacity_per_truck": 4500,
            "status": "available",
            "location": "İpekyolu Depo"
        }
    ],
    "Malatya": [
        {
            "company": "Malatya Nakliyat",
            "trucks": 5,
            "capacity_per_truck": 5000,
            "status": "available",
            "location": "Battalgazi Depo"
        }
    ],
    "Mardin": [
        {
            "company": "Mardin Transport",
            "trucks": 4,
            "capacity_per_truck": 4500,
            "status": "available",
            "location": "Kızıltepe Depo"
        }
    ]
}

def get_available_trucks(city):
    """Şehirdeki mevcut tırları getirir"""
    return MOCK_TRUCKS.get(city, [])

def calculate_route(from_city, to_city):
    """Basit rota hesaplaması"""
    # Şehirler arası mesafeler (km)
    DISTANCES = {
        ('İstanbul', 'Ankara'): 450,
        ('İstanbul', 'İzmir'): 550,
        ('İstanbul', 'Bursa'): 230,
        ('İstanbul', 'Antalya'): 730,
        ('İstanbul', 'Adana'): 940,
        ('İstanbul', 'Konya'): 660,
        ('İstanbul', 'Kocaeli'): 100,
        ('İstanbul', 'Mersin'): 1000,
        ('İstanbul', 'Eskişehir'): 310,
        ('İstanbul', 'Samsun'): 700,
        ('İstanbul', 'Denizli'): 670,
        ('İstanbul', 'Sakarya'): 160,
        ('İstanbul', 'Kayseri'): 770,
        ('Ankara', 'İzmir'): 600,
        ('Ankara', 'Bursa'): 400,
        ('Ankara', 'Antalya'): 480,
        ('Ankara', 'Adana'): 500,
        ('Ankara', 'Konya'): 260,
        ('Ankara', 'Şanlıurfa'): 850,
        ('Ankara', 'Gaziantep'): 770,
        ('Ankara', 'Diyarbakır'): 970,
        ('Ankara', 'Mersin'): 560,
        ('Ankara', 'Eskişehir'): 235,
        ('Ankara', 'Samsun'): 500,
        ('Ankara', 'Denizli'): 480,
        ('Ankara', 'Kayseri'): 320,
        ('Ankara', 'Van'): 1350,
        ('Ankara', 'Malatya'): 680,
        ('İzmir', 'Bursa'): 380,
        ('İzmir', 'Antalya'): 480,
        ('İzmir', 'Adana'): 900,
        ('İzmir', 'Denizli'): 240,
        ('Adana', 'Gaziantep'): 220,
        ('Adana', 'Mersin'): 70,
        ('Adana', 'Diyarbakır'): 520,
        ('Gaziantep', 'Şanlıurfa'): 220,
        ('Gaziantep', 'Diyarbakır'): 390,
        ('Gaziantep', 'Malatya'): 350,
        ('Diyarbakır', 'Malatya'): 240,
        ('Diyarbakır', 'Van'): 450,
        ('Diyarbakır', 'Mardin'): 100,
        ('Şanlıurfa', 'Malatya'): 430,
        ('Şanlıurfa', 'Mardin'): 190,
        ('Samsun', 'Trabzon'): 150,
        ('Bursa', 'Kocaeli'): 175,
        ('Bursa', 'Eskişehir'): 220,
        ('Bursa', 'Sakarya'): 280,
        ('Kocaeli', 'Sakarya'): 60,
        ('Eskişehir', 'Konya'): 380,
        ('Eskişehir', 'Denizli'): 450
    }
    
    key = (from_city, to_city)
    reverse_key = (to_city, from_city)
    
    if key in DISTANCES:
        distance = DISTANCES[key]
    elif reverse_key in DISTANCES:
        distance = DISTANCES[reverse_key]
    else:
        distance = 500  # Default mesafe
    
    # Hız: 80 km/saat ortalama
    travel_time = distance / 80  # saat
    
    return {
        "distance": distance,
        "travel_time": travel_time,
        "estimated_arrival": f"{int(travel_time)} saat {int((travel_time % 1) * 60)} dakika"
    }

def dispatch_truck(from_city, to_city, product, amount):
    """Tır gönderimi simülasyonu"""
    route = calculate_route(from_city, to_city)
    trucks = get_available_trucks(from_city)
    
    if trucks:
        selected_truck = trucks[0]  # En uygun tırı seç
        
        return {
            "status": "dispatched",
            "company": selected_truck["company"],
            "from": from_city,
            "to": to_city,
            "product": product,
            "amount": amount,
            "route": route,
            "message": f"{selected_truck['company']} firması {from_city}'dan {to_city}'a {amount} adet {product} gönderiyor"
        }
    else:
        return {
            "status": "no_truck_available",
            "message": f"{from_city}'da uygun tır bulunamadı"
        }