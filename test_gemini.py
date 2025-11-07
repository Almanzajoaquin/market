# test_gemini.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'masivo_tech.settings')
django.setup()

import google.generativeai as genai
from masivo_tech import settings

print("🔧 Probando Gemini...")

if hasattr(settings, 'GEMINI_API_KEY') and settings.GEMINI_API_KEY:
    print(f"✅ API Key: {settings.GEMINI_API_KEY[:20]}...")
    
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Di 'Hola Masivo Tech'")
        print(f"✅ Gemini funciona: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
else:
    print("❌ GEMINI_API_KEY no configurada")