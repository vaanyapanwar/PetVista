# 🐾 PetVista — Web App

A warm, pet-owner-friendly inventory & sales management system built with Flask + MySQL.

<img width="1448" height="953" alt="Screenshot 2026-06-03 112407" src="https://github.com/user-attachments/assets/5c733b93-108a-4f09-b4f3-5116a55f5b89" />

## Project Structure

```
petvista/
├── app.py                  ← Flask backend (all routes)
├── requirements.txt        ← Python dependencies
├── setup.sql               ← DB setup + optional sample data
├── templates/
│   ├── base.html           ← Sidebar layout, nav, flash messages
│   ├── index.html          ← Dashboard with hero, stats, quick views
│   ├── products.html       ← Product grid with search & filter
│   ├── add_product.html    ← Add product form
│   ├── edit_product.html   ← Edit price/quantity form
│   ├── sell.html           ← Make a sale (live total preview)
│   └── sales.html          ← Full sales history table
└── static/
    ├── css/style.css       ← All styles (warm cream + amber palette)
    └── js/main.js          ← Live sell preview, flash auto-dismiss
```

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Create the database
```bash
mysql -u root -p < setup.sql
```
Or open MySQL Workbench / CLI and run `setup.sql` manually.

### 3. Update credentials in `app.py` if needed
```python
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",     # ← change if different
    database="petvista"
)
```

### 4. Run the app
```bash
python app.py
```

Open **http://localhost:5000** in your browser.

## Features
- 🏠 **Dashboard** — stats overview, low stock alerts, recent sales
- 📦 **Products** — card grid, search by name, filter by category, add/edit/delete
- 🛒 **Sell** — dropdown product picker with live total calculation
- 📊 **Sales History** — full table sorted newest first, total revenue pill
