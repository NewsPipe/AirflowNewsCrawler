import os
import datetime

from dag_factory import create_dag

url = "bild.net"
output_dir = "/output"
airflow_config = {'schedule_interval': '*/30 * * * *', # every 30 minutes
                  'start_date': datetime.datetime(2020, 7, 6, 21), # year, month, day, hour
                  }

DAG = create_dag(url=url,
                 output_dir=output_dir,
                 airflow_config=airflow_config,
                 name=os.path.basename(__file__))