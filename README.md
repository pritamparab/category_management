# Require Packages
- Python 3.9 or higher

# Clone the git repository
git clone https://github.com/pritamparab/category_management.git

cd category_management

# Install Python Packages
1. pip install -r requirements.txt
2. python manage.py migrate
3. python manage.py populate_categories
4. python scripts/populate_data.py
5. python scripts/setup_groups.py

# Run Backend Server
python manage.py runserver

# Run Frontend 
1. cd frontend
2. npm install
3. npm run dev