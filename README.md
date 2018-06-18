# medscrawler

## 目录结构
    .
    ├── medscrawler
    │   ├── __init__.py
    │   ├── const.py        # 常量
    │   ├── handler         # 将 JSON 格式数据导入 RDBMS, (通过每个文件内的 `import_from_file()` 方法)
    │   │   ├── cure.py
    │   │   ├── disease.py
    │   │   └── medicine.py
    │   ├── kbqa            # 问答系统
    │   │   ├── __init__.py
    │   │   ├── parse.py    # 将自然语言问题转化为 SPARQL 模板
    │   │   ├── rules.py    # 问题模板
    │   │   └── words.py    # 单词匹配规则
    │   ├── models          # RDBMS 表结构对应的ORM模型
    │   │   ├── __init__.py
    │   │   ├── cure.py
    │   │   ├── department.py
    │   │   ├── disease.py
    │   │   ├── disease_alias.py
    │   │   ├── disease_complication.py
    │   │   ├── disease_department.py
    │   │   ├── disease_examination.py
    │   │   ├── disease_postition.py
    │   │   ├── disease_surgery.py
    │   │   ├── disease_symptiom.py
    │   │   ├── entity.py
    │   │   ├── examination.py
    │   │   ├── medicine.py
    │   │   ├── postion.py
    │   │   ├── surgery.py
    │   │   └── symptom.py
    │   ├── server.py       # 简单的 Web 服务器
    │   ├── spiders         # 爬虫，每个文件对应不同类型数据
    │   │   ├── __init__.py
    │   │   ├── disease.py
    │   │   ├── disease_detail.py
    │   │   ├── disease_info.py
    │   │   └── meds_info.py
    │   ├── items.py
    │   ├── pipelines.py
    │   ├── middlewares.py
    │   ├── settings.py
    │   └── utils
    │       ├── func.py
    │       ├── sparql.py
    │       └── str.py
    ├── rdf
    │   ├── config.ttl      # Fuseki 配置 (对应下文　`ConfigFile`)
    │   ├── kg.nt           # N-Triples 格式的 RDF 数据
    │   ├── kg.ttl          # RDBMS到rdf映射
    │   ├── ontology.ttl    # 本体定义
    │   └── rules.ttl
    ├── requirements.txt
    ├── scrapy.cfg
    ├── static              # KBQA网页静态内容
    │   ├── index.html
    │   └── index.js
    ├── tdb
    ├── db_backup.sql       # 数据库备份
    ├── disease.json        # 爬取的　科室－疾病－疾病页　数据
    ├── disease_detail.jl   # 爬取的　疾病－药品　数据
    ├── disease_info.jl     # 爬取的　疾病详情　数据
    ├── meds_dict.txt       # 疾病词典，用于分词
    ├── meds_info.jl        # 爬取的　药品说明书　数据
    ├── config.py           # 项目配置文件
    
    

## SPARQL 端点启动

`fuseki-server --config=ConfigFile` (本项目 `ConfigFile` 为 `medscrawler/rdf/config.ttl`)

## Web 服务启动

`hug -f medscrawler/server.py`
