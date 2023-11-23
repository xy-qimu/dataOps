from pathlib import Path
from cosmos import ProjectConfig, ProfileConfig, ExecutionConfig

dbt_project_path = Path("/usr/local/airflow/dbt/dw")
dbt_executable = Path("/usr/local/airflow/dbt_venv/bin/dbt")

project_cfg = ProjectConfig(dbt_project_path)

execution_cfg = ExecutionConfig(dbt_executable_path=str(dbt_executable))

profile_cfg = ProfileConfig(
    profile_name="default",
    target_name="dev",
    profiles_yml_filepath=dbt_project_path / "profiles.yml",
    )


