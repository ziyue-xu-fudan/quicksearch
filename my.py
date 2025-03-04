import streamlit as st
import pandas as pd

st.title("病史信息查看工具")

# 文件上传
uploaded_file = st.file_uploader("上传 Excel 文件", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.success(f"文件已上传，共 {len(df)} 行数据")

    # 多关键词筛选
    keywords = st.text_input("搜索关键词（多个关键词用空格分隔）")
    keyword_list = keywords.split() if keywords else []

    if keyword_list:
        filtered_df = df[df.apply(lambda row: all(row.astype(str).str.contains(k, case=False).any() for k in keyword_list), axis=1)]
    else:
        filtered_df = df

    # 筛选特定列
    columns = st.multiselect("选择筛选列", df.columns.tolist())
    if columns and keyword_list:
        filtered_df = filtered_df[filtered_df[columns].apply(lambda row: any(row.astype(str).str.contains(k, case=False).any() for k in keyword_list), axis=1)]

    # 翻页导航
    page_size = st.number_input("每页显示行数", min_value=1, max_value=100, value=10)
    total_pages = (len(filtered_df) - 1) // page_size + 1
    page = st.number_input("页码", min_value=1, max_value=total_pages, value=1)
    start_idx = (page - 1) * page_size
    end_idx = min(start_idx + page_size, len(filtered_df))

    st.write(f"显示第 {start_idx + 1} 到 {end_idx} 行，共 {len(filtered_df)} 行")
    st.dataframe(filtered_df.iloc[start_idx:end_idx])

    # 可选编辑功能
    if st.checkbox("启用编辑模式"):
        edited_df = st.data_editor(filtered_df.iloc[start_idx:end_idx], num_rows="dynamic")
        df.update(edited_df)
        st.success("修改已保存")

    # 导出修改后的文件
    if st.button("导出修改后的文件"):
        output_file = "modified_file.xlsx"
        df.to_excel(output_file, index=False)
        st.download_button("下载修改后的文件", data=open(output_file, "rb").read(), file_name=output_file, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        st.success("文件已导出")
