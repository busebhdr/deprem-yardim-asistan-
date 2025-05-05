from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # Ekle
from pydantic import BaseModel
from gemini_analyzer import analyze_help_text
import uvicorn
from typing import List, Optional
import os
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from mock_market import get_available_markets, get_product_availability
from mock_trucks import get_available_trucks, dispatch_truck
from gemini_analyzer import model
# .env dosyasını yükle
load_dotenv()

app = FastAPI(title="Deprem Yardım Asistanı API")

# CORS middleware ekle
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB bağlantısı
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "deprem_yardim")

# MongoDB client
mongodb_client = AsyncIOMotorClient(MONGODB_URL)
db = mongodb_client[DATABASE_NAME]

# Database collections
entries_collection = db.entries
markets_collection = db.markets
trucks_collection = db.trucks

# Request modelleri
class AnalyzeRequest(BaseModel):
    text: str

class EntryRequest(BaseModel):
    text: str
    name: Optional[str] = None

class MatchRequest(BaseModel):
    konum: str
    urun_adi: str
    miktar: int

# Response modelleri
class AnalyzeResponse(BaseModel):
    ihtiyac_var: bool
    konum: str
    urunler: list
    öncelik: str

@app.on_event("startup")
async def startup_event():
    # MongoDB'de index'leri oluştur
    await entries_collection.create_index("konum")
    await entries_collection.create_index("status")

@app.on_event("shutdown")
async def shutdown_event():
    mongodb_client.close()

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_endpoint(request: AnalyzeRequest):
    """
    Kullanıcının girdiği metni analiz eder
    """
    try:
        result = analyze_help_text(request.text)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/submit-entry")
