DATABASE_ID = "26b597b7ded4429fa949dfe6390f9950"
SECRET_KEY = "secret_JlQryh59QqOTwqxqmpne0SGoXkizufC3rEhiVbLhW0c"
headers = {
    "Authorization": f"Bearer {SECRET_KEY}",
    'Notion-Version': "2022-02-22",
    "Content-Type": "application/json"
}

# type_days = ['Mon', 'Wed', 'Mo', 'Thu', 'Fri', 'Tue', 'Sat', 'Sun']
type_days_dict = {
    'Mon': 0,
    'Tue': 1,
    'Wed': 2,
    "Thu": 3,
    "Fri": 4,
    "Sat": 5,
    "Sun": 6,
    "Mo": 0,
}