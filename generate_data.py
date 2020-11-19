import pandas as pd
import numpy as np
import random

from faker import Faker
from datetime import datetime

from bq_util import upload_df


def gen_fk():
    return np.random.randint(1, 20)


def gen_height():
    return np.random.randint(100, 200)


def gen_location_id():
    return np.random.randint(101, 105)


def generate_row(id):
    fake = Faker()

    return [id,
            gen_fk(),
            fake.name(),
            fake.email(),
            fake.address(),
            datetime.strptime(fake.date(), "%Y-%m-%d").date(),
            gen_height(),
            f'+62{fake.msisdn()}',
            fake.msisdn(),
            gen_location_id(),
            random.choice([True, False]),
            datetime.now()]


def make_df(row_count):
    df = pd.DataFrame([generate_row(id) for id in range(1, row_count)])
    df.columns = ['primary_key_id',
                  'foreign_key_id',
                  'name',
                  'email',
                  'address',
                  'birthdate',
                  'height',
                  'phone_number',
                  'ktp_id',
                  'location_id',
                  'is_validated',
                  'processed_dttm']
    return df



project_id = 'tokopedia-staging-198806'
target_dataset = 'aldous_test'
target_table = 'ge_table_user_2'


upload_df(make_df(5000), project_id, target_dataset, target_table)
