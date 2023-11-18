select
         f_gh
        ,f_xm
        ,f_xb_name
        ,f_gwmc_name
        ,f_szzz_name
        ,f_gszt_name
        ,f_rzrq
        ,f_splz
        ,f_mrpb_name
        ,f_cph1
        ,f_cph2
        ,f_kqksrq
        ,f_kqfs
        ,f_kqfs_name
        ,f_kqrl_name
        ,to_char(now(),'yyyy-mm-dd hh24:mi:ss')  as DATA_LOAD_TIME
from stg.stg_dhr_w_emp_info
