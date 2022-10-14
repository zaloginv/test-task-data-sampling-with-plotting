import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import pandas as pd

df = pd.read_csv('result_data/res_data.csv')
min_count = df['count'].min()
uniqs = df['area'].unique()

for uniq in uniqs:
    area_df = df.loc[df['area'] == uniq]
    clusters_names = list(df['cluster_name'].unique())
    fig, ax = plt.subplots(figsize=(15, 15))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
    clusters_in_area = []
    for _, data in area_df.iterrows():
        x = data['x']
        y = data['y']
        c = data['color']
        cluster = data['cluster_name']
        size = float(data['count'])

        if cluster not in clusters_in_area:
            scatter = ax.scatter(x=x, y=y, c=c, label=data['cluster_name'], s=min_count)
            clusters_in_area.append(cluster)

        scatter = ax.scatter(x=x, y=y, c='black', s=size)
        scatter = ax.scatter(x=x, y=y, c=c, s=size - size / 4)
        keyword = data['keyword']

        if len(keyword) > 15:
            keyword = keyword.replace(' ', '\n')
        ax.text(x=x + 0.5, y=y, s=keyword)

    plt.legend(title='Кластеры', loc=0)
    plt.title(f'График области {uniq}')
    plt.xlabel("Ось X")
    plt.ylabel("Ось Y")
    if uniq == 'ar\\vr':
        uniq = 'arvr'
    plt.savefig(f'result_images/{uniq}.png')
