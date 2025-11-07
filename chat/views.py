import google.generativeai as genai
import json
import uuid
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# Configurar logging
logger = logging.getLogger(__name__)

# Configurar Gemini con el modelo CORRECTO
def setup_gemini():
    try:
        if hasattr(settings, 'GEMINI_API_KEY') and settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            
            # USAR EL MODELO CORRECTO de tu lista
            model_name = 'models/gemini-2.0-flash-001'  # ← MODELO ESTABLE Y RÁPIDO
            
            try:
                model = genai.GenerativeModel(model_name)
                # Probar el modelo
                test_response = model.generate_content("Hola")
                if test_response.text:
                    logger.info(f"✅ Gemini configurado con: {model_name}")
                    return model
            except Exception as e:
                logger.error(f"❌ Error con {model_name}: {e}")
                
                # Fallback a otros modelos
                fallback_models = [
                    'models/gemini-2.5-flash',
                    'models/gemini-flash-latest', 
                    'models/gemini-pro-latest'
                ]
                
                for fallback_model in fallback_models:
                    try:
                        model = genai.GenerativeModel(fallback_model)
                        test_response = model.generate_content("Hola")
                        if test_response.text:
                            logger.info(f"✅ Gemini configurado con fallback: {fallback_model}")
                            return model
                    except:
                        continue
            
            logger.error("❌ Ningún modelo de Gemini funcionó")
            return None
            
        else:
            logger.warning("⚠️  GEMINI_API_KEY no configurada")
            return None
            
    except Exception as e:
        logger.error(f"❌ Error configurando Gemini: {e}")
        return None

# Configurar al iniciar
gemini_model = setup_gemini()

def chat_view(request):
    session_id = request.session.get('chat_session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
        request.session['chat_session_id'] = session_id
    
    return render(request, 'chat/chat.html', {
        'session_id': session_id,
        'gemini_available': gemini_model is not None
    })

@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            session_id = data.get('session_id')
            
            logger.info(f"📨 Mensaje del usuario: {user_message}")
            
            if not user_message:
                return JsonResponse({'response': '¡Hola! ¿En qué puedo ayudarte? 😊'})
            
            # USAR GEMINI CON EL MODELO CORRECTO
            if gemini_model:
                try:
                    # Prompt optimizado para Masivo Tech
                    prompt = f"""Eres Masibot, el asistente virtual oficial de Masivo Tech.

INFORMACIÓN REAL:
- Tienda: Masivo Tech - Periféricos gaming
- Productos: teclados mecánicos, mouses gaming, auriculares, monitores, sillas gamer
- Marcas: Logitech, Razer, Redragon, HyperX, SteelSeries
- Envíos: CABA 24-48hs, Interior 3-5 días hábiles
- Pagos: tarjetas (hasta 12 cuotas), transferencia (10% descuento), efectivo
- Garantía: 6-12 meses oficial
- Contacto: WhatsApp +54 11 1234-5678, info@masivotech.com
- Horario: Lunes a Viernes 9-18hs

RESPONDE:
- En español argentino coloquial y amigable
- Usa emojis relevantes 🎮🖱️⌨️🎧🚚💳
- Sé entusiasta sobre gaming
- Responde específicamente a la consulta
- NO inventes precios exactos
- NO inventes stocks exactos
- Mantén respuestas breves (máximo 2 párrafos)

Consulta: {user_message}

Respuesta:"""
                    
                    response = gemini_model.generate_content(prompt)
                    bot_response = response.text.strip()
                    
                    logger.info(f"🤖 Gemini 2.0 Flash respondió: {bot_response}")
                    
                    return JsonResponse({
                        'response': bot_response,
                        'session_id': session_id,
                        'source': 'gemini_2.0_flash'
                    })
                    
                except Exception as e:
                    logger.error(f"❌ Error con Gemini: {e}")
                    # Continuar con fallback
            
            # FALLBACK INTELIGENTE
            return handle_fallback_response(user_message)
                
        except Exception as e:
            logger.error(f"❌ Error general: {e}")
            return JsonResponse({
                'response': '¡Hola! 😊 Soy Masibot. ¿En qué puedo ayudarte? 🎮'
            })
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def handle_fallback_response(user_message):
    """Sistema de respuestas predefinidas"""
    user_lower = user_message.lower()
    
    responses = {
        'hola': "¡Hola! 😊 Soy Masibot de Masivo Tech. ¿Buscás algún periférico gaming? 🎮",
        'mouse': "🖱️ Tenemos mouses gaming Logitech, Razer, Redragon. ¿Inalámbricos o con cable?",
        'teclado': "🎹 Teclados mecánicos con switches azul, rojo o marrón. Marcas: Redragon, Logitech, Razer",
        'auricular': "🎧 Auriculares gaming con sonido surround 7.1. HyperX, Logitech, Razer",
        'monitor': "🖥️ Monitores gaming 144Hz, 240Hz. Samsung, LG, ASUS. ¿Qué tamaño?",
        'silla': "💺 Sillas gamer ergonómicas con soporte lumbar ajustable",
        'logitech': "🎮 Logitech G! Pro X Superlight, G502 Hero, G203 Lightsync. ¿Cuál modelo?",
        'razer': "🐍 Razer! DeathAdder, Viper, BlackWidow. Calidad premium",
        'redragon': "🐲 Redragon! Kumara, Griffin, Lamia. Excelente calidad-precio",
        'envío': "🚚 ¡Envíos a todo el país! CABA: 24-48hs | Interior: 3-5 días | Gratis +$50.000",
        'envios': "🚚 ¡Envíos a todo el país! CABA: 24-48hs | Interior: 3-5 días | Gratis +$50.000",
        'pago': "💳 Tarjetas (12 cuotas SIN interés), transferencia (10% OFF), efectivo",
        'cuota': "💰 ¡12 cuotas SIN interés! Transferencia con 10% de descuento",
        'garantía': "✅ Garantía oficial 6-12 meses. Distribuidores autorizados",
        'garantia': "✅ Garantía oficial 6-12 meses. Distribuidores autorizados",
        'stock': "📦 Todos los productos publicados están disponibles. Stock en tiempo real!",
        'contacto': "📞 WhatsApp: +54 11 1234-5678 | Email: info@masivotech.com | Lun-Vie 9-18hs",
        'whatsapp': "💬 WhatsApp: +54 11 1234-5678 - Respondemos al instante!",
        'gracias': "¡De nada! 😊 ¿Necesitás algo más?",
    }
    
    for keyword, answer in responses.items():
        if keyword in user_lower:
            return JsonResponse({'response': answer, 'source': 'fallback'})
    
    import random
    contextual = [
        f"😊 ¿Sobre '{user_message}'? ¡Contame más! ¿Qué te interesa? 🎮",
        f"🎯 ¿'{user_message}'? Preguntame sobre productos gaming, envíos o garantías!",
        f"🖥️ ¿Necesitás info sobre '{user_message}'? Soy experto en periféricos!",
    ]
    
    return JsonResponse({
        'response': random.choice(contextual),
        'source': 'fallback_contextual'
    })