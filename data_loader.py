# data_loader.py
import json
import sqlite3
import re
import os
from typing import Dict, List, Any, Optional

def create_database():
    """Create the database schema"""
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cuisine TEXT,
            title TEXT NOT NULL,
            rating REAL,
            prep_time INTEGER,
            cook_time INTEGER,
            total_time INTEGER,
            description TEXT,
            nutrients TEXT,
            serves TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database schema created successfully")

def parse_numeric_value(value):
    """Parse numeric values, handling NaN and invalid data"""
    if value is None:
        return None
    
    if isinstance(value, str):
        if value.lower() == 'nan' or value.strip() == '':
            return None
        # Try to extract numbers from strings
        numbers = re.findall(r'\d+\.?\d*', value)
        if numbers:
            try:
                num = float(numbers[0])
                return int(num) if num.is_integer() else num
            except:
                return None
        return None
    
    try:
        if isinstance(value, (int, float)):
            return value
        return float(value)
    except (ValueError, TypeError):
        return None

def parse_nutrients(nutrients_data):
    """Parse nutrients data"""
    if not nutrients_data:
        return "{}"
    
    if isinstance(nutrients_data, dict):
        clean_nutrients = {}
        for key, value in nutrients_data.items():
            if value and str(value).lower() != 'nan' and str(value).strip() != '':
                clean_nutrients[key] = str(value)
        return json.dumps(clean_nutrients)
    
    return "{}"

def extract_recipe_from_dict(recipe_dict):
    """Extract recipe data from a recipe dictionary"""
    try:
        # Extract fields directly using the exact field names from your JSON
        cuisine = recipe_dict.get('cuisine')
        title = recipe_dict.get('title')
        description = recipe_dict.get('description')
        serves = recipe_dict.get('serves')
        
        # Parse numeric fields
        rating = parse_numeric_value(recipe_dict.get('rating'))
        prep_time = parse_numeric_value(recipe_dict.get('prep_time'))
        cook_time = parse_numeric_value(recipe_dict.get('cook_time'))
        total_time = parse_numeric_value(recipe_dict.get('total_time'))
        
        # Calculate total_time if not provided but prep_time and cook_time exist
        if total_time is None and prep_time is not None and cook_time is not None:
            total_time = prep_time + cook_time
        
        # Parse nutrients
        nutrients = parse_nutrients(recipe_dict.get('nutrients'))
        
        # Only return if we have a title
        if title:
            return {
                'cuisine': cuisine,
                'title': title,
                'rating': rating,
                'prep_time': prep_time,
                'cook_time': cook_time,
                'total_time': total_time,
                'description': description,
                'nutrients': nutrients,
                'serves': serves
            }
    
    except Exception as e:
        print(f"⚠️ Error extracting recipe: {e}")
    
    return None

def load_all_recipes():
    """Load ALL recipes from JSON file - FIXED VERSION"""
    print("📂 Loading recipes from us_recipes_null.json...")
    
    if not os.path.exists('us_recipes_null.json'):
        print("❌ us_recipes_null.json not found!")
        return []
    
    try:
        with open('us_recipes_null.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        print(f"📊 JSON structure: {type(data)}")
        
        recipes = []
        
        # Your JSON is a dictionary with numeric keys like "0", "1", "2", etc.
        if isinstance(data, dict):
            print(f"🔑 Found {len(data)} recipes in dictionary structure")
            
            # Iterate through all numeric keys
            for key, recipe_data in data.items():
                if isinstance(recipe_data, dict):
                    recipe = extract_recipe_from_dict(recipe_data)
                    if recipe:
                        recipes.append(recipe)
                
                # Show progress for large files
                if len(recipes) % 100 == 0 and len(recipes) > 0:
                    print(f"   Extracted {len(recipes)} recipes...")
        
        print(f"✅ Successfully extracted {len(recipes)} recipes")
        
        # Show sample of extracted recipes
        if recipes:
            print("\n📋 Sample of extracted recipes:")
            for i in range(min(5, len(recipes))):
                print(f"   {i+1}. '{recipes[i]['title']}' - Cuisine: {recipes[i].get('cuisine', 'N/A')} - Rating: {recipes[i].get('rating', 'N/A')}")
        
        return recipes
        
    except Exception as e:
        print(f"❌ Error loading JSON file: {e}")
        import traceback
        traceback.print_exc()
        return []

def insert_recipes_into_database(recipes):
    """Insert recipes into SQLite database"""
    if not recipes:
        print("❌ No recipes to insert")
        return 0
    
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute('DELETE FROM recipes')
    
    # Prepare insert statement
    insert_sql = '''
        INSERT INTO recipes (cuisine, title, rating, prep_time, cook_time, total_time, description, nutrients, serves)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    
    # Insert all recipes
    inserted_count = 0
    for i, recipe in enumerate(recipes):
        try:
            cursor.execute(insert_sql, (
                recipe['cuisine'],
                recipe['title'],
                recipe['rating'],
                recipe['prep_time'],
                recipe['cook_time'],
                recipe['total_time'],
                recipe['description'],
                recipe['nutrients'],
                recipe['serves']
            ))
            inserted_count += 1
            
            # Show progress
            if (i + 1) % 100 == 0:
                print(f"   Inserted {i + 1} recipes...")
                
        except Exception as e:
            print(f"⚠️ Error inserting recipe {i}: {e}")
            continue
    
    conn.commit()
    conn.close()
    print(f"✅ Successfully inserted {inserted_count} recipes into database")
    return inserted_count

def main():
    """Main function to load data"""
    print("🚀 Starting data loader...")
    print("=" * 60)
    
    # Create database
    create_database()
    
    # Load recipes from JSON
    recipes = load_all_recipes()
    
    if not recipes:
        print("❌ No recipes found in JSON file")
        print("💡 Please check the JSON file structure")
        return
    
    # Insert into database
    inserted_count = insert_recipes_into_database(recipes)
    
    print("=" * 60)
    print(f"🎉 Data loading completed!")
    print(f"📊 Total recipes loaded: {inserted_count}")
    print("=" * 60)

if __name__ == '__main__':
    main()