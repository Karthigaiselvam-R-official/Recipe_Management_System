# diagnose_json.py
import json
import os

def diagnose_json():
    print("🔍 Diagnosing JSON file structure...")
    print("=" * 60)
    
    if not os.path.exists('us_recipes_null.json'):
        print("❌ us_recipes_null.json not found!")
        print("Current directory:", os.getcwd())
        print("Files in directory:", [f for f in os.listdir('.') if f.endswith('.json')])
        return
    
    try:
        with open('us_recipes_null.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ JSON file loaded successfully")
        print(f"📊 Data type: {type(data)}")
        
        if isinstance(data, list):
            print(f"📈 Number of items in array: {len(data)}")
            if data:
                print(f"🔑 First item keys: {list(data[0].keys())}")
                print(f"📝 Sample of first item:")
                for key in list(data[0].keys())[:10]:  # Show first 10 keys
                    value = data[0][key]
                    preview = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                    print(f"   {key}: {preview}")
        
        elif isinstance(data, dict):
            print(f"🔑 Dictionary keys: {list(data.keys())}")
            for key in data.keys():
                value = data[key]
                print(f"   {key}: type={type(value)}")
                if isinstance(value, list):
                    print(f"      List length: {len(value)}")
                    if value and isinstance(value[0], dict):
                        print(f"      First item keys: {list(value[0].keys())}")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"❌ Error reading JSON: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    diagnose_json()