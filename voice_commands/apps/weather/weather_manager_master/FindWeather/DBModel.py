from typing import List, Dict, Any

from pprint import pprint


import sqlite3


from sqlite3 import Error


import traceback


from . import config


from uuid import UUID








def dprint(*args, **kwargs):


    if config.sql_logs_enabled:


        print(*args, **kwargs)








def sqlite(func):


    def wrapper(self, *args, **kwargs):


        result = None


        try:


            connect = sqlite3.connect(config.db_name)


            cursor = connect.cursor()


            sql_list = []





            def execute(sql: str):


                dprint(f'Execute: "{sql}"')


                sql_list.append(sql)


                return cursor.execute(sql)





            result = func(self, execute, *args, **kwargs)


            connect.commit()


        except Error as e:


            dprint('-'*25, ' ERROR ', '-'*26)


            dprint(f'SQLite error: {" ".join(e.args)}')


            dprint(f'Exception class is: {e.__class__}')


            dprint(f'SQL Request is: "{sql_list.pop()}"')


            dprint(f'\nTraceback: {traceback.format_exc()}')


            dprint('-'*60)


        except Exception as e:


            dprint('-'*23, ' EXCEPTION ', '-'*24)


            dprint(f'Exception args: {" ".join(e.args)}')


            dprint(f'Exception class is {e.__class__}')


            dprint(f'\nTraceback: {traceback.format_exc()}')


            dprint('-'*60)


        finally:


            connect.close()


            return result





    return wrapper








class DBModel:





    table_name: str


    columns: List[str]





    @sqlite


    def __init__(self, execute, table_name: str, columns: Dict[str, str] = []):


        self.table_name = table_name


        if not execute(f'select * from sqlite_master WHERE type = "table" AND name = "{self.table_name}"').fetchall():


            if columns:


                columns_types = ', '.join([f'{name} {args}' for name, args in columns.items()])


                execute(f'create table if not exists {self.table_name}(id blob primary key, {columns_types})')


                self.columns = ['id', *columns.keys()]


        else:


            self.columns = [properties[1] for properties in execute(f'pragma table_info({self.table_name})').fetchall()]





    @sqlite


    def all(self, execute) -> Dict[str, Any]:


        rows = execute(f'select * from {self.table_name}').fetchall()


        data = []


        for row in rows:


            dict = {}


            for i, value in enumerate(row):


                dict[self.columns[i]] = value


            data.append(dict)


        return data





    def count(self) -> int:


        return len(self.all())





    @sqlite


    def where(self, execute, condition: str) -> List[Any]:


        return execute(f'select * from {self.table_name} where {condition}')





    @sqlite


    def update(self, execute, values: Dict[str, Any], where: str):


        updates = " ".join([f'{key} = "{value}"' for key, value in values.items()])


        execute(f'update {self.table_name} set {updates} where {where}')





    @sqlite


    def insert(self, execute, dict: Dict[str, Any]):


        values = [f'"{v}"' for v in dict.values()]


        execute(f'insert into {self.table_name}({", ".join(dict.keys())}) values({", ".join(values)})')





    @sqlite


    def drop(self, execute):


        execute(f'drop table if exists {self.table_name}')





    @sqlite


    def alter(self, execute, to: 'DBModel', foreignKey: str, onDelete: str, onUpdate: str):


        execute(f'alter table {self.table_name} add foreign key ({foreignKey}) references {to.table_name}(id) on delete {onDelete} on update {onUpdate}')