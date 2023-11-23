#!/usr/bin/env python3
"""
 @功能描述: Run a dbt Core project as a task group with Cosmos
 @创建人:  tik.xie
 @创建日期: 2023-10-28
"""
from airflow import DAG
# from airflow.models import Variable
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.macros import ds_add, ds_format, timedelta
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig
from pathlib import Path

from pendulum import datetime, duration, timezone

from wechat_operator import WechatOperator

local_tz = timezone("Asia/Shanghai")


#-------  Variable definitions  ------------------------------------------------

# get variable
# vJobRun = Variable.get("v_kettle_job_run")
# vEmail = Variable.get("v_email")

vETLDate = '{{ next_ds }}'   # 如 dag 在 2023-11-9 执行，则 etl date 为 2023-11-8

dbt_project_path = Path("/usr/local/airflow/dbt/dw")
dbt_executable = Path("/usr/local/airflow/dbt_venv/bin/dbt")


vAirb_Airflow_Conn = 'conn_airbyte'         # Airflow connection
vK3_Airbyte_Conn_ID = '66031d5a-f729-4513-9088-ee6eee255f08'   # airbyte connection id


profile_config = ProfileConfig(
    profile_name="default",
    target_name="dev",
    profiles_yml_filepath= dbt_project_path / "profiles.yml",
)


def failure_callback(context):
    message = '# <font color="warning">Airflow Task Failure Tips:</font>\n' \
              '> ## DAG:  {}\n' \
              '> ## Task:  {}\n' \
              '**Finish Time:**  {}\n' \
              '**Reason:** {}\n' \
        .format(context['task_instance'].dag_id,
                context['task_instance'].task_id,
                local_tz.convert(context['task_instance'].end_date).strftime("%Y-%m-%d %H:%M:%S"),
                context['exception'])
    return WechatOperator(
        task_id='failure_callback',
        wechat_conn_id='conn_wechat',
        message_type='markdown',
        message=message,
        at_all=True,
    ).execute(context)


def success_callback(context):
    message = '# <font color="info">Airflow Task Success Tips:</font>\n' \
              '> ## DAG:  {}\n' \
              '> ## Task:  {}\n' \
              '**Finish Time:**  {}\n' \
        .format(context['task_instance'].dag_id,
                context['task_instance'].task_id,
                local_tz.convert(context['task_instance'].end_date).strftime("%Y-%m-%d %H:%M:%S"))
    return WechatOperator(
        task_id='success_callback',
        wechat_conn_id='conn_wechat',
        message_type='markdown',
        message=message,
        at_all=True,
    ).execute(context)


def retry_callback(context):
    message = '# <font color="comment">Airflow Task Retry Tips:</font>\n' \
              '> ## DAG:  {}\n' \
              '> ## Task:  {}\n' \
              '> **Finish Time:**  {}\n' \
              '**Reason:** {}\n' \
        .format(context['task_instance'].dag_id,
                context['task_instance'].task_id,
                local_tz.convert(context['task_instance'].end_date).strftime("%Y-%m-%d %H:%M:%S"),
                context['exception'])
    return WechatOperator(
        task_id='retry_callback',
        wechat_conn_id='conn_wechat',
        message_type='markdown',
        message=message,
        at_all=True,
    ).execute(context)

dag_args = {
    "owner": "dw",  # Defines the value of the "owner" column in the DAG view of the Airflow UI
    "retries": 2,  # If a task fails, it will retry 3 times.
    "retry_delay": duration(minutes=3),  # A task that fails will wait 3 minutes to retry.
    "execution_timeout": duration(minutes=100),
    "email": 'xxx@qq.com',
    "email_on_failure": False,
    "email_on_retry": False,
    'on_failure_callback': failure_callback,
    # 'on_success_callback': success_callback,
    'on_retry_callback': retry_callback,
    # "pool": 'parallel_run_num',
}

with DAG(
    dag_id="dataOps",
    start_date=datetime(2023, 11, 11, 9, 0, tz=local_tz),
    schedule_interval="0 1 * * *",
    catchup=False,
    max_active_runs=1,
    default_args=dag_args

):
    e1 = EmptyOperator(task_id="DW-Start")

    trigger_k3_airbyte_sync = AirbyteTriggerSyncOperator(
        task_id='k3_trigger_sync',
        airbyte_conn_id=vAirb_Airflow_Conn,
        connection_id=vK3_Airbyte_Conn_ID,

    )

    dbt_tg = DbtTaskGroup(
        project_config=ProjectConfig(dbt_project_path)
        , profile_config=profile_config
        , execution_config=ExecutionConfig(dbt_executable_path=str(dbt_executable))
        , operator_args={"vars": {"etl_date": vETLDate}}
    )

    e2 = EmptyOperator(task_id="DW-End"
                       ,on_success_callback=success_callback)


    e1 >> trigger_k3_airbyte_sync >> dbt_tg >> e2