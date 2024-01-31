from IPython.display import Markdown, display
from llama_index import SQLDatabase, ServiceContext
import sqlite3
from llama_index.llms import OpenAI
from llama_index.indices.struct_store.sql_query import (
    SQLTableRetrieverQueryEngine,
)
from llama_index.objects import (
    SQLTableNodeMapping,
    ObjectIndex,
    SQLTableSchema,
)
from llama_index import VectorStoreIndex
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    select,
)
import os

db_dir = "files/db"
db_files = [os.path.join(db_dir, file) for file in os.listdir(db_dir) if file.endswith('.db')]

for db_file in db_files:
    engine = create_engine('sqlite:///' + db_file)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

    tables = cursor.fetchall()
    for table in tables:
        print(table[0])

    table_name = table[0]
    print(f"\nTable: {table_name} in {db_file}")
    metadata_obj = MetaData()
    print(metadata_obj)
    # Get table schema
    print("Schema:")
    cursor.execute(f"PRAGMA table_info({table_name});")
    schema = cursor.fetchall()
    for column in schema:
        print(column)

    # Get the first five rows
    # print("\nFirst 5 rows:")
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo")
    service_context = ServiceContext.from_defaults(llm=llm)
    sql_database = SQLDatabase(engine)
    # set Logging to DEBUG for more detailed outputs
    table_node_mapping = SQLTableNodeMapping(sql_database)
    table_schema_objs = [
        (SQLTableSchema(table_name=str(table_name)))
    ]  # add a SQLTableSchema for each table

    obj_index = ObjectIndex.from_objects(
        table_schema_objs,
        table_node_mapping,
        VectorStoreIndex,
    )
    query_engine = SQLTableRetrieverQueryEngine(
        sql_database, obj_index.as_retriever(similarity_top_k=3)
    )
    response = query_engine.query("How many different proteins with lymphoid tissue?")
    display(Markdown(f"<b>{response}</b>"))
    # Close the cursor and connection
    cursor.close()
    conn.close()
