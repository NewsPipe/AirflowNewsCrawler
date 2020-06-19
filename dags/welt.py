import os
import datetime

from dag_factory import create_dag

url = "welt.de"
output_dir = "/output"
airflow_config = {'schedule_interval': '@hourly',
                  'start_date': datetime.datetime(2020, 6, 4, 21),
                  'end_date':datetime.datetime(2020, 6, 5, 6),
                  }

DAG = create_dag(url=url,
                 output_dir=output_dir,
                 airflow_config=airflow_config,
                 name=os.path.basename(__file__))