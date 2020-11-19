import pandas as pd
import pydata_google_auth
import os
import pandas_gbq
from google.oauth2 import service_account


def get_user_credentials():
    try:
        return service_account.Credentials.from_service_account_file(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'))
    except:
        SCOPES = [
            'https://www.googleapis.com/auth/cloud-platform',
            'https://www.googleapis.com/auth/drive',
        ]

        return pydata_google_auth.get_user_credentials(
            SCOPES,
            auth_local_webserver=False,
        )


def query_bq(query, project_id, credentials=get_user_credentials()):
    try:
        return pandas_gbq.read_gbq(query, project_id=project_id, credentials=credentials)
    except Exception as e:
        return e


def upload_df(df, project_id, target_dataset, target_table, if_exists='append', credentials=get_user_credentials()):

    try:
        return pandas_gbq.to_gbq(df, destination_table=f'{target_dataset}.{target_table}', project_id=project_id, if_exists=if_exists, credentials=credentials)
    except Exception as e:
        return e
