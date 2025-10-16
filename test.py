import streamlit as st
import sqlite3 as sql
import pandas as pd
from datetime import datetime

conn = sql.connect('simple_bmi.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bmi_data(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    height REAL, 
    weight REAL, 
    bmi REAL,   
    record_time TEXT, 
    notes TEXT  
);
""")
conn.commit()

st.title("简易BMI数据库管理系统")

st.subheader("1. 添加BMI记录")
with st.form("add_form", clear_on_submit=True):
    height = st.number_input("身高(cm)", 50.0, 250.0, 175.0)
    weight = st.number_input("体重(kg)", 10.0, 250.0, 70.0)
    notes = st.text_input("备注")
    submit = st.form_submit_button("添加记录")

    if submit:
        height_m = height / 100
        bmi = round(weight / (height_m ** 2), 1)
        record_time = datetime.now().strftime("%Y-%m-%d %H:%M")

        cursor.execute("""
        INSERT INTO bmi_data(height, weight, bmi, record_time, notes)
        VALUES (?, ?, ?, ?, ?)
        """, (height_m, weight, bmi, record_time, notes))
        conn.commit()
        st.success("记录已添加！")

st.subheader("2. 查看所有记录")
cursor.execute("SELECT * FROM bmi_data ORDER BY record_time DESC")
data = cursor.fetchall()

if data:
    df = pd.DataFrame(data, columns=["ID", "身高(米)", "体重(kg)", "BMI", "记录时间", "备注"])
    st.dataframe(df, use_container_width=True)
else:
    st.info("暂无记录，请添加数据")

st.subheader("3. 更新记录")
with st.form("update_form"):
    update_id = st.number_input("要更新的记录ID", 1, value=1)
    # 新增更新身高的输入框
    new_height = st.number_input("新身高(米)", 0.5, 2.5, 1.75, step=0.01)
    new_weight = st.number_input("新体重(kg)", 10.0, 250.0, 70.0)
    new_notes = st.text_input("新备注")
    update_submit = st.form_submit_button("更新记录")

    if update_submit:
        # 先查询是否存在该ID的记录
        cursor.execute("SELECT * FROM bmi_data WHERE id = ?", (update_id,))
        result = cursor.fetchone()

        if result:
            # 使用新的身高和体重重新计算BMI
            new_bmi = round(new_weight / (new_height **2), 1)
            new_time = datetime.now().strftime("%Y-%m-%d %H:%M")

            # 更新语句中加入身高字段
            cursor.execute("""
            UPDATE bmi_data 
            SET height = ?, weight = ?, bmi = ?, record_time = ?, notes = ?
            WHERE id = ?
            """, (new_height, new_weight, new_bmi, new_time, new_notes, update_id))
            conn.commit()
            st.success(f"ID为{update_id}的记录已更新！新BMI值为: {new_bmi}")
        else:
            st.error("未找到该ID的记录")

st.subheader("4. 删除记录")
with st.form("delete_form"):
    delete_id = st.number_input("要删除的记录ID", 1, value=1, key="delete")
    delete_submit = st.form_submit_button("删除记录")

    if delete_submit:
        cursor.execute("DELETE FROM bmi_data WHERE id = ?", (delete_id,))
        conn.commit()

        if cursor.rowcount > 0:
            st.success(f"ID为{delete_id}的记录已删除！")
        else:
            st.error("未找到该ID的记录")

conn.close()
