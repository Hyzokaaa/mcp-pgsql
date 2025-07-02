# examples/api_client.py

import requests
import json

def test_api():
    """Ejemplo de cómo usar la API"""
    
    # URL de la API (ajustar según tu configuración)
    base_url = "http://localhost:8000"
    
    # Test 1: Health check
    print("=== Test Health Check ===")
    health_response = requests.get(f"{base_url}/api/v1/health")
    print(f"Status: {health_response.status_code}")
    print(f"Response: {health_response.json()}")
    print()
    
    # Test 2: Chat simple
    print("=== Test Chat Simple ===")
    chat_data = {
        "messages": [
            {
                "role": "user",
                "content": "¿Qué tablas hay en la base de datos?"
            }
        ]
    }
    
    chat_response = requests.post(
        f"{base_url}/api/v1/chat",
        headers={"Content-Type": "application/json"},
        json=chat_data
    )
    
    print(f"Status: {chat_response.status_code}")
    if chat_response.status_code == 200:
        response_data = chat_response.json()
        print(f"Response: {response_data['response']}")
    else:
        print(f"Error: {chat_response.text}")
    print()
    
    # Test 3: Chat con historial
    print("=== Test Chat con Historial ===")
    chat_with_history = {
        "messages": [
            {
                "role": "user",
                "content": "Lista las tablas"
            },
            {
                "role": "assistant",
                "content": "Las tablas disponibles son: users, orders, products"
            },
            {
                "role": "user",
                "content": "Describe la tabla users"
            }
        ]
    }
    
    chat_response = requests.post(
        f"{base_url}/api/v1/chat",
        headers={"Content-Type": "application/json"},
        json=chat_with_history
    )
    
    print(f"Status: {chat_response.status_code}")
    if chat_response.status_code == 200:
        response_data = chat_response.json()
        print(f"Response: {response_data['response']}")
    else:
        print(f"Error: {chat_response.text}")

if __name__ == "__main__":
    test_api()
