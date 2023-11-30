Overview
========

本项目的定位是通过研发一套成熟稳定的现代数据仓库平台，并构建自动化的数据更新管道，为公司的各项生产经营活动提供高质量的数据支撑，从而达到降本增效的目标。

涉及的业务模块：采购、销售、生产、库存及财务等

涉及的业务系统：SAP、POS及CRM等

<font color=red size=5>项目亮点：</font> 
通过落地DataOps，提升了数据团队的开发运维效率，从而更好地为业务提供更高质量更稳定的数据服务。
1) 数据团队只需在<font color=green>本地的IDE环境</font>进行工作，通过git和jenkins实现版本管理及持续集成交付
2) 数据团队<font color=green>不再</font>需要手工配置调度依赖和数据血缘关系（可自动感知生成）
3) <font color=green>自动生成</font>数据字典文档及代码单元测试

Project Contents
================

### <font color=red>1、数据架构：</font>stg + ods + dim + dwd +dws + ads

![img.png](res/img1.png)

### <font color=red>2、技术架构：</font>airbyte + dbt + airflow + cosmos + astro + postgresql + git + jenkins 

        1) airbyte: 开源的数据同步工具。与各种数据源对接，通过简单配置即可实现数据入仓。即EL工作
        2) dbt:     开源的数据转换工具。针对仓内的数据进行清洗转换等处理，并可自动生成文档及单元测试。即T工作
        3) airflow: 开源的任务调度工具。用于编排调度数据管道任务
        4) cosmos:  开源的python软件包。用于airflow和dbt的集成对接，通过该框架可自动识别dbt模型的血缘信息，无需再手工配置airflow调度任务依赖
        5) astro:   该开源工具通过docker容器自动创建管理airflow实例，让数据团队无需花太多精力在airflow实例的管理上，更专注在数据管道的设计和维护
        6) postgresql: 开源关系数据库。用于存储和计算加工仓库数据
        7) git:     代码版本控制
        8) jenkins: CICD平台
        

### <font color=red>3、项目部署流程：</font>     
(部署前请先在本地安装：<font color=red>python / docker / astro</font>    [详见安装部署记录](./安装部署记录.md))  
1）从GitHub上pull项目到本地  
2）在本地项目根目录上创建虚拟环境dbt_venv,并安装项目依赖：<font color=red>pip install -r requirements.txt</font>   
3）如部署到生产环境，修改.env文件内容：<font color=red>DW_ENV=prod</font>     
4）启动项目： <font color=red>astro dev start</font>  [--env .env]  (默认的.env文件，可不用加 --env指定环境变量文件)
