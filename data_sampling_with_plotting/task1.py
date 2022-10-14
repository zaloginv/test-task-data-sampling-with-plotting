import pandas as pd
import numpy as np
import openpyxl as px

COLORS = ['#17becf', '#bcbd22', '#7f7f7f', '#e377c2', '#8c564b', '#9467bd', '#d62728', '#2ca02c', '#ff7f0e', '#1f77b4']

tz_data = pd.read_csv('initial_data/tz_data.csv')
rework_data = tz_data[['area', 'cluster', 'cluster_name', 'keyword', 'x', 'y', 'count']]

res_data = pd.DataFrame(columns=['area', 'cluster', 'cluster_name', 'keyword', 'x', 'y', 'count', 'color'])

areas = {}

for _, data in rework_data.iterrows():
    checker = True

    # проверка на непустые ячейки
    for item in data:
        if item in [None, np.nan, 'N/A', '', '-', 'N\\A']:
            checker = False

    # словарь
    area = data['area']
    if area not in areas:
        areas[area] = {'keywords': [], 'cluster_colors': {}}

    # проверка на повтор слов/словосочетаний
    keyword = data['keyword']
    if keyword not in areas[area]['keywords']:
        areas[area]['keywords'].append(keyword)
    else:
        checker = False

    # для распределения цветов в области -> в кластеры
    # на случай, если одинаковые кластеры в разных областях нужно будет окрасить в разные цвета
    try:
        cluster = int(data['cluster'])
    except:
        pass
    if cluster not in areas[area]:
        areas[area]['cluster_colors'][cluster] = COLORS[cluster]
        color = areas[area]['cluster_colors'][cluster]

    # запись данных в строку
    if checker:
        res_data.loc[len(res_data.index)] = [
            area, cluster, data['cluster_name'], keyword, data['x'], data['y'], data['count'], color
        ]

res_data = res_data.sort_values(['area', 'cluster', 'cluster_name', 'count'], ascending=[True, True, True, False])


def saving_result(variant=1):
    if variant == 1:
        res_data.to_csv(index=False, path_or_buf='result_data/res_data.csv')
    else:
        res_data.to_excel(excel_writer='result_data/res_data.xlsx', index=False, sheet_name='sheet')

        wb = px.load_workbook('result_data/res_data.xlsx')
        ws = wb.active
        ws.auto_filter.ref = ws.dimensions
        ws.freeze_panes = 'I2'
        ws.column_dimensions['A'].width = 14
        ws.column_dimensions['C'].width = 15
        ws.column_dimensions['D'].width = 40
        ws.column_dimensions['E'].width = 21
        ws.column_dimensions['F'].width = 22
        wb.save('result_data/res_data_processed.xlsx')


saving_result(variant=2)
