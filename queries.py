def categories_per_app_hist_query():
    return """
with
categories_per_app as (
select
    apps.id as appl_id
    ,count(distinct category_mapping.category_id) as category_count

from shopify.apps as apps
    join shopify.apps_categories as category_mapping
        on apps.id = category_mapping.app_id

group by
    apps.id
)
select
    categories_per_app.category_count
    ,count(distinct categories_per_app.appl_id) as app_count
    ,app_count/4750 as percent_of_apps

from categories_per_app

group by
    categories_per_app.category_count

order by
    categories_per_app.category_count asc
"""

def app_count_query():
    return """
select
    count(distinct apps.id) as app_count
from shopify.apps as apps
"""

def reviewer_count_query():
    return """
select
    count(distinct reviews.author) as reviewer_count
from shopify.reviews_trunc as reviews
"""

def category_summary_stats_query():
    return """
select
    categories.title as category_title
    ,count(distinct apps.id) as app_count

    -- ratings
    ,sum(apps.rating) as summed_app_ratings
    ,median(apps.rating) as median_app_rating
    ,summed_app_ratings/app_count as avg_rating_per_app

    -- reviews
    ,sum(apps.reviews_count) as total_reviews_count
    ,median(apps.reviews_count) as median_review_count
    ,total_reviews_count/app_count as avg_no_reviews_per_app

from shopify.apps as apps
    join shopify.apps_categories as category_map
        on apps.id = category_map.app_id

    join shopify.categories as categories
        on category_map.category_id = categories.id

group by
    category_title

order by
    app_count desc
"""

def app_rating_histogram_query(category=None):
    if category is None: return
    return """
select

    apps.id as appl_id
    ,max(apps.rating) as avg_rating
    ,(case
        when avg_rating = 0 then '0'
        when avg_rating < 0.5 then '< 0.5'
        when avg_rating < 1 then '0.5 - 1'
        when avg_rating < 1.5 then '1 - 1.5'
        when avg_rating < 2 then '1.5 - 2'
        when avg_rating < 2.5 then '2 - 2.5'
        when avg_rating < 3 then '2.5 - 3'
        when avg_rating < 3.5 then '3 - 3.5'
        when avg_rating < 4 then '3.5 - 4'
        when avg_rating < 4.5 then '4 - 4.5'
        else '4.5 - 5'
      end) as avg_rating_grouped

from shopify.apps as apps
    join shopify.apps_categories as category_map
        on apps.id = category_map.app_id

    join shopify.categories as categories
        on category_map.category_id = categories.id

where 1=1
    and categories.title = 'Finances'

group by
    apps.id

order by avg_rating desc

""".format(category_label = category)
