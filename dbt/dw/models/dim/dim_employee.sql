select
         f_gh                         as emp_id
        ,f_xm                         as emp_name
        ,f_xb_name                    as emp_sex
        ,f_gwmc_name                  as emp_position
        ,f_szzz_name                  as emp_dept
        ,f_gszt_name                  as emp_company
        ,substring(F_rzrq,1,10)       as hire_date
        ,F_splz                       as is_quit
        ,f_mrpb_name                  as work_schedule
        ,f_cph1                       as emp_car_no1
        ,f_cph2                       as emp_car_no2
        ,f_kqksrq                     as attend_start_date
        ,f_kqfs                       as attend_type_id
        ,f_kqfs_name                  as attend_type
        ,f_kqrl_name                  as attend_calendar
        ,to_char(now(),'yyyy-mm-dd hh24:mi:ss')  as DATA_LOAD_TIME
from {{ ref("ods_dhr_w_emp_info")}}