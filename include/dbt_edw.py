import os
from pathlib import Path
from cosmos import ProjectConfig, ProfileConfig, ExecutionConfig
from dotenv import load_dotenv

load_dotenv()

target_name = os.getenv('EDW_ENV')

dbt_project_path = Path("/usr/local/airflow/dbt/edw")
dbt_executable = Path("/usr/local/bin/dbt")

project_cfg = ProjectConfig(dbt_project_path)

execution_cfg = ExecutionConfig(dbt_executable_path=str(dbt_executable))

profile_cfg = ProfileConfig(
    profile_name="default",
    target_name=target_name,
    profiles_yml_filepath=dbt_project_path / "profiles.yml",
    )


