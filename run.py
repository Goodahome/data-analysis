import pandas as pd
import streamlit as st
import os
from PIL import Image
# import plotly.express as px
# from PIL import Image
from collections import Counter
 
if __name__ == '__main__':
    # 设置网页名称
    st.set_page_config(page_title='远程会诊数据', layout="wide")
    # 设置网页标题
    st.header('远程会诊中心数据分析平台')
    # 设置网页子标题
    # st.subheader('2023年远程会诊数据')

    tab1, tab2, tab3, tab4, tab5, tab6, tab7= st.tabs(["全年汇总数据", "每周数据", "单学科查询", 
    "多学科查询", "医院会诊查询", "医生收益核算", "申请科室汇总"])

    # # Streamlit 侧边栏
    # st.sidebar.title("侧边栏")

    # # 打开图像文件
    # image = Image.open(os.path.abspath('icon.png'))

    # # 使用st.image函数展示图像
    # st.image(image, caption='Sunrise by the mountains')

    # # 上传文件按钮
    # uploaded_file = st.sidebar.file_uploader("上传文件", type=["csv", "txt", "png"])

    # # 列表用于跟踪已上传的文件
    # uploaded_files = st.sidebar.empty()
    # uploaded_files_list = st.session_state.get('uploaded_files_list', [])

    # # 如果文件被上传
    # if uploaded_file is not None:
    #     # 将文件保存到执行目录
    #     with open(os.path.join(uploaded_file.name), "wb") as f:
    #         f.write(uploaded_file.read())
        
    #     # 记录已上传文件
    #     uploaded_files_list.append(uploaded_file.name)
    #     st.session_state.uploaded_files_list = uploaded_files_list

    #     st.sidebar.success(f"文件 '{uploaded_file.name}' 已上传到执行目录。")

    # # 显示已上传文件的记录
    # if uploaded_files_list:
    #     uploaded_files.header("已上传文件")
    #     for file_name in uploaded_files_list:
    #         uploaded_files.write(file_name)
    #         # 提供删除文件的按钮
    #         if st.sidebar.button(f"删除 {file_name}"):
    #             os.remove(file_name)
    #             uploaded_files_list.remove(file_name)
    #             st.session_state.uploaded_files_list = uploaded_files_list
    #             st.sidebar.success(f"文件 '{file_name}' 已删除。")
    
    
    # 打开图像文件
    image = Image.open(os.path.abspath('icon.png'))

    # 使用st.image函数展示图像
    st.sidebar.image(image, caption='XXX医院')
    # 设置侧边栏标题
    st.sidebar.header('文件选择')
    # 获取工作目录下所有的 '.xlsx' 文件
    xlsx_files = [file for file in os.listdir() if file.endswith('.xlsx')]

    # 在侧边栏上添加文件上传组件
    selected_file = st.sidebar.file_uploader('选择文件', type=['xlsx'])

    # 如果用户选择了文件，则读取数据
    if selected_file:
        df = pd.read_excel(selected_file, sheet_name = 0)
        # st.write('读取的数据:')
        # st.write(df)
    else:
        st.warning('请选择一个 Excel 文件进行读取。')
        st.stop() 

    # 读取数据
    # excel_file = os.path.abspath(uploaded_file.name)
    sheet_name = 'Sheet1'
    week_num_list = []
    names_zhi_list = []
    week_datas = pd.DataFrame()

    # df = pd.read_excel(excel_file, sheet_name = 0)
    df[['专家工号']] = df[['专家工号']].astype(str)
    df[['备注']] = df[['备注']].astype(str)

    def date(para):
        delta = pd.Timedelta(str(int(para))+'days')
        time = pd.to_datetime('1899-12-30')+ delta
        return time

    df['会诊时间'] = df['会诊时间'].apply(date)
    df['会诊时间'] = pd.to_datetime(df['会诊时间'])

    # 设置日期为索引
    data=df.set_index('会诊时间')
    df.head(10)


    # 将数据按日期分组
    df_sorted = df.iloc[1:].sort_values(by='会诊时间')
    for week_start, week_data in df_sorted.groupby(pd.Grouper(key='会诊时间', freq='W-Mon')):
        week_number = week_start.strftime('%Y%m%d')
        week_num_list.append(week_number)
    # st.dataframe(week_num_list, use_container_width=True, height=500)
    week_num_df = pd.DataFrame()
    #     week_datas = pd.concat([week_datas, pd.DataFrame({'week':[week_start], 'datas':[weekgroup.get_group('20230925')]})], ignore_index = False)
    week_num_df['会诊时间'] = week_num_list
    # st.write(week_num_df)
    weekgroup = df_sorted.groupby(pd.Grouper(key='会诊时间', freq='W-Mon'))

    # 按周筛选数据
    with tab2:
        dep_date = week_num_df['会诊时间'].unique().tolist()
        dep_date_selection = st.selectbox('会诊时间:',
                                            dep_date,
                                            index=0)
        mask1 = (weekgroup.get_group(dep_date_selection))

        number_of_dateweek = week_num_df['会诊时间'].shape[0]
        number_of_mask = mask1['会诊时间'].shape[0]

        st.dataframe(mask1, use_container_width=True, height=500)
        st.subheader('总的会诊周数有 {} 个周。'.format(number_of_dateweek), '所选周的会诊数有 {} 次。'.format(number_of_mask))


    # st.write('所选周的会诊数有 {} 次。'.format(number_of_mask))

    # 去掉时间只保留日期
    df['会诊时间'] = df['会诊时间'].apply(lambda x:x.strftime('%Y-%m-%d'))

    # 将数据转换成dataframe格式
    dfs = pd.DataFrame(df)

    # 显示医院所有会诊数量统计
    with tab1:
        number_of_data = df['会诊时间'].shape[0]
        st.dataframe(dfs, use_container_width=True, width=None, height=500)
        st.subheader('全年总的会诊数量有 {} 次。'.format(number_of_data))

    # 筛选出单学科的会诊
    with tab3:
        data = df[(df["学科"].str.contains("单学科", na=False))]
        number_of_datadan = data['会诊时间'].shape[0]
        # st.subheader('2023年单学科会诊数据')
        st.dataframe(data, use_container_width=True, height=500)
        st.subheader('全年总的单学科会诊数量有 {} 次。'.format(number_of_datadan))

    # 筛选多学科的会诊
    with tab4:
        data2 = df[(df["学科"].str.contains("多学科", na=False))]
        number_of_datadan = data2['会诊时间'].shape[0]
        # st.subheader('2023年多学科会诊数据')
        st.dataframe(data2, use_container_width=True, height=500)
        st.subheader('全年总的多学科会诊数量有 {} 次。'.format(number_of_datadan))

    # 根据选择过滤医院的会诊数据，勿删！！！！
    with tab5:
        department = df['申请医院'].unique().tolist()
        department_selection = st.multiselect('申请医院:',
                                            department,
                                            default=None)
        mask = (df['申请医院'].isin(department_selection))
        hos_result = df[mask].reset_index(drop=True)

        st.dataframe(hos_result, use_container_width=True, height=500)
        # 显示指定医院会诊数量统计
        number_of_result = df[mask].shape[0]
        st.subheader('{}的会诊数量有 {} 次。'.format(department_selection, number_of_result))

    # 医生收益汇总
    with tab6:
        
        # 单学科数据提取
        new_names = pd.DataFrame(columns=['会诊专家', '职称'])
        names = data['会诊专家'].unique().tolist()
        for value in names:
            result = df[df['会诊专家'] == value][['会诊专家', '职称']]
            new_names = new_names._append(result, ignore_index = True)
        # 去除行内容完全重复的项
        new_names = new_names.drop_duplicates()
        #统计专家的单学科会诊次数
        names_counts = df['会诊专家'].value_counts()
        new_names['会诊次数'] = new_names['会诊专家'].map(names_counts)
        # 添加 '收益' 列
        new_names['专家收益'] = new_names.apply(lambda row: row['会诊次数'] * 100 if row['职称'] == '主任医师' or row['职称'] == '正高' else row['会诊次数'] * 80, axis=1)
        # 处理索引列
        new_names = new_names.reset_index(drop=True)
        #####################################################################################
        # 判断是否有重复项及异常项
        异常项 = new_names[new_names.duplicated(subset=['会诊专家'], keep=False)]
        # 判断 '专家' 列中是否存在多个值的行
        多值异常 = new_names[new_names['会诊专家'].str.contains(' ')]
        # 追加多个值的行到 duplicate_experts 中
        异常项 = pd.concat([异常项, 多值异常])
        # 去除行内容完全重复的项
        异常项 = 异常项.drop_duplicates()
        异常项 = 异常项.reset_index(drop=True)
        st.markdown('请先检查数据异常的会诊')
        st.dataframe(异常项, use_container_width=True, height=500)
        #####################################################################################
        merged_df = pd.merge(new_names, 异常项, on=['会诊专家', '职称', '会诊次数', '专家收益'], how='outer', indicator=True)
        正常数据 = merged_df[merged_df['_merge'] == 'left_only'][new_names.columns]
        正常数据 = 正常数据.reset_index(drop=True)

        ##################################################################################################################
        
        #多学科数据提取
        combined_list = list(zip(df['会诊专家'],df['学科']))
        # 提取‘会诊专家’中单行存在多个值的数据到duo_df，拆分duo_df里每一个值到duo_list列表里面
        duo_df = df[df['会诊专家'].str.contains(' ')]
        duo_list = []
        # 
        for index, row in duo_df.iterrows():
            experts = row['会诊专家'].split()
            subjects = [row['学科']] * len(experts)  # 重复 '学科' 列的值以与 '会诊专家' 对应
    
            # 判断 '学科' 列的值是否为 "单学科"，如果不是则保留该行
            if "单学科" not in subjects:
                duo_list.extend(list(zip(experts, subjects)))

        # 判断duo_list里面每个值出现的次数到duo_list_counter并以多到少排序
        duo_list_counter = Counter(duo_list)
        duo_list_sorted = sorted(duo_list_counter.items(), key=lambda x: x[1], reverse=True)
        duo_df_split = pd.DataFrame()
        # 将会诊专家列存在多个值的数据拆分
        duo_df_split['会诊专家'] = duo_df['会诊专家'].str.split()
        
        #计算专家每次多会诊的收益
        duo_df_split['专家收益'] = 256 / duo_df_split['会诊专家'].apply(len)
        # 使用 explode 方法将列表中的专家名字排成一列
        duo_df_expanded = duo_df_split.explode(['会诊专家']).reset_index(drop=True)
        # 计算专家参与多学科会诊的次数
        多学科会诊次数 = duo_df_expanded['会诊专家'].value_counts()

        duo_df_expanded['多学科会诊次数']  = duo_df_expanded['会诊专家'].map(多学科会诊次数)
        
        # 将相同名字的 '专家收益' 相加
        result_df = duo_df_expanded.groupby('会诊专家')['专家收益'].sum().reset_index()

        # 将新增的'多学科会诊次数'加入到分组后的数据里面，因为新增的列不会进行分组
        result_df = result_df.merge(duo_df_expanded[['会诊专家', '多学科会诊次数']].drop_duplicates(), on='会诊专家')

        # 按照 '收益' 列的值从多到少排序
        result_df = result_df.sort_values(by='专家收益', ascending=False).reset_index(drop=True)
        

        ###########################################################################################################
        # 医生总核算
        # 将 '专家收益' 列的数据类型转换为整数
        正常数据['专家收益'] = 正常数据['专家收益'].astype(float)
        result_df['专家收益'] = result_df['专家收益'].astype(float)

        # 合并两个表，根据 '会诊专家' 列进行匹配
        merged_总核算 = pd.merge(正常数据, result_df, on=['会诊专家','专家收益'], how='outer', indicator=True)

        # 根据匹配结果，对相同 '会诊专家' 列的收益进行相加
        merged_总核算['专家收益'] = merged_总核算.groupby('会诊专家')['专家收益'].transform('sum')

        # 筛选出包含 '会诊专家' 列和 '收益' 列的新表
        总核算 = merged_总核算[['会诊专家', '专家收益']].drop_duplicates()
        # 判断是否有重复值
        # 总核算_重复 = 总核算[总核算.duplicated(subset=['会诊专家'], keep=False)]
        # st.dataframe(总核算_重复)
        # 将专家收益以多到少排序
        总核算 = 总核算.sort_values(by='专家收益', ascending=False).reset_index(drop=True)
        合计 = 总核算['专家收益'].sum()
        # 交换两列位置
        result_df[['专家收益', '多学科会诊次数']] = result_df[['多学科会诊次数', '专家收益']]
        ###########################################################################################################
        # 显示单学科收益结果
        st.subheader('单学科收益汇总')
        st.dataframe(正常数据, use_container_width=True, height=500)
        # 显示多学科收益结果
        st.subheader('多学科收益汇总')
        st.dataframe(result_df, use_container_width=True, height=500)
        st.subheader('单学科+多学科收益汇总')
        st.dataframe(总核算, use_container_width=True, height=500)
        st.subheader('本年度所有医生会诊总收入为{}'.format(合计))
        


    # # 多学科会诊医生收益
    # with tab7:
    #     st.write("nothing")


    with tab7:
        new_df = pd.DataFrame(columns=['申请科室'])
        new_list_keshi = []
        for index, row in df.iterrows():
            # 提取 '申请科室' 列的数据
            departments = row['申请科室'].split() if pd.notnull(row['申请科室']) else []
            new_list_keshi.extend(departments)
        # 计算每个值在 new_list_keshi 中出现的次数
        counter_dict = Counter(new_list_keshi)

        # 转换为 DataFrame
        df_counts = pd.DataFrame(list(counter_dict.items()), columns=['申请科室', '会诊次数'])
        df_counts_sorted = df_counts.sort_values(by='会诊次数', ascending=False)
        df_counts_sorted = df_counts_sorted.reset_index(drop=True) # drop=True重置索引时替换原有的，而不是新增一列
        st.dataframe(df_counts_sorted, use_container_width=True, height=500)

   

