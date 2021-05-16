### libraries for snowflake access
import os
import sys
project_home = '/Users/adityajoshi/git_repos/shopify_kaggle'
sys.path.append(project_home)
from utils import snowflake_connection as sc
from importlib import reload

### Computational libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

### Custom libraries
import queries as q

category_app_hist = sc.get_dataframe(q.categories_per_app_hist_query())
category_app_hist['CATEGORY_COUNT'] = pd.to_numeric(category_app_hist['CATEGORY_COUNT'])
category_app_hist['PERCENT_OF_APPS'] = pd.to_numeric(category_app_hist['PERCENT_OF_APPS'])

total_app_count = sc.get_dataframe(q.app_count_query())
app_count = max(total_app_count['APP_COUNT'])

total_reviewer_count = sc.get_dataframe(q.reviewer_count_query())
reviewer_count = max(total_reviewer_count['REVIEWER_COUNT'])

css = sc.get_dataframe(q.category_summary_stats_query())
css['Percent of Total Distinct Apps'] = css['APP_COUNT']/app_count
css_trunc = css[['CATEGORY_TITLE'
     ,'APP_COUNT'
     ,'MEDIAN_APP_RATING'
     ,'AVG_RATING_PER_APP'
     ,'MEDIAN_REVIEW_COUNT'
     ,'AVG_NO_REVIEWS_PER_APP'
     ,'Percent of Total Distinct Apps' ]].copy()


def load_category_app_hist():
    ax2 = category_app_hist.plot.bar(x='CATEGORY_COUNT', y='PERCENT_OF_APPS', rot=0)
    plt.xlabel('Number of Category Labels')
    plt.ylabel('Number of Apps')
    plt.title('Histogram of Apps by Number of Category Labels')
    plt.show()
    return

def print_app_and_reviewer_counts():

    print("Total distinct app count: {app_count} \nTotal distinct reviewer count: {reviewer_count}".format(
        app_count = app_count
        ,reviewer_count = reviewer_count
        ))
    return

def display_category_summary_stats():

    ax = css_trunc.plot.bar(x='CATEGORY_TITLE', y='Percent of Total Distinct Apps')
    plt.xlabel('Category titles')
    plt.ylabel('Percent of Apps')
    plt.title('Percent of Total Distinct Apps by Category')
    plt.xticks(rotation=30, ha='right')
    plt.show()

    display(css_trunc)
    return

def load_app_by_average_rating_hist(category=None):
    category_apps = sc.get_dataframe(q.app_rating_histogram_query(category=category))

    ax = pd.pivot_table(category_apps, values='APPL_ID', index = ['AVG_RATING_GROUPED']
                     ,aggfunc=np.count_nonzero).plot.bar()
    plt.xlabel('Average Rating Bucket')
    plt.ylabel('Number of Apps')
    plt.title('Number of ' + str(category) + ' Apps by Average Rating')
    plt.xticks(rotation=30, ha='right')
    plt.show()
    return
