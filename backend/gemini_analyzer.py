import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# .env dosyasından API anahtarını yükle
load_dotenv()

# API anahtarını al
api_key = os.getenv("GEMINI_API_KEY")

# Gemini'yi konfigüre et
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-1.5-flash')

def analyze_help_text(user_text):
    """
    Kullanıcının girdiği metni analiz eder ve JSON formatında döndürür.
    
    Args:
        user_text (str): Kullanıcının girdiği metin
    
    Returns:
        dict: Analiz sonucu JSON formatında
    """
    
    # Gemini'ya gönderilecek prompt
    prompt = f"""
    Aşağıdaki metni analiz et ve SADECE JSON formatında cevap ver. Başka hiçbir açıklama veya metin yazma.

    Metin: "{user_text}"

    İstenilen JSON formatı:
    {{
        "ihtiyac_var": true/false,
        "konum": "şehir/ilçe",
        "urunler": [
            {{
                "urun_adi": "ürün adı",
                "miktar": 0,
                "birim": "adet/paket/şişe"
            }}
        ],
        "öncelik": "düşük/orta/yüksek/acil"
    }}

    JSON:
    """
    
    try:
        response = model.generate_content(prompt)
        
        # Ham yanıtı kontrol et
        cleaned_text = response.text.strip()
        
        # Eğer yanıt ```json ile başlıyorsa temizle
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        elif cleaned_text.startswith("```"):
            cleaned_text = cleaned_text[3:]
        
        # Eğer ``` ile bitiyorsa temizle
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
        
        cleaned_text = cleaned_text.strip()
        
        # JSON'ı parse et
        response_json = json.loads(cleaned_text)
        return response_json
    except Exception as e:
        return {"error": str(e)}