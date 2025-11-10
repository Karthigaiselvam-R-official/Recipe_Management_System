# app.py
from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import json
import re
import os

app = Flask(__name__, static_folder='.')

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect('recipes.db')
    conn.row_factory = sqlite3.Row
    return conn

def recipe_row_to_dict(row):
    """Convert SQLite row to recipe dictionary"""
    if row is None:
        return None
    
    recipe = dict(row)
    
    # Parse nutrients JSON
    nutrients_str = recipe.get('nutrients', '{}')
    if nutrients_str and nutrients_str != '{}':
        try:
            recipe['nutrients'] = json.loads(nutrients_str)
        except:
            recipe['nutrients'] = {}
    else:
        recipe['nutrients'] = {}
    
    # Parse ingredients if it's a string
    ingredients_str = recipe.get('ingredients', '[]')
    if ingredients_str and isinstance(ingredients_str, str) and ingredients_str.startswith('['):
        try:
            recipe['ingredients'] = json.loads(ingredients_str)
        except:
            recipe['ingredients'] = []
    
    return recipe

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    """Get all recipes without pagination for initial load"""
    try:
        # Get all recipes at once for frontend filtering
        query = '''
            SELECT * FROM recipes 
            ORDER BY 
                CASE WHEN rating IS NULL THEN 0 ELSE rating END DESC,
                title ASC
        '''
        conn = get_db_connection()
        recipes_rows = conn.execute(query).fetchall()
        conn.close()
        
        # Convert to dictionaries
        recipes = [recipe_row_to_dict(row) for row in recipes_rows]
        
        # Get total count
        total = len(recipes)
        
        # Prepare response
        response = {
            'total': total,
            'data': recipes
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recipes/paginated', methods=['GET'])
def get_recipes_paginated():
    """Get recipes with pagination"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 15, type=int)
        
        # Validate parameters
        if page < 1:
            page = 1
        if limit < 1:
            limit = 15
        if limit > 200:
            limit = 200
        
        # Calculate offset
        offset = (page - 1) * limit
        
        # Get total count
        conn = get_db_connection()
        total = conn.execute('SELECT COUNT(*) FROM recipes').fetchone()[0]
        conn.close()
        
        # Get paginated results
        query = '''
            SELECT * FROM recipes 
            ORDER BY 
                CASE WHEN rating IS NULL THEN 0 ELSE rating END DESC,
                title ASC
            LIMIT ? OFFSET ?
        '''
        conn = get_db_connection()
        recipes_rows = conn.execute(query, (limit, offset)).fetchall()
        conn.close()
        
        # Convert to dictionaries
        recipes = [recipe_row_to_dict(row) for row in recipes_rows]
        
        # Prepare response
        response = {
            'page': page,
            'limit': limit,
            'total': total,
            'data': recipes
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recipes/search', methods=['GET'])
def search_recipes():
    """Search recipes with various filters"""
    try:
        # Get query parameters
        title_filter = request.args.get('title')
        cuisine_filter = request.args.get('cuisine')
        total_time_filter = request.args.get('total_time')
        rating_filter = request.args.get('rating')
        
        # Start with base query
        query = 'SELECT * FROM recipes WHERE 1=1'
        params = []
        
        # Apply filters
        if title_filter:
            query += ' AND title LIKE ?'
            params.append(f'%{title_filter}%')
        
        if cuisine_filter:
            query += ' AND cuisine LIKE ?'
            params.append(f'%{cuisine_filter}%')
        
        # Parse and apply numeric filters
        if total_time_filter:
            operator, value = parse_filter_operator(total_time_filter)
            if operator and value is not None:
                query += f' AND total_time {operator} ?'
                params.append(value)
        
        if rating_filter:
            operator, value = parse_filter_operator(rating_filter)
            if operator and value is not None:
                query += f' AND rating {operator} ?'
                params.append(value)
        
        # Add sorting
        query += ' ORDER BY CASE WHEN rating IS NULL THEN 0 ELSE rating END DESC, title ASC'
        
        # Execute query
        conn = get_db_connection()
        recipes_rows = conn.execute(query, params).fetchall()
        conn.close()
        
        # Convert to dictionaries
        recipes = [recipe_row_to_dict(row) for row in recipes_rows]
        
        # Prepare response
        response = {
            'data': recipes,
            'count': len(recipes)
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def parse_filter_operator(filter_string):
    """Parse filter operator and value from string like '>=4.5'"""
    if not filter_string:
        return None, None
    
    operator = None
    value_str = filter_string
    
    for op in ['>=', '<=', '>', '<', '=']:
        if filter_string.startswith(op):
            operator = op
            value_str = filter_string[len(op):]
            break
    
    # Default to equals if no operator found
    if not operator:
        operator = '='
    
    try:
        value = float(value_str)
        return operator, value
    except (ValueError, TypeError):
        return None, None

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get API status and database info"""
    try:
        conn = get_db_connection()
        count = conn.execute('SELECT COUNT(*) FROM recipes').fetchone()[0]
        
        # Get sample recipes to verify data
        sample_recipes = conn.execute('SELECT title, cuisine, rating FROM recipes LIMIT 5').fetchall()
        conn.close()
        
        sample_data = []
        for row in sample_recipes:
            sample_data.append({
                'title': row['title'],
                'cuisine': row['cuisine'],
                'rating': row['rating']
            })
        
        return jsonify({
            'status': 'running',
            'database_records': count,
            'message': f'Database contains {count} recipes',
            'sample_data': sample_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Check if database exists
    if not os.path.exists('recipes.db'):
        print("❌ Database not found. Please run data_loader.py first.")
        exit(1)
    
    # Check database content
    conn = get_db_connection()
    count = conn.execute('SELECT COUNT(*) FROM recipes').fetchone()[0]
    conn.close()
    
    print("=" * 60)
    print("🚀 Recipe Management System API")
    print("=" * 60)
    print(f"📊 Database contains {count} recipes")
    print("🌐 Access the application at: http://localhost:5001")
    print("🔍 API Status: http://localhost:5001/api/status")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5001)