# list_models.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'masivo_tech.settings')
django.setup()

import google.generativeai as genai
from masivo_tech import settings

print("🔍 Listando modelos disponibles...")
print("=" * 50)

try:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    
    # Listar todos los modelos
    models = genai.list_models()
    
    print("📋 MODELOS DISPONIBLES PARA generateContent:")
    print("-" * 40)
    
    available_models = []
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            available_models.append(model.name)
            print(f"✅ {model.name}")
            print(f"   - {model.description}")
            print()
    
    if available_models:
        print(f"🎯 Modelos disponibles: {', '.join(available_models)}")
    else:
        print("❌ No hay modelos disponibles para generateContent")
            
except Exception as e:
    print(f"❌ Error: {e}")