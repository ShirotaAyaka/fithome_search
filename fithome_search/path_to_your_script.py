import streamlit as st
import os
import sqlite3
import pandas as pd
import stat

# データベースファイルのパスを確認して権限を設定する関数
def check_and_set_permissions(db_path):
    if not os.path.exists(db_path):
        st.write(f"Database file does not exist at {db_path}")
        return False
    else:
        st.write(f"Database file found at {db_path}")
        
        # ファイルの権限を確認
        file_permissions = os.stat(db_path).st_mode
        st.write(f"File permissions: {oct(file_permissions)}")
        
        # 読み取り/書き込み権限を設定
        os.chmod(db_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP)
        st.write(f"Updated file permissions: {oct(os.stat(db_path).st_mode)}")
        return True

# SQLiteからデータを読み込む関数
def read_data_from_sqlite(db_path='property.db', query='SELECT * FROM SUUMOHOMES'):
    if not check_and_set_permissions(db_path):
        return pd.DataFrame()  # 空のDataFrameを返す

    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # データベース内のすべてのテーブルを表示
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = c.fetchall()
        st.write("Tables in the database:", tables)

        # テーブルの存在を確認
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='SUUMOHOMES';")
        table_exists = c.fetchone()
        if not table_exists:
            st.write("Table 'SUUMOHOMES' does not exist in the database.")
            conn.close()
            return pd.DataFrame()  # 空のDataFrameを返す

        c.execute(query)
        rows = c.fetchall()
        # SQLiteの結果をDataFrameに変換
        df = pd.DataFrame(rows, columns=[desc[0] for desc in c.description])
        conn.close()
        return df
    except sqlite3.OperationalError as e:
        st.write(f"OperationalError: {e}")
        return pd.DataFrame()  # 空のDataFrameを返す
    except Exception as e:
        st.write(f"Unexpected error: {e}")
        return pd.DataFrame()  # 空のDataFrameを返す

# メイン関数
def main():
    st.write("Current working directory:", os.getcwd())
    st.write("Files and directories in the current directory:", os.listdir('.'))
    data = read_data_from_sqlite()
    if not data.empty:
        # データの表示や処理をここで行う
        st.write(data)
    else:
        st.write("No data found or failed to read data from the database.")

if __name__ == "__main__":
    main()
