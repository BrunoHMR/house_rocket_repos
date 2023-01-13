import pandas as pd
import numpy  as np
import streamlit as st
import plotly.express as px

np.set_printoptions(suppress=True)
pd.set_option('display.float_format', '{:.2f}'.format)
st.set_page_config(layout='wide')

st.title('House Rocket App')

@st.cache(allow_output_mutation=True)

def get_data(path):

    df = pd.read_csv(path)
    df = df.sort_values(by = 'date', ascending = False)
    df = df.drop_duplicates(subset=['id']).reset_index()
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

    return df

def create_new_attributes(df):

    df['year'] = df['date'].dt.year
    df['year_month'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m')
    df['water_view'] = df['waterfront'].apply(lambda x: 'no' if x == 0 else 'yes')
    df['condition_good'] = df['condition'].apply(lambda x: 'no' if x <= 3 else 'yes')
    df['renovated'] = df['yr_renovated'].apply(lambda x: 'no' if x == 0 else 'yes')

    return df

def create_season_column(df):

    df['month'] = df['date'].dt.month
    df['season'] = df['month'].apply(lambda x: 'Mar to May' if x >= 3 and x <= 5 else
    'Jun to Aug' if x >= 6 and x <= 8 else
    'Sep to Nov' if x >= 9 and x <= 11 else
    'Dec to Feb')

    return df

def create_selling_columns(df):

    df['selling_price'] = 'NA'
    for i, l in df.iterrows():
        if df.loc[i, 'price'] < df.loc[i, 'median_price']:
            df.loc[i, 'selling_price'] = df.loc[i, 'price'] * 1.3
        elif df.loc[i, 'price'] == df.loc[i, 'median_price']:
            df.loc[i, 'selling_price'] = df.loc[i, 'price'] * 1.2
        else:
            df.loc[i, 'selling_price'] = df.loc[i, 'price'] * 1.1

    df['selling_moment'] = 'NA'
    df.loc[df['median_price'] > df['price'], 'selling_moment'] = 'good'
    df.loc[df['median_price'] == df['price'], 'selling_moment'] = 'regular'
    df.loc[df['median_price'] < df['price'], 'selling_moment'] = 'bad'

    return df

# Non-Interactive Analysis:
def assumptions(df):

    st.header('Hypotheses')

    st.markdown('1. Waterfront houses are 30% more expensive, on average.')
    df1 = df[['water_view', 'price']].groupby(['water_view']).mean().reset_index()
    st.dataframe(df1)
    bv1 = (100 * df1.iloc[1, 1] / df1.iloc[0, 1]) - 100
    st.write(f'\nWaterfront houses are {round(bv1,2)}% more expensive, on average.\n')

    st.markdown('2. Houses younger than 1955 are 50% more expensive, on average.')
    df2 = df.copy()
    df2['younger_than_1955'] = df2['yr_built'].apply(lambda x: 'no' if x <= 1955 else 'yes')
    df2 = df2[['younger_than_1955', 'price']].groupby(['younger_than_1955']).mean().reset_index()
    st.dataframe(df2)
    bv2 = (100 * df2.iloc[1, 1] / df2.iloc[0, 1]) - 100
    st.write(f'\nHouses younger than 1955 are {round(bv2,2)}% more expensive, on average.\n')

    st.markdown('3. Houses with basement are 50% bigger, on average.')
    df['with_basement'] = df['sqft_basement'].apply(lambda x: 'no' if x == 0 else 'yes')
    df3 = df[['with_basement', 'sqft_living']].groupby(['with_basement']).mean().reset_index()
    st.dataframe(df3)
    bv3 = (100 * df3.iloc[1, 1] / df3.iloc[0, 1]) - 100
    st.write(f'\nHouses with basement are {round(bv3,2)}% bigger, on average.\n')

    st.markdown('4. The YoY price growth by year built are 10%:')
    df4 = create_cresciment_column(df, 'price', 'yr_built', 'YoY [%]')
    st.dataframe(df4)
    bv4 = df4.loc[:, 'YoY [%]'].mean()
    st.write(f'\nThe YoY price growth are {round(bv4,2)}%, on average.\n')

    st.markdown('5. Houses with 3 bathrooms have a 15% MoM price growth.')
    df5 = df.loc[df['bathrooms'] == 3, :]
    df5 = create_cresciment_column(df5, 'price', 'year_month', 'MoM [%]')
    st.dataframe(df5)
    bv5 = df5.loc[:, 'MoM [%]'].mean()
    st.write(f'\nHouses with 3 bathrooms have a {round(bv5,2)}% MoM price growth, on average.\n')

    st.markdown('6. In december houses are 25% more expensive than other months, on average:')
    df6 = df.copy()
    df6['month'].astype(int)
    df6['is_december'] = df6['month'].apply(lambda x: 'no' if x != 12 else 'yes')
    df6 = df6[['is_december', 'price']].groupby(['is_december']).mean().reset_index()
    st.dataframe(df6)
    bv6 = (100 * df6.iloc[1, 1] / df6.iloc[0, 1]) - 100
    st.write(f'\nIn december houses are {round(bv6,2)}% more expensive, on average.\n')

    st.markdown('7. Renovated houses are 50% more expensive, on average:')
    df7 = df[['renovated', 'price']].groupby(['renovated']).mean().reset_index()
    st.dataframe(df7)
    bv7 = (100 * df7.iloc[1, 1] / df7.iloc[0, 1]) - 100
    st.write(f'\nRenovated houses are {round(bv7,2)}% more expensives, on average.\n')

    st.markdown('8. Houses with basement are 40% more expensive, on average:')
    df8 = df[['with_basement', 'price']].groupby(['with_basement']).mean().reset_index()
    st.dataframe(df8)
    bv8 = (100 * df8.iloc[1, 1] / df8.iloc[0, 1]) - 100
    st.write(f'\nHouses with basement are {round(bv8,2)}% more expensive, on average.\n')

    st.markdown('9. Houses in good conditions are 10 years younger houses in bad conditions, on average:')
    df9 = df[['condition_good', 'yr_built']].groupby(['condition_good']).mean().reset_index()
    st.dataframe(df9)
    bv9 = df9.iloc[1, 1] - df9.iloc[0, 1]
    st.write(f'\nHouses in good conditions are {round(bv9,2)} years younger, on average.\n')

    st.markdown('10. Renovated houses have a MoM growth price 5% bigger than no renovated houses.')
    df10a = df.loc[df['renovated'] == 'no', :]
    df10b = df.loc[df['renovated'] == 'yes', :]
    df10a = create_cresciment_column(df10a, 'price', 'year_month', 'MoM [%]')
    df10b = create_cresciment_column(df10b, 'price', 'year_month', 'MoM [%]')
    c1, c2 = st.columns(2)
    c1.dataframe(df10a)
    c2.dataframe(df10b)
    bv10a = df10a.loc[:, 'MoM [%]'].mean()
    bv10b = df10b.loc[:, 'MoM [%]'].mean()
    c1.write(f'\nThe MoM growth price of no renovated houses are {round(bv10a,2)}%.\n')
    c2.write(f'\nThe MoM growth price of renovated houses are {round(bv10b,2)}%.\n')

    return None

def purchase_report(df):

    df1 = df[['zipcode', 'price']].groupby('zipcode').median().reset_index()

    df = df.loc[(df['water_view'] == 'yes') & (df['condition_good'] == 'yes')]

    df2 = pd.merge(df1, df, on='zipcode', how='inner')[['zipcode', 'price_x']].drop_duplicates(subset=['zipcode'])

    df = pd.merge(df, df2, on='zipcode', how='inner')[['id', 'date', 'zipcode', 'price', 'price_x']]
    df = df.rename(columns={"price_x": "median_price"})

    df_purchase = df[df['price'] < df['median_price']].sort_values(by='zipcode').reset_index()

    return df_purchase

def selling_report(df, df_purchase):

    df2 = df[['zipcode', 'season', 'price']].groupby(['zipcode', 'season']).median().reset_index()

    df = pd.merge(df2, df_purchase, on='zipcode', how='inner')[['zipcode', 'season', 'price_x']].drop_duplicates(
        subset=['zipcode', 'season'])

    df = pd.merge(df_purchase, df, on='zipcode', how='inner')[['id', 'date', 'zipcode', 'price', 'season', 'price_x']]
    df = df.rename(columns={"season": "median_season", "price_x": "median_price"})
    df = create_season_column(df)

    df_selling = create_selling_columns(df)[
        ['id', 'zipcode', 'season', 'price', 'median_season', 'median_price', 'selling_price', 'selling_moment']]

    return df_selling

def finance_result(df_purchase, df_selling):

    cost = df_purchase.loc[:,'price'].sum()
    revenue = df_selling.drop_duplicates(subset = ['id','selling_price'])
    revenue = revenue[revenue['selling_moment'] == 'good'].loc[:,'selling_price'].sum()
    profit = revenue - cost

    st.write(f'\nTotal purchase will cost US$ {round(cost,2)}.\n')
    st.write(f'Total sale will generate US$ {round(revenue, 2)}.\n')
    st.write(f'Total profit will be US$ {round(profit, 2)}.')

    return None

def show_non_interactive(df):

    with st.expander("Show non-interactive analysis"):

        hip = assumptions(df)
        c3, c4 = st.columns(2)
        df_purchase = purchase_report(df)
        c3.header('Purchase report')
        c3.dataframe(df_purchase)
        df_selling = selling_report(df, df_purchase)
        c4.header('Selling report')
        c4.dataframe(df_selling)
        fin = finance_result(df_purchase, df_selling)

    return None

# Interactive analysis:
def data_overview(df):

    st.header('Data Overview')

    st.sidebar.title('Data filters')
    select_columns = st.sidebar.multiselect('Enter columns', df.columns)
    select_zipcodes = st.sidebar.multiselect('Enter zipcode', df['zipcode'].unique())
    select_waterview = st.sidebar.multiselect('Is waterfront?', df['water_view'].unique())
    select_condition = st.sidebar.multiselect('Condition is good?', df['condition_good'].unique())

    if select_columns != [] and select_zipcodes != []:
        df = df.loc[df['zipcode'].isin(select_zipcodes), select_columns]
    if select_columns != [] and select_zipcodes == []:
        df = df.loc[:, select_columns]
    if select_columns == [] and select_zipcodes != []:
        df = df.loc[df['zipcode'].isin(select_zipcodes), :]
    if select_columns == [] and select_zipcodes == []:
        df = df.copy()

    if select_waterview != [] and select_condition == []:
        df = df.loc[(df['water_view'].isin(select_waterview)), :]
    if select_waterview == [] and select_condition != []:
        df = df.loc[(df['condition_good'].isin(select_condition)), :]
    if select_waterview != [] and select_condition != []:
        df = df.loc[(df['water_view'].isin(select_waterview)) & (df['condition_good'].isin(select_condition)), :]
    if select_waterview == [] and select_condition == []:
        df = df.copy()

    st.write(df)

    return df

def average_metrics(df):

    df1 = df[['id', 'zipcode']].groupby('zipcode').count().reset_index()
    df2 = df[['price', 'zipcode']].groupby('zipcode').mean().reset_index()

    df = pd.merge(df1, df2, on='zipcode', how='inner')
    df.columns = ['zipcode', 'total_ids', 'avg_price']

    return df

def create_map(df):

    houses = df[['id', 'zipcode', 'lat', 'long', 'price', 'water_view', 'condition_good']].copy()

    fig = px.scatter_mapbox(houses,
                            lat='lat',
                            lon='long',
                            color='zipcode',
                            size='price',
                            color_continuous_scale=px.colors.cyclical.IceFire,
                            size_max=15,
                            zoom=10)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(autosize=True, margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig

def filter_interactive(df, col1, col2):

    min_ = int(df[col1].min())
    max_ = int(df[col1].max())
    st.sidebar.subheader('Select max value')
    min_, max_ = st.sidebar.slider(f'{col1}', min_, max_, (min_, max_))

    df = df[[col1, col2]].groupby([col1]).mean().reset_index()
    df = df.loc[df[col1].between(min_, max_)]

    return df

def create_cresciment_column(df, mean_column, group_column, new_column, loc_col=None):

    if loc_col == 'bathrooms' or loc_col == 'renovated':
        select_col = st.sidebar.multiselect(f'Enter {loc_col}', df[loc_col].unique())
        df = df.loc[df[loc_col].isin(select_col), :]

    if loc_col == None:
        df = df.copy()

    df = df[[mean_column, group_column]].groupby([group_column]).mean().sort_values(by=group_column).reset_index()
    df[new_column] = 0

    for i, l in df.iterrows():
        if i < len(df) - 1:
            df.loc[i + 1, new_column] = ((df.loc[i + 1, mean_column]) / (df.loc[i, mean_column]) - 1) * 100

    return df

def plot_graph(df, col1, col2, col3):

    fig = px.line(df, x=col1, y=col2, title=f'Average {col2} per {col1} for filter {col3}')
    st.plotly_chart(fig, use_container_width=True)

    return fig

def show_interactive(df):

    with st.expander("Show interactive analysis"):

        df = data_overview(df)
        c5, c6 = st.columns(2)
        show_map = create_map(df)
        c5.header('Map Overview')
        c5.write(show_map)
        avg_met = average_metrics(df)
        c6.header('Average Metrics')
        c6.dataframe(avg_met)

        st.sidebar.title('Interactive graph filters')
        yr_built_interactive = filter_interactive(df, 'yr_built', 'price')
        month_interactive = filter_interactive(df, 'month', 'price')
        st.sidebar.title('Cresciment graph filters')
        yr_built_cresciment = create_cresciment_column(df, 'price', 'yr_built', 'YoY [%]')
        month_cresciment_bath = create_cresciment_column(df, 'price', 'year_month', 'MoM [%]', 'bathrooms')
        month_cresciment_ren = create_cresciment_column(df, 'price', 'year_month', 'MoM [%]', 'renovated')

        plot_yr_built = plot_graph(yr_built_interactive, 'yr_built', 'price', 'yr_built')
        plot_month = plot_graph(month_interactive, 'month', 'price', 'month')
        plot_yoy = plot_graph(yr_built_cresciment, 'yr_built', 'price', 'none')
        plot_mom_bath = plot_graph(month_cresciment_bath, 'year_month', 'price', 'bathrooms')
        plot_mom_ren = plot_graph(month_cresciment_ren, 'year_month', 'price', 'renovated')

        return None

def write_purchase(df):

    write_purchase = purchase_report(df)
    write_purchase.to_csv('csv\purchase_recommendations.csv')

    return write_purchase

def write_selling(df, df_purchase):

    write_selling = selling_report(df, df_purchase)
    write_selling.to_csv('csv\selling_recommendations.csv')

    return write_selling

# ETL:
if __name__ == "__main__":

    path = 'csv\kc_house_data.csv'
    df = get_data(path)

    df = create_new_attributes(df)
    df = create_season_column(df)
    non_interactive = show_non_interactive(df)
    interactive = show_interactive(df)

    csv_purchase = write_purchase(df)
    csv_selling = write_selling(df, purchase_report(df))