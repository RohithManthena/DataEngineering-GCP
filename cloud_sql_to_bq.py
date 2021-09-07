import os
from airflow import DAG
from datetime import datetime
from airflow.contrib.operators.mysql_to_gcs import MySqlToGoogleCloudStorageOperator
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from airflow.contrib.operators.bigquery_operator import BigQueryOperator

CLOUD_SQL_INSTANCE = 'mysql-instance-prod-v1'
DEFAULT_DATABASE = 'classicmodels'
AGGREGATE_TABLE = 'top_five_employees'

class TableConfig:
    STANDARD_EXPORT_QUERY = None
    _STANDARD_EXPORT_QUERY = "SELECT * from {}"

    def __init__(self,
                 cloud_sql_instance,
                 export_bucket,
                 export_table,
                 export_query,
                 gcp_project,
                 stage_table,
                 stage_final_query,
                 bq_location
                 ):

        self.params = {
            'export_table': export_table,
            'export_bucket': export_bucket,
            'export_database': DEFAULT_DATABASE,
            'export_query': export_query or self._STANDARD_EXPORT_QUERY.format(export_table),
            'gcp_project': gcp_project,
            'stage_dataset': DEFAULT_DATABASE,
            'stage_table': stage_table or export_table,
            'stage_final_query': stage_final_query,
            'cloud_sql_instance': cloud_sql_instance,
            'bq_location': bq_location or "US",
        }

# args
DEFAULT_ARGS = {
    'owner': 'Surya Manthena',
    'depend_on_past': False,
    'start_date': datetime(2021, 1, 1, 10, 00, 00),
    'email': []
}

dag_id = 'cloud-sql-to-bq-dag'
dag = DAG(dag_id,
          default_args=DEFAULT_ARGS,
          schedule_interval='*/5 * * * *',
          catchup=False)


def get_tables():
    export_tables = ['customers', 'employees', 'offices', 'orderdetails', 'orders', 
                     'payments', 'productlines', 'products']
    tables = []
    for table in export_tables:
        tables.append(TableConfig(cloud_sql_instance=CLOUD_SQL_INSTANCE,
                                  export_table=table,
                                  export_bucket=os.environ['GCP_PROJECT'],
                                  export_query=TableConfig.STANDARD_EXPORT_QUERY,
                                  gcp_project=os.environ['GCP_PROJECT'],
                                  stage_table=None,
                                  stage_final_query=None,
                                  bq_location="US"))
    return tables

def gen_export_table_task(table_config):
    export_task = MySqlToGoogleCloudStorageOperator(task_id='export_{}'.format(table_config.params['export_table']),
                                                    dag=dag,
                                                    sql=table_config.params['export_query'],
                                                    bucket=table_config.params['export_bucket'],
                                                    filename='cloudsql-to-bigquery/{}/{}'.format(table_config.params['export_table'],
                                                                                                 table_config.params['export_table']) + '_{}',
                                                    schema_filename='cloudsql-to-bigquery/schema/{}/schema_raw'.format(table_config.params['export_table']),
                                                    mysql_conn_id='cloud_sql_proxy_conn')
    return export_task


def gen_import_table_task(table_config):
    import_task = GoogleCloudStorageToBigQueryOperator(
        task_id='{}_to_bigquery'.format(table_config.params['export_table']),
        bucket=table_config.params['export_bucket'],
        source_objects=['cloudsql-to-bigquery/{}/{}*'.format(table_config.params['export_table'],
                                                             table_config.params['export_table'])],
        destination_project_dataset_table='{}.{}.{}'.format(table_config.params['gcp_project'],
                                                            table_config.params['stage_dataset'],
                                                            table_config.params['stage_table']),
        schema_object="cloudsql-to-bigquery/schema/{}/schema_raw".format(table_config.params['export_table']),
        write_disposition='WRITE_TRUNCATE',
        source_format="NEWLINE_DELIMITED_JSON",
        dag=dag)

    return import_task

aggregate_tables_task = BigQueryOperator(
    task_id='aggregate_tables',
    sql="""SELECT
  firstName,
  lastName,
  total_amount
FROM (
  SELECT
    e.employeeNumber,
    ROUND(SUM(amount)) AS total_amount
  FROM
    classicmodels.employees AS e
  JOIN
    classicmodels.customers AS c
  ON
    e.employeeNumber = c.salesRepEmployeeNumber
  JOIN
    classicmodels.payments AS p
  ON
    c.customerNumber = p.customerNumber
  GROUP BY
    e.employeeNumber ) AS s
JOIN
  classicmodels.employees AS e
ON
  s.employeeNumber = e.employeeNumber
ORDER BY
  3 DESC
LIMIT
  5""",
    destination_dataset_table='{}:{}.{}'.format(os.environ['GCP_PROJECT'], DEFAULT_DATABASE, AGGREGATE_TABLE),
    write_disposition='WRITE_TRUNCATE',
    create_disposition='CREATE_IF_NEEDED',
    use_legacy_sql=False,
    dag=dag
)


"""
The code that follows setups the dependencies between the tasks
"""

for table_config in get_tables():
    export_script = gen_export_table_task(table_config)
    import_script = gen_import_table_task(table_config)

    export_script >> import_script >> aggregate_tables_task
