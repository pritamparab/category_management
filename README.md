# Require Packages
- Python 3.9 or higher

# Clone the git repository
git clone https://github.com/pritamparab/category_management.git

cd category_management

# Install Python Packages
pip install -r requirements.txt
python manage.py migrate
python manage.py populate_categories
python scripts/populate_data.py
python scripts/setup_groups.py
python manage.py makemigrations
python manage.py migrate

# Run Backend Server
python manage.py runserver

# Run Frontend 
cd frontend
npm install
npm run dev