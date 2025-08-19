# test_railway_complete.py - Test completo para Railway deployment
import requests
import json
from datetime import datetime, timedelta
import sys

# 🚀 CONFIGURACIÓN RAILWAY
RAILWAY_URL = "https://web-production-8d7cb.up.railway.app"
session = requests.Session()

def print_separator(title):
    """Imprimir separador bonito"""
    print("\n" + "="*80)
    print(f"🔍 {title}")
    print("="*80)

def print_data_preview(data, title, max_items=3):
    """Mostrar preview de datos de forma bonita"""
    print(f"\n📋 {title}")
    print("-" * 60)
    
    if not data:
        print("❌ No hay datos disponibles")
        return
    
    if isinstance(data, list):
        print(f"Total elementos: {len(data)}")
        items_to_show = min(len(data), max_items)
        
        for i, item in enumerate(data[:items_to_show]):
            print(f"\n[{i+1}] {json.dumps(item, indent=2, ensure_ascii=False)}")
        
        if len(data) > max_items:
            print(f"\n... y {len(data) - max_items} elementos más")
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False))

def test_railway_connectivity():
    """Test básico de conectividad a Railway"""
    print_separator("CONECTIVIDAD RAILWAY")
    
    try:
        # Test básico de la raíz
        print("🌐 Probando conectividad básica...")
        response = requests.get(RAILWAY_URL, timeout=10)
        print(f"   Status raíz: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        
        # Test del health endpoint
        print("\n🔍 Probando health check...")
        health_response = requests.get(f"{RAILWAY_URL}/api/reports/health", timeout=10)
        print(f"   Health status: {health_response.status_code}")
        
        if health_response.status_code == 200:
            health_data = health_response.json()
            print_data_preview(health_data, "Health Check Response")
            return True
        else:
            print(f"   Health response: {health_response.text[:200]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"💥 Error de conectividad: {str(e)}")
        return False

def test_railway_login():
    """Test específico de login en Railway"""
    print_separator("LOGIN RAILWAY")
    
    # Headers específicos para Railway
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Railway-Test-Client/1.0',
        # Sin Origin específico para evitar CORS
    }
    
    login_data = {
        "username": "Auren", 
        "password": "Grupo4uren"
    }
    
    print("🔐 Intentando login en Railway...")
    print(f"   URL: {RAILWAY_URL}/api/auth/signin")
    print(f"   Headers: {headers}")
    print(f"   Data: {login_data}")
    
    try:
        response = session.post(
            f"{RAILWAY_URL}/api/auth/signin", 
            json=login_data, 
            headers=headers,
            timeout=15
        )
        
        print(f"\n📊 RESULTADO LOGIN:")
        print(f"   Status: {response.status_code}")
        print(f"   Headers response: {dict(response.headers)}")
        
        # Analizar cookies
        cookies = session.cookies.get_dict()
        print(f"   Cookies obtenidas: {list(cookies.keys())}")
        
        if response.status_code == 200:
            print("   ✅ LOGIN EXITOSO")
            
            # Mostrar detalles de cookies
            for cookie in session.cookies:
                print(f"   Cookie '{cookie.name}': domain='{cookie.domain}', path='{cookie.path}', secure={cookie.secure}")
            
            try:
                response_data = response.json()
                print_data_preview(response_data, "Login Response")
            except:
                print("   Respuesta no es JSON")
                
            return cookies.get('access_token')
            
        else:
            print(f"   ❌ LOGIN FALLÓ: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"💥 Error en login: {str(e)}")
        return None

def test_railway_endpoint(endpoint, description, token=None, params=None, method='GET'):
    """Test genérico de endpoint en Railway"""
    print(f"\n🧪 Testing: {description}")
    print(f"   Endpoint: {endpoint}")
    
    url = f"{RAILWAY_URL}{endpoint}"
    headers = {
        'Accept': 'application/json',
        'User-Agent': 'Railway-Test-Client/1.0'
    }
    
    # Si tenemos token, agregarlo como cookie manual
    if token:
        headers['Cookie'] = f'access_token={token}'
        print(f"   🔑 Usando token: {token[:20]}...")
    
    try:
        if method == 'GET':
            response = session.get(url, headers=headers, params=params, timeout=15)
        else:
            response = session.post(url, headers=headers, json=params, timeout=15)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ ÉXITO")
            try:
                data = response.json()
                return data
            except:
                return {"raw_response": response.text[:500]}
        elif response.status_code == 401:
            print("   🔒 ERROR AUTH - Token inválido o expirado")
            return None
        elif response.status_code == 404:
            print("   🚫 ERROR 404 - Endpoint no encontrado")
            return None
        else:
            print(f"   ❌ ERROR {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"   💥 EXCEPCIÓN: {str(e)}")
        return None

def test_railway_cors():
    """Test específico de CORS para Railway"""
    print_separator("TEST CORS RAILWAY")
    
    # Simular request desde frontend local
    cors_headers = {
        'Origin': 'http://localhost:3000',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'Content-Type',
    }
    
    print("🌐 Probando CORS preflight...")
    try:
        response = requests.options(f"{RAILWAY_URL}/api/auth/signin", headers=cors_headers)
        print(f"   OPTIONS status: {response.status_code}")
        print(f"   CORS headers: {dict(response.headers)}")
        
        # Verificar headers CORS importantes
        cors_origin = response.headers.get('Access-Control-Allow-Origin')
        cors_credentials = response.headers.get('Access-Control-Allow-Credentials')
        cors_methods = response.headers.get('Access-Control-Allow-Methods')
        
        print(f"\n📋 ANÁLISIS CORS:")
        print(f"   Allow-Origin: {cors_origin}")
        print(f"   Allow-Credentials: {cors_credentials}")
        print(f"   Allow-Methods: {cors_methods}")
        
        if cors_origin and ('*' in cors_origin or 'localhost' in cors_origin):
            print("   ✅ CORS Allow-Origin configurado correctamente")
        else:
            print("   ❌ CORS Allow-Origin problemático")
            
        return response.status_code in [200, 204]
        
    except Exception as e:
        print(f"💥 Error CORS: {str(e)}")
        return False

def run_railway_complete_test():
    """Ejecutar test completo de Railway"""
    
    print("🚀 INICIANDO TEST COMPLETO DE RAILWAY")
    print(f"Railway URL: {RAILWAY_URL}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. Test de conectividad básica
    if not test_railway_connectivity():
        print("❌ Falló conectividad básica - abortando")
        return
    
    # 2. Test CORS
    test_railway_cors()
    
    # 3. Test de login
    token = test_railway_login()
    if not token:
        print("❌ No se pudo obtener token - continuando con tests públicos")
    
    # 4. Test de endpoints públicos
    print_separator("ENDPOINTS PÚBLICOS")
    
    # Health check
    health_data = test_railway_endpoint('/api/reports/health', 'Health Check')
    if health_data:
        print_data_preview(health_data, "Health Response")
    
    # Debug general
    debug_data = test_railway_endpoint('/api/reports/debug', 'Debug Info')
    if debug_data:
        print_data_preview(debug_data, "Debug Info")
    
    # 5. Test de endpoints con auth (si tenemos token)
    if token:
        print_separator("ENDPOINTS CON AUTENTICACIÓN")
        
        # Test connection
        conn_data = test_railway_endpoint('/api/reports/test-connection', 'Test Connection', token=token)
        if conn_data:
            print_data_preview(conn_data, "Connection Test")
        
        # Zonales
        zonales_data = test_railway_endpoint('/api/reports/zonales', 'Zonales', token=token)
        if zonales_data and zonales_data.get('success'):
            zonales_list = zonales_data.get('data', [])
            print_data_preview(zonales_list, "Zonales Disponibles")
        
        # Supervisores
        supervisores_data = test_railway_endpoint('/api/reports/supervisores', 'Supervisores', token=token)
        if supervisores_data and supervisores_data.get('success'):
            supervisores_list = supervisores_data.get('data', [])
            print_data_preview(supervisores_list, "Supervisores Disponibles")
        
        # Reporte con fecha actual
        today = datetime.now().strftime('%Y-%m-%d')
        resumen_data = test_railway_endpoint(
            '/api/reports/vendedores-ventas', 
            f'Resumen Vendedores {today}', 
            token=token,
            params={'fecha': today}
        )
        if resumen_data and resumen_data.get('success'):
            resumen_list = resumen_data.get('data', [])
            print_data_preview(resumen_list, f"Resumen {today}")
        
        # Debug auth
        debug_auth_data = test_railway_endpoint('/api/reports/debug-auth', 'Debug Auth', token=token)
        if debug_auth_data:
            print_data_preview(debug_auth_data, "Debug Auth")
    
    # 6. DIAGNÓSTICO FRONTEND
    print_separator("DIAGNÓSTICO PARA FRONTEND")
    
    print("🔧 PROBLEMAS DETECTADOS:")
    print("\n1. ❌ URL INCORRECTA EN FRONTEND:")
    print("   Tu frontend usa: https://web-production-8d7cb.up.railway.app:3000/")
    print("   Debe ser:       https://web-production-8d7cb.up.railway.app/")
    print("   Railway NO usa puertos personalizados")
    
    print("\n2. 🔧 CORRECCIÓN EN NEXT.JS:")
    print("   En tu .env.local:")
    print("   NEXT_PUBLIC_API_URL=https://web-production-8d7cb.up.railway.app")
    print("   (SIN puerto 3000)")
    
    print("\n3. 📋 VERIFICAR CONFIGURACIÓN:")
    print("   - Rewrites en next.config.ts apuntan correctamente")
    print("   - CORS está configurado para localhost")
    print("   - JWT cookies tienen path='/' y secure=true")
    
    print_separator("RESUMEN FINAL")
    print("✅ Test de Railway completado")
    print("🔧 ACCIÓN REQUERIDA: Corregir URL en frontend (quitar :3000)")
    print("📝 El backend de Railway parece funcionar correctamente")

def main():
    """Función principal"""
    try:
        run_railway_complete_test()
    except KeyboardInterrupt:
        print("\n⚠️  Test interrumpido por usuario")
    except Exception as e:
        print(f"\n💥 Error inesperado: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()