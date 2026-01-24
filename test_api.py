# test_api.py
import requests

BASE_URL = "http://127.0.0.1:8000"

def test_top_products():
    print("\n========== Top Products ==========")
    try:
        resp = requests.get(f"{BASE_URL}/reports/top-products")
        resp.raise_for_status()
        data = resp.json()
        for item in data.get("top_products", []):
            print(f"{item['product']} -> {item['mentions']} mentions")
    except requests.HTTPError as e:
        print(f"Error: {e} {resp.text}")

def test_visual_content():
    print("\n========== Visual Content Stats ==========")
    try:
        resp = requests.get(f"{BASE_URL}/reports/visual-content")
        resp.raise_for_status()
        data = resp.json()
        for item in data:
            print(f"{item['channel_name']}: {item['messages_with_images']}/{item['total_messages']} messages with images ({item['image_percentage']}%)")
    except requests.HTTPError as e:
        print(f"Error: {e} {resp.text}")

def test_channel_activity(channel_name):
    print(f"\n========== Channel Activity: {channel_name} ==========")
    try:
        resp = requests.get(f"{BASE_URL}/channels/{channel_name}/activity")
        resp.raise_for_status()
        data = resp.json()
        for item in data.get("activity", []):
            print(f"{item['date']} -> {item['message_count']} messages")
    except requests.HTTPError as e:
        print(f"Error: {e} {resp.text}")

def test_search_messages(query):
    print(f"\n========== Search Messages: '{query}' ==========")
    try:
        resp = requests.get(f"{BASE_URL}/search/messages", params={"query": query, "limit": 20})
        resp.raise_for_status()
        data = resp.json()
        for msg in data.get("messages", []):
            print(f"[{msg['created_at']}] {msg['channel_name']}: {msg['text']}")
    except requests.HTTPError as e:
        print(f"Error: {e} {resp.text}")

if __name__ == "__main__":
    test_top_products()
    test_visual_content()
    test_channel_activity("HealthTipsChannel")
    test_search_messages("paracetamol")
