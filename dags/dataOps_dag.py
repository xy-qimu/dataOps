#!/usr/bin/env python3
"""
 @功能描述: Run a dbt Core project as a task group with Cosmos
 @创建人:  tik.xie
 @创建日期: 2023-10-28
"""
import include.dbt_dw as dbt
from pendulum import datetime, duration, timezone
from cosmos import DbtTaskGroup
from include.dag_callback import failure_callback, success_callback, retry_callback
from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.macros import ds_add, ds_format, timedelta
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator

local_tz = timezone("Asia/Shanghai")

#-------  Variable definitions  ------------------------------------------------

# get variable
# vJobRun = Variable.get("v_kettle_job_run")
# vEmail = Variable.get("v_email")

vETLDate = '{{ next_ds }}'   # dag 于 2023-11-9 执行，则 etl date 为 2023-11-8

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
    # "pool": 'dw_pool',
}

with DAG(
    dag_id="dataOps",
    start_date=datetime(2023, 11, 11, 9, 0, tz=local_tz),
    schedule_interval="0 1 * * *",
    catchup=False,
    max_active_runs=1,
    default_args=dag_args

):
    task_start = EmptyOperator(task_id="DW-Start")

    trigger_k3_airbyte_sync = AirbyteTriggerSyncOperator(
        task_id= 'k3_trigger_sync'
        , airbyte_conn_id= 'conn_airbyte'         # Airflow connection
        , connection_id= '66031d5a-f729-4513-9088-ee6eee255f08'   # airbyte connection id

    )

    dbt_tasks = DbtTaskGroup(
        project_config = dbt.project_cfg
        , profile_config = dbt.profile_cfg
        , execution_config = dbt.execution_cfg
        , operator_args={"vars": {"etl_date": vETLDate}}
    )

    task_end = EmptyOperator(task_id="DW-End", on_success_callback = success_callback)


    task_start >> trigger_k3_airbyte_sync >> dbt_tasks >> task_end