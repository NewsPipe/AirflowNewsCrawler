import os

from typing import Any, Dict, List, Text

from tfx import types

from tfx.components.base import base_component
from tfx.components.base import executor_spec
from tfx.components.base import base_executor

from tfx.types import standard_artifacts

from tfx.types.artifact_utils import get_single_uri

from tfx.types.component_spec import ChannelParameter
from tfx.types.component_spec import ExecutionParameter

from tfx.utils.dsl_utils import external_input

from tfx.orchestration import metadata
from tfx.orchestration import pipeline

from tfx.orchestration.airflow.airflow_dag_runner import AirflowDagRunner
from tfx.orchestration.airflow.airflow_dag_runner import AirflowPipelineConfig

from newscrawler.crawler import Crawler


class Executor(base_executor.BaseExecutor):

    def Do(self, input_dict: Dict[Text, List[types.Artifact]],
           output_dict: Dict[Text, List[types.Artifact]],
           exec_properties: Dict[Text, Any]) -> None:
        crawler = Crawler(exec_properties["url"])
        rss_feed = crawler.get_article_information_as_dataframe()

        output_path = os.path.join(get_single_uri(output_dict["rss_feed"]), "feed.csv")
        rss_feed.to_csv(output_path, index=False)


class NewsCrawlerSpec(types.ComponentSpec):
    PARAMETERS = {
        'url': ExecutionParameter(type=Text),
    }

    INPUTS = {}

    OUTPUTS = {
        'rss_feed': ChannelParameter(type=standard_artifacts.ExternalArtifact),
    }


class NewsCrawler(base_component.BaseComponent):
    SPEC_CLASS = NewsCrawlerSpec
    EXECUTOR_SPEC = executor_spec.ExecutorClassSpec(Executor)

    def __init__(self,
                 url: Text,
                 rss_feed: types.Channel = None):
        if not rss_feed:
            rss_feed = external_input("rss_feed")

        spec = NewsCrawlerSpec(url=url,
                              rss_feed=rss_feed)

        super(NewsCrawler, self).__init__(spec=spec)


def create_dag(name, url, output_dir, airflow_config):
    pipeline_name = name
    pipeline_root = os.path.join(output_dir, 'pipelines', pipeline_name)
    metadata_path = os.path.join(output_dir, 'metadata', pipeline_name,
                                 'metadata.db')

    crawler = NewsCrawler(url=url)
    tfx_pipeline = pipeline.Pipeline(pipeline_name=pipeline_name,
                                     pipeline_root=pipeline_root,
                                     components=[crawler],
                                     enable_cache=False,
                                     metadata_connection_config=metadata.sqlite_metadata_connection_config(
                                         metadata_path))

    return AirflowDagRunner(AirflowPipelineConfig(airflow_config)).run(tfx_pipeline)
