import pygsheets
import pandas as pd
import numpy as np

def main():
    client = pygsheets.authorize(service_account_file='config.json')
    sheet = client.open('Repo Link Responses')
    wks = sheet.worksheet(property='index', value=0)
    df = wks.get_as_df()
    unique_urls = df["Paste link to clone your repo"].unique()
    np.savetxt("repo_urls.txt", unique_urls, delimiter="\n", fmt="%s")
    

if __name__ == '__main__':
    main()