async def submit_entry(request: EntryRequest):
    """
    Kullanıcının yardım kaydını veritabanına ekler
    """
    try:
        # Metni analiz et
        analysis = analyze_help_text(request.text)
        if "error" in analysis:
            raise HTTPException(status_code=500, detail=analysis["error"])
        
        # Veritabanına ekle
        entry = {
            "name": request.name,
            "original_text": request.text,
            "analysis": analysis,
            "timestamp": datetime.now(),
            "status": "aktif"
        }
        
        result = await entries_collection.insert_one(entry)
        entry_id = str(result.inserted_id)
        
        return {"message": "Kayıt başarıyla eklendi", "id": entry_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/entries")
async def get_entries():
    """
    Tüm kayıtları listeler
    """
    try:
        entries = []
        async for entry in entries_collection.find():
            entry["_id"] = str(entry["_id"])  # ObjectId'yi string'e çevir
            entries.append(entry)
        return {"entries": entries}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/match")
async def match_entries(request: MatchRequest):
    """
    Belirli konumda belirli ürünü arayan veya verebilecek kayıtları bulur
    """
    try:
        # Aynı şehirde arama yap
        query = {
            "analysis.konum": request.konum,
            "status": "aktif"
        }
        
        # İhtiyacını verebilecek (arz) kayıtları bul
        supply_entries = []
        demand_entries = []
        
        async for entry in entries_collection.find(query):
            entry["_id"] = str(entry["_id"])
            
            # Ürün kontrolü
            for urun in entry["analysis"]["urunler"]:
                if urun["urun_adi"].lower() == request.urun_adi.lower():
                    if entry["analysis"]["ihtiyac_var"] == False:  # Arz
                        supply_entries.append({
                            "id": entry["_id"],
                            "name": entry["name"],
                            "miktar": urun["miktar"],
                            "öncelik": entry["analysis"]["öncelik"],
                            "timestamp": entry["timestamp"]
                        })
                    else:  # Talep
                        demand_entries.append({
                            "id": entry["_id"],
                            "name": entry["name"],
                            "miktar": urun["miktar"],
                            "öncelik": entry["analysis"]["öncelik"],
                            "timestamp": entry["timestamp"]
                        })
        
        return {
            "konum": request.konum,
            "urun": request.urun_adi,
            "arz": supply_entries,
            "talep": demand_entries,
            "summary": {
                "toplam_arz": sum(e["miktar"] for e in supply_entries),
                "toplam_talep": sum(e["miktar"] for e in demand_entries)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/simulate-earthquake")
async def simulate_earthquake(konum: str):
    """Deprem simülasyonu - tüm yardım kaynakları harekete geçirilir"""
    try:
        # 1. Etkilenen bölgedeki tüm kayıtları bul
        query = {
            "analysis.konum": konum,
            "status": "aktif"
        }
        
        # Mevcut kaynakları topla
        total_resources = {}
        urgent_needs = []
        
        async for entry in entries_collection.find(query):
            entry["_id"] = str(entry["_id"])
            
            # Kaynakları topla
            for urun in entry["analysis"]["urunler"]:
                if not entry["analysis"]["ihtiyac_var"]:  # Arz
                    if urun["urun_adi"] not in total_resources:
                        total_resources[urun["urun_adi"]] = 0
                    total_resources[urun["urun_adi"]] += urun["miktar"]
                else:  # Acil ihtiyaçları tespit et
                    if entry["analysis"]["öncelik"] in ["acil", "yüksek"]:
                        urgent_needs.append({
                            "id": entry["_id"],
                            "name": entry["name"],
                            "urun": urun["urun_adi"],
                            "miktar": urun["miktar"],
                            "öncelik": entry["analysis"]["öncelik"]
                        })
        
        # 2. Tüm kayıtları "deprem modu"na al
        await entries_collection.update_many(
            {"analysis.konum": konum},
            {"$set": {"status": "deprem_modu", "earthquake_activated": datetime.now()}}
        )
        
        # 3. Market ihtiyaçlarını analiz et (mock)
        missing_items = []
        if len(urgent_needs) > 0:
            missing_items = ["ilaç", "bebek maması", "su"]  # Mock veri
            
        # Market ve tır durumunu ekleyin
        nearby_cities = ["İstanbul", "Ankara", "İzmir", "Bursa", "Samsun", "Adana", "Konya", "Antalya", "Kocaeli", "Mersin"]
        logistics_support = []
        market_support = []
        
        # En yakın 3 şehirden yardım talep et
        for city in nearby_cities[:3]:
            if city != konum:
                trucks = get_available_trucks(city)
                if trucks:
                    # Eksik stoklar için tır gönder
                    if len(urgent_needs) > 0:
                        first_need = urgent_needs[0]
                        dispatch = dispatch_truck(city, konum, first_need["urun"], first_need["miktar"])
                        logistics_support.append(dispatch)
                        
                # Market durumunu kontrol et
                markets = get_available_markets(city)
                if markets:
                    market_support.append({
                        "city": city,
                        "markets": len(markets),
                        "capacity": sum(m["capacity"] for m in markets)
                    })
        
        return {
            "message": "Deprem simülasyonu başlatıldı",
            "konum": konum,
            "timestamp": datetime.now().isoformat(),
            "available_resources": total_resources,
            "urgent_needs": urgent_needs,
            "logistics_support": logistics_support,
            "market_support": market_support,
            "status_updates": [
                f"{konum} bölgesinde tüm yardım kaynakları harekete geçirildi",
                f"{len(urgent_needs)} acil yardım talebi tespit edildi",
                f"Toplam {sum(total_resources.values()) if total_resources else 0} adet yardım malzemesi mevcut",
                "Gerekli malzemeler için yakın marketlerle iletişime geçiliyor..." if missing_items else "Tüm ihtiyaçlar mevcut kaynaklar ile karşılanabilir",
                f"{len(logistics_support)} şehirden tır desteği yola çıktı" if logistics_support else "Lojistik desteğe ihtiyaç duyulmadı"
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stock-summary")
async def get_stock_summary():
    """Şehir bazlı stok özeti"""
    try:
        stock_data = {}
        
        async for entry in entries_collection.find():
            city = entry.get("analysis", {}).get("konum", "Bilinmiyor")
            
            if city not in stock_data:
                stock_data[city] = {
                    "supplies": {},
                    "trucks": 0,
                    "entries": []
                }
            
            # Malzemeleri topla
            products = entry.get("analysis", {}).get("urunler", [])
            for product in products:
                product_name = product.get("urun_adi")
                product_quantity = product.get("miktar", 0)
                
                if product_name in stock_data[city]["supplies"]:
                    stock_data[city]["supplies"][product_name] += product_quantity
                else:
                    stock_data[city]["supplies"][product_name] = product_quantity
            
            # Tır sayısını kontrol et
            original_text = entry.get("original_text", "")
            if "tır" in original_text:
                import re
                match = re.search(r'(\d+)\s*tır', original_text)
                if match:
                    stock_data[city]["trucks"] += int(match.group(1))
            
            stock_data[city]["entries"].append({
                "name": entry.get("name", "Anonim"),
                "text": original_text,
                "timestamp": entry.get("timestamp", "")
            })
        
        return {"stock_summary": stock_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/market-status/{city}")
async def get_market_status(city: str):
    """Şehirdeki marketlerin durumunu gösterir"""
    try:
        markets = get_available_markets(city)
        return {
            "city": city,
            "markets": markets,
            "total_capacity": sum(m["capacity"] for m in markets)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/truck-status/{city}")
async def get_truck_status(city: str):
    """Şehirdeki tırların durumunu gösterir"""
    try:
        trucks = get_available_trucks(city)
        return {
            "city": city,
            "trucks": trucks,
            "total_capacity": sum(t["trucks"] * t["capacity_per_truck"] for t in trucks)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/dispatch-help")
async def dispatch_help(from_city: str, to_city: str, product: str, amount: int):
    """Yardım malzemesi gönderimini simüle eder"""
    try:
        # Önce marketten var mı kontrol et
        market_stock = get_product_availability(from_city, product)
        
        if market_stock < amount:
            return {
                "status": "insufficient_stock",
                "message": f"{from_city}'da yeterli {product} yok. Mevcut: {market_stock}, Gerekli: {amount}"
            }
        
        # Tır gönderimi
        dispatch_result = dispatch_truck(from_city, to_city, product, amount)
        
        return dispatch_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ai-smart-matching")
@app.post("/ai-smart-matching")
async def ai_smart_matching(konum: str, urun_adi: str):
    """AI ile akıllı eşleştirme sistemi"""
    try:
        # Yakındaki şehirleri bulun
        nearby_cities = get_nearby_cities(konum)
        
        # AI prompt oluştur
        prompt = f"""
        {konum} şehrinde {urun_adi} ihtiyacı var. 
        En yakın şehirlerden birini seç: {', '.join(nearby_cities)}
        
        JSON formatında döndür:
        {{
            "recommended_city": "{nearby_cities[0]}",
            "reason": "Yakın mesafede ve yeterli stok var",
            "distance": "50",
            "available_amount": "10"
        }}
        """
        
        # AI'dan öneri al
        response = model.generate_content(prompt)
        
        # JSON'ı daha güvenilir bir şekilde çıkar
        import json
        import re
        
        # AI yanıtından JSON'u çıkar
        text = response.text
        json_pattern = r'\{[^}]+\}'
        json_match = re.search(json_pattern, text)
        
        if json_match:
            ai_result = json.loads(json_match.group())
        else:
            # Fallback: AI JSON döndüremediyse sabit veri
            ai_result = {
                "recommended_city": nearby_cities[0],
                "reason": "En yakın şehir",
                "distance": "100",
                "available_amount": "5"
            }
        
        return {
            "ai_recommendation": ai_result,
            "nearby_options": nearby_cities
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_nearby_cities(city):
    """Yakındaki şehirleri döndürür"""
    distance_matrix = {
        "İstanbul": ["Kocaeli", "Bursa", "Sakarya"],
        "Ankara": ["Konya", "Eskişehir", "Kayseri"],
        "İzmir": ["Denizli", "Manisa", "Aydın"],
        "Trabzon": ["Samsun", "Giresun", "Ordu"],
        "Bursa": ["İstanbul", "Kocaeli", "Eskişehir"],
        "Adana": ["Mersin", "Gaziantep", "Osmaniye"]
    }
    
    return distance_matrix.get(city, ["İstanbul", "Ankara", "İzmir"])
@app.get("/active-routes")
async def get_active_routes():
    """Aktif tır rotalarını döndürür"""
    try:
        # Mock route data
        active_routes = [
            {
                "from": "Ankara",
                "to": "İstanbul",
                "product": "Battaniye",
                "amount": 50,
                "status": "yolda",
                "progress": 65
            },
            {
                "from": "İzmir",
                "to": "Bursa",
                "product": "Su",
                "amount": 100,
                "status": "hazırlanıyor",
                "progress": 10
            }
        ]
        return {"routes": active_routes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/get-notifications")
async def get_notifications(konum: str):
    """Deprem bölgesindeki bildirimleri döndürür"""
    try:
        # Gerçek bildirimleri simüle et
        notifications = []
        async for entry in entries_collection.find({"status": "deprem_modu"}):
            if entry.get("analysis", {}).get("konum") != konum:
                notifications.append({
                    "to": entry.get("name", "Anonim"),
                    "city": entry.get("analysis", {}).get("konum", "Bilinmiyor"),
                    "message": f"ACİL! {konum} deprem bölgesine yardım için malzemelerinizi en yakın toplama merkezine ulaştırın."
                })
        
        return {"notifications": notifications[:10]}  # İlk 10 bildirimi göster
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/ai-risk-analysis")
async def ai_risk_analysis():
    """AI ile bölgesel risk analizi"""
    try:
        # AI ile tüm şehirlerin durumunu analiz et
        prompt = """
        Türkiye'deki şehirlerin deprem riski ve yardım kaynaklarını analiz et.
        
        JSON formatında döndür:
        {{
            "high_risk": ["liste şehirler"],
            "low_supply": ["stok eksikliği olan şehirler"],
            "recommendation": "öneri metni"
        }}
        """
        
        response = model.generate_content(prompt)
        
        import json
        import re
        
        # AI yanıtından JSON'u çıkar
        text = response.text
        json_pattern = r'\{[^}]+\}'
        json_match = re.search(json_pattern, text, re.DOTALL)
        
        if json_match:
            ai_result = json.loads(json_match.group())
        else:
            # Fallback
            ai_result = {
                "high_risk": ["İstanbul", "İzmir", "Bursa"],
                "low_supply": ["Trabzon", "Samsun"],
                "recommendation": "Bu şehirlerde stok artırımı öneriliyor"
            }
        
        return {
            "ai_analysis": ai_result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/")
async def root():
    return {"message": "Deprem Yardım Asistanı API v1.0"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)