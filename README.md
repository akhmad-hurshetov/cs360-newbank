# newbank-starter

This is a complementary starter project. You may clone the following repository to proceed with lab assignments.

### Usage
1. Set up Python virtual environment:
```
python3 -m venv .env
source .env/bin/activate
```
2. Install Django:
```
pip install --upgrade pip
pip install Django
django-admin --version
```
3. Clone the project:
```
git clone https://github.com/NUU-SE201/newbank.git
cd newbank-starter
python3 manage.py runserver
```
4. Open the following URLs in your browser:
```
http://127.0.0.1:8000/cards/
http://127.0.0.1:8000/cards/Visa/
http://127.0.0.1:8000/currency/
http://127.0.0.1:8000/currency/exchange/?from=usd&to=uzs
```

### Note
Do not submit PRs to this repository unless they fix an existing bug.
This project is meant to be a starter project, new features wil not be added.
