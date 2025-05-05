# mock_market.py

MOCK_MARKETS = {
    "İstanbul": [
        {
            "name": "Mega Market İstanbul",
            "location": "Beşiktaş",
            "distance": 5,  # km
            "capacity": 1000,  # kişi başına yeterli malzeme
            "products": {
                "Su": 5000,
                "Battaniye": 1000,
                "Çadır": 200,
                "Konserve": 3000,
                "İlk yardım": 500
            }
        },
        {
            "name": "Süper Market Anadolu",
            "location": "Kadıköy",
            "distance": 8,
            "capacity": 800,
            "products": {
                "Su": 3000,
                "Battaniye": 500,
                "Çadır": 100,
                "Konserve": 2000,
                "İlk yardım": 300
            }
        }
    ],
    "Ankara": [
        {
            "name": "Capital Market",
            "location": "Çankaya",
            "distance": 3,
            "capacity": 600,
            "products": {
                "Su": 2000,
                "Battaniye": 300,
                "Çadır": 80,
                "Konserve": 1500,
                "İlk yardım": 200
            }
        }
    ],
    "İzmir": [
        {
            "name": "Ege Market",
            "location": "Karşıyaka",
            "distance": 4,
            "capacity": 700,
            "products": {
                "Su": 3500,
                "Battaniye": 600,
                "Çadır": 150,
                "Konserve": 2500,
                "İlk yardım": 400
            }
        }
    ]
}

# Daha az stoku olan marketler (dinamik envanter simülasyonu için)
MARKET_STOCK_VARIATIONS = {
    "İstanbul": {
        "Mega Market İstanbul": 0.8,  # %80 stok dolu
        "Süper Market Anadolu": 0.4   # %40 stok dolu
    },
    "Ankara": {
        "Capital Market": 0.6
    },
    "İzmir": {
        "Ege Market": 0.7
    }
}

def get_available_markets(city):
    """Şehirdeki mevcut marketleri getirir"""
    if city in MOCK_MARKETS:
        markets = []
        for market in MOCK_MARKETS[city]:
            # Mevcut stok miktarını hesapla
            stock_multiplier = MARKET_STOCK_VARIATIONS[city].get(market["name"], 1.0)
            available_market = market.copy()
            available_market["products"] = {
                k: int(v * stock_multiplier) 
                for k, v in market["products"].items()
            }
            markets.append(available_market)
        return markets
    return []

def get_product_availability(city, product_name):
    """Belirli bir ürünün şehirdeki toplam stok durumunu gösterir"""
    total_stock = 0
    markets = get_available_markets(city)
    for market in markets:
        if product_name in market["products"]:
            total_stock += market["products"][product_name]
    return total_stock