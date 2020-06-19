# Airflow NewsCrawler
AirflowNewsCrawler is a software application for crawling online newspaper articles. It is based on [Airflow](https://airflow.readthedocs.io/en/stable/) and [TensorFlow Extended](https://www.tensorflow.org/tfx). The implementation dockerized, thus the user does not need to worry about dependencies. Additionally, `docker-compose` is available to increase the useability for the user. **To start this application run:**
```
docker-compose up
```
The application should be available on `localhost:8080`. You will see the airflow dashboard with our default examples:

![](imgs/dashboard.png)

The dags are defined in `dags`. Therefore to add/remove DAGs, you will have to add/remove DAGs in the `dags` folder. Please use one of the default example as template. The DAGs are very simple and straightforward.

```python
url = "taz.de" # Online newspaper source

output_dir = "/output" # Output directory 

# defining the crawling times
airflow_config = {'schedule_interval': '@hourly',
                  'start_date': datetime.datetime(2020, 6, 4, 21),
                  'end_date':datetime.datetime(2020, 6, 5, 6),
                  }

# create DAG
DAG = create_dag(url=url,
                 output_dir=output_dir,
                 airflow_config=airflow_config,
                 name=os.path.basename(__file__))
```


