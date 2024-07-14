import os
from pathlib import Path
from cosmos import ProjectConfig, ProfileConfig, ExecutionConfig
from dotenv import load_dotenv

load_dotenv()

target_name = os.getenv("EDW_ENV")

# docker容器内的dbt项目路径
dbt_project_path = Path("/usr/local/airflow/dbt/edw")

# docker容器内的dbt命令路径
dbt_executable_path = Path("/usr/local/bin/dbt")

profiles_yml_path = '/'.join([str(dbt_project_path), "profiles.yml"])

project_cfg = ProjectConfig(dbt_project_path)
execution_cfg = ExecutionConfig(dbt_executable_path=str(dbt_executable_path))

profile_cfg = ProfileConfig(
    profile_name="default",
    target_name=target_name,
    profiles_yml_filepath=profiles_yml_path
)
