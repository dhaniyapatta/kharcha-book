from config import Config
from imap_connect import IMAPClient
from email_parser import EmailParser
import pandas as pd
from tabulate import tabulate


def main():

    imap_client = IMAPClient(Config.IMAP_SERVER, Config.EMAIL, Config.PASSWORD)

    emails = imap_client.fetch_emails(*Config.HDFC_EMAIL_DETAILS)
    df= EmailParser.email_to_dataframe(emails)
    df.to_pickle(Config.PICKLE_FILENAME)



if __name__ == "__main__":
    main()