import datetime
import great_expectations as ge
# import great_expectations.jupyter_ux
from great_expectations.data_context.types.resource_identifiers import (
    ValidationResultIdentifier,
)

context = ge.data_context.DataContext()

expectation_suite_name = "ge_table_user_1"
suite = context.get_expectation_suite(expectation_suite_name)
suite.expectations = []

batch_kwargs = {
    "query": "SELECT * FROM `tokopedia-staging-198806.aldous_test.ge_table_user_1` limit 12",
    "bigquery_temp_table": "tokopedia-staging-198806.aldous_test.tmp_ge_table_user_1",
    "data_asset_name": "ge_table_user_1",
    "datasource": "tokopedia-staging-198806",
    "schema": None,
    "table": "ge_table_user_1",
}

batch = context.get_batch(batch_kwargs, suite)
batch.head()

# Table Expectations
batch.expect_table_row_count_to_be_between(max_value=5498, min_value=4499)
batch.expect_table_column_count_to_equal(value=12)
batch.expect_table_columns_to_match_ordered_list(
    column_list=[
        "primary_key_id",
        "foreign_key_id",
        "name",
        "email",
        "address",
        "birthdate",
        # "height",
        # "phone_number",
        # "ktp_id",
        # "location_id",
        "is_validated",
        "processed_dttm",
    ]
)

# Column Expectations
## primary_key_id
batch.expect_column_values_to_be_unique(column="primary_key_id")
batch.expect_column_values_to_not_be_null(column="primary_key_id")

## foreign_key_id
batch.expect_column_values_to_not_be_null(column="foreign_key_id")
batch.expect_column_distinct_values_to_be_in_set(
    column="foreign_key_id",
    value_set=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
)

## name
batch.expect_column_values_to_not_be_null(column="name")
batch.expect_column_value_lengths_to_be_between(column="name", min_value=1)

## email
batch.expect_column_values_to_be_unique(column="email")
batch.expect_column_values_to_not_be_null(column="email")
batch.expect_column_value_lengths_to_be_between(column="email", min_value=1)

## address
batch.expect_column_values_to_be_unique(column="address")
batch.expect_column_values_to_not_be_null(column="address")
batch.expect_column_value_lengths_to_be_between(column="address", min_value=1)

## birthdate
batch.expect_column_values_to_be_unique(column="birthdate")
batch.expect_column_values_to_not_be_null(column="birthdate")
batch.expect_column_value_lengths_to_be_between(column="birthdate", min_value=1)

## is_validated
batch.expect_column_values_to_not_be_null(column="is_validated")
batch.expect_column_distinct_values_to_be_in_set(
    column="is_validated", value_set=[False, True]
)

## processed_dttm
batch.expect_column_values_to_be_unique(column="processed_dttm")
batch.expect_column_values_to_not_be_null(column="processed_dttm")
batch.expect_column_values_to_be_between(
    column="processed_dttm",
    max_value="2021-11-18 17:33:55.552680+00:00",
    min_value="2019-11-19 17:32:51.130709+00:00",
    parse_strings_as_datetimes=True,
)

batch.save_expectation_suite(discard_failed_expectations=False)

results = context.run_validation_operator("action_list_operator", assets_to_validate=[batch])
validation_result_identifier = results.list_validation_result_identifiers()[0]
context.build_data_docs()
context.open_data_docs(validation_result_identifier)