import yaml
class Config:

    with open('/Users/ankitjha/Downloads/credentials.yaml') as f:
        content = f.read()
        my_credentials = yaml.load(content, Loader = yaml.FullLoader)
        user, password = my_credentials['email_id'], my_credentials['password']
    IMAP_SERVER = "imap.gmail.com"
    EMAIL = user
    PASSWORD = password
    FETCH_COUNT = 100
    DATE_FROM = '20-May-2024'
    DATE_TO = '28-May-2024'
    SENDER_EMAIL = 'alerts@hdfcbank.com'
    PICKLE_FILENAME = 'dataframe.pkl'


    HDFC_EMAIL_DETAILS = [FETCH_COUNT,"inbox","alerts@hdfcbank.net",DATE_FROM,DATE_TO]
    search_criteria = f'(FROM "{SENDER_EMAIL}" SINCE {DATE_FROM} BEFORE {DATE_TO})'

