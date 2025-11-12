# 🍳 Recipe Management System

<div align="center">

![GitHub](https://img.shields.io/badge/Version-1.0.0-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.0+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

*A modern, intuitive recipe management application to organize your culinary creations*

[![Features](https://img.shields.io/badge/Features-8+-orange)](#features)
[![Documentation](https://img.shields.io/badge/Documentation-📖-purple)](#documentation)
[![Demo](https://img.shields.io/badge/Live_Demo-🚀-red)](#quick-start)

</div>

---

## ✨ Features

| 🎯 Feature | 📝 Description |
|-----------|---------------|
| **📖 Recipe Catalog** | Organize all your recipes in one beautiful interface |
| **🔍 Smart Search** | Find recipes by ingredients, categories, or cooking time |
| **📱 Web Interface** | Clean HTML interface for easy recipe management |
| **💾 Data Management** | Efficient JSON data handling and SQLite database |
| **🔄 Data Loading** | Automated recipe data loading from JSON files |
| **🔧 Diagnostics** | Built-in diagnostic tools for system health |
| **📊 Recipe Analysis** | Analyze and process recipe data efficiently |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Flask 2.0+
- Modern web browser

### Installation

```bash
# Clone the repository
git clone https://github.com/Karthigaiselvam-R-official/Recipe_Management_System.git

# Navigate to project directory
cd Recipe_Management_System/recipe_app

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

🎯 Usage
Access the application: Open http://localhost:5001 in your browser

Load recipe data: Use data_loader.py to import recipes

Browse recipes: Navigate through the web interface

Run diagnostics: Use diagnose.py for system checks

🛠️ Technology Stack
<div align="center">
Layer	Technology
Backend	Python, Flask
Database	SQLite
Data Format	JSON
Frontend	HTML, CSS
Data Processing	Custom Python scripts
</div>

📁 Project Structure
recipe_app/
├── 🐍 app.py              # Main Flask application
├── 📊 data_loader.py      # Recipe data loading utility
├── 🔧 diagnose.py         # System diagnostics and health checks
├── 💾 recipes.db          # SQLite database file
├── 🌐 index.html          # Web interface
├── 📄 requirements.txt    # Python dependencies
├── us_recipes_null.json  # Recipe dataset
└── 📖 README.md          # Project documentation

🔧 File Descriptions
File	Purpose
app.py	Main Flask application server and web routes
data_loader.py	Loads and processes recipe data from JSON to database
diagnose.py	Diagnostic tools for system verification and debugging
recipes.db	SQLite database containing recipe information
index.html	Web interface for recipe browsing and management
us_recipes_null.json	Dataset containing recipe information in JSON format

graph TD
    A[Recipe Data JSON] --> B[Data Loader]
    B --> C[SQLite Database]
    C --> D[Flask App]
    D --> E[Web Interface]
    F[User] --> E
    E --> G[Recipe Management]

🚀 Getting Started
Step 1: Setup Environment
bash
cd recipe_app
pip install -r requirements.txt
Step 2: Initialize Database
bash
python data_loader.py
Step 3: Launch Application
bash
python app.py
Step 4: Access Application
Open your browser and navigate to: http://localhost:5000

🧪 Running Diagnostics
Check system health and data integrity:

bash
python diagnose.py
📊 Data Schema
The application uses a structured recipe format:

Recipe Name

Ingredients

Instructions

Cooking Time

Difficulty Level

Category

🤝 Contributing
We welcome contributions! Here's how you can help:

🍴 Fork the repository

🌿 Create a feature branch (git checkout -b feature/AmazingFeature)

💾 Commit your changes (git commit -m 'Add AmazingFeature')

🚀 Push to the branch (git push origin feature/AmazingFeature)

🔃 Open a Pull Request

🐛 Troubleshooting
Common Issues:
Issue: Port 5000 already in use
Solution:

bash
# Kill process using port 5000
sudo lsof -t -i tcp:5000 | xargs kill -9
# Or use different port
python app.py --port 5001
Issue: Database connection error
Solution:

bash
python diagnose.py  # Run diagnostics
rm recipes.db       # Reset database (if needed)
python data_loader.py  # Reload data
📞 Support
<div align="center">
❓ Need Help?
We're here to support you!

Channel	Link
📧 Email	karthigaiselvamr.cs2022@gmail.com
🐛 Issues	GitHub Issues
</div>
<div align="center">
⭐ If you like this project, don't forget to give it a star!
Made with ❤️ by Karthigaiselvam R
</div>

Key Updates Made:
Correct Project Structure - Updated to match your actual file structure

Technology Stack - Changed from Django to Flask based on your files

File Descriptions - Added clear explanations for each file

Workflow Diagram - Shows how data flows through your system

Specific Instructions - Tailored to your actual application setup

Troubleshooting - Added practical solutions for common issues
