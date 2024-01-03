from plugins.wechat_operator import WechatOperator
from pendulum import timezone

local_tz = timezone("Asia/Shanghai")


def failure_callback(context):
    message = (
        '# <font color="warning">Airflow Task Failure Tips:</font>\n'
        "> ## DAG:  {}\n"
        "> ## Task:  {}\n"
        "**Finish Time:**  {}\n"
        "**Reason:** {}\n".format(
            context["task_instance"].dag_id,
            context["task_instance"].task_id,
            local_tz.convert(context["task_instance"].end_date).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            context["exception"],
        )
    )
    return WechatOperator(
        task_id="failure_callback",
        wechat_conn_id="conn_wechat",
        message_type="markdown",
        message=message,
        at_all=True,
    ).execute(context)


def success_callback(context):
    message = (
        '# <font color="info">Airflow Task Success Tips:</font>\n'
        "> ## DAG:  {}\n"
        "> ## Task:  {}\n"
        "**Finish Time:**  {}\n".format(
            context["task_instance"].dag_id,
            context["task_instance"].task_id,
            local_tz.convert(context["task_instance"].end_date).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        )
    )
    return WechatOperator(
        task_id="success_callback",
        wechat_conn_id="conn_wechat",
        message_type="markdown",
        message=message,
        at_all=True,
    ).execute(context)


def retry_callback(context):
    message = (
        '# <font color="comment">Airflow Task Retry Tips:</font>\n'
        "> ## DAG:  {}\n"
        "> ## Task:  {}\n"
        "> **Finish Time:**  {}\n"
        "**Reason:** {}\n".format(
            context["task_instance"].dag_id,
            context["task_instance"].task_id,
            local_tz.convert(context["task_instance"].end_date).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            context["exception"],
        )
    )
    return WechatOperator(
        task_id="retry_callback",
        wechat_conn_id="conn_wechat",
        message_type="markdown",
        message=message,
        at_all=True,
    ).execute(context)
