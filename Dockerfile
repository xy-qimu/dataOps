FROM quay.io/astronomer/astro-runtime:9.4.0

# install dbt into a virtual environment
# replace dbt-postgres with the adapter you need

RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir dbt-postgres &&  deactivate
	
RUN pip install apache-airflow-providers-airbyte[http] && \
	pip install apache-airflow-providers-airbyte  