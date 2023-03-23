import sqlite3
import io
import numpy as np
from App.utilities import *

class Database:    
    __DB_PATH = 'db.db'

    def adapt_array(cls, arr):
        """
        http://stackoverflow.com/a/31312102/190597 (SoulNibbler)
        """
        out = io.BytesIO()
        np.save(out, arr)
        out.seek(0)
        return sqlite3.Binary(out.read())

    def convert_array(text):
        out = io.BytesIO(text)
        out.seek(0)
        return np.load(out)

    sqlite3.register_adapter(np.ndarray, adapt_array)

    # Converts TEXT to np.array when selecting
    sqlite3.register_converter("array", convert_array)
    conn = sqlite3.connect(__DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = conn.cursor()

    @classmethod
    def fetch(cls, table, columns='*', conditions='',):
        condition_keys = ''
        condition_values = ()

        if columns != '*':
            columns = dynamic_columns(columns)
        if conditions != '':
            condition_keys = dynamic_where(conditions)
            condition_values = list(conditions.values())

        statment = f'SELECT {columns} FROM {table} {condition_keys}'
        print(statment)
        cls.cur.execute(statment, condition_values)

    @classmethod
    def fetch_all(cls, table, columns='*', conditions='',):
        cls.fetch(table, columns, conditions)
        rows = cls.cur.fetchall()
        
        if rows == []:
            return False

        return rows

    @classmethod
    def fetch_once(cls, table, columns='*', conditions=''):
        cls.fetch(table, columns, conditions)
        row = cls.cur.fetchone()
        print(row)
        if row == []:
            return False

        return row
    @classmethod
    def insert(self, table, values):
        values_temp = dynamic_values(values)
        statment = f"INSERT INTO {table} VALUES {values_temp}"
        try:
            self.cur.execute(statment, (values))
            self.conn.commit()
            return True
        except:
            return False

    @classmethod
    def update(self, table, set_diconary, where_diconary):
        set_values = list(set_diconary.values())
        set_keys = dynamic_set(set_diconary.keys())

        where_values = list(where_diconary.values())
        where_keys = dynamic_where(where_diconary.keys())

        statement = f'UPDATE {table} SET {set_keys} {where_keys}'
        self.cur.execute(statement,
                            (set_values + where_values))
        self.conn.commit()
