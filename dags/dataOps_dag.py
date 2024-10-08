#!/usr/bin/env python3
"""
 @功能描述: Run a dbt Core project as a task group with Cosmos
 @创建人:  tik.xie
 @创建日期: 2023-10-28
"""
import include.dbt_edw as dbt
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

# -------  Variable definitions  ------------------------------------------------

# get variable
# vJobRun = Variable.get("v_kettle_job_run")
# vEmail = Variable.get("v_email")

airflow_conn_id_airbyte = "conn_airbyte"  # Airflow connection
airbyte_connection_id = "66031d5a-f729-4513-9088-ee6eee255f08"  # airbyte connection id

ETL_Date = "{{ data_interval_start.in_timezone('Asia/Shanghai').strftime('%Y-%m-%d')}}"  # data_interval_start

dag_args = {
    "owner": "tik",  # Defines the value of the "owner" column in the DAG view of the Airflow UI
    "retries": 2,  # If a task fails, it will retry 3 times.
    "retry_delay": duration(
        minutes=3
    ),  # A task that fails will wait 3 minutes to retry.
    "execution_timeout": duration(minutes=100),
    "email": "xxx@qq.com",
    "email_on_failure": False,
    "email_on_retry": False,
    "on_failure_callback": failure_callback,
    # 'on_success_callback': success_callback,
    "on_retry_callback": retry_callback,
    # "pool": 'airflow_pool',
}

with DAG(
    dag_id="dataOps",
    start_date=datetime(2023, 11, 11, 9, 0, tz=local_tz),
    schedule_interval="0 1 * * *",
    catchup=False,
    max_active_runs=1,
    default_args=dag_args,
):
    _start = EmptyOperator(task_id="ETL-Start")

    trigger_pos_airbyte_sync = AirbyteTriggerSyncOperator(
        task_id="pos_trigger_sync",
        airbyte_conn_id=airflow_conn_id_airbyte,  # Airflow connection
        connection_id=airbyte_connection_id,  # airbyte connection id
    )

    dbt_tasks = DbtTaskGroup(
        project_config=dbt.project_cfg,
        profile_config=dbt.profile_cfg,
        execution_config=dbt.execution_cfg,
        operator_args={
            "vars": {"etl_date": ETL_Date},  # etl_date is a dbt variable
            "install_deps": True,  # install any necessary dependencies before running any dbt command
            "full_refresh": True,  # used only in dbt commands that support this flag
        },
    )

    _end = EmptyOperator(task_id="ETL-End", on_success_callback=success_callback)

    _start >> trigger_pos_airbyte_sync >> dbt_tasks >> _end
