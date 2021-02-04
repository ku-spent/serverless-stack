"""
This script exists so that when developing or internal deployment of public commits
(to retail-demo-store-eu-west-1 and retail-demo-store-us-east-1 and retail-demo-store-us-west-2)
the new Personalize training files can be generated, picked up, and uploaded.

This script generates interactions for Amazon Personalize by heuristic simulation. It is based off the notebook
under workshop/01-Personalization where the logic is explained in more detail.
However, it has been improved in the following ways:
1. This script is deterministic; random seeds from RANDOM_SEED random variable below.
2. Logic exists for ensuring balance across categories.
3. Logic exists for ensuring balance across news.
4. Discount events are also generated according to 3 different types of users: discount-likers discount-indifferent,
    and price-sensitive-discount-likers.
Item 1 allows us to re-generate data during staging and item 2 and 3 helps recommendations look appropriate in
the final demo. If there is poor balance across news and categories then one may not get recommendations
for news in the same category. This is a hotfix for the logic whereby we generate profiles and probabilistically
sample news categories according to the sample user profile. Item 4 is necessary for training the discounts
personalizeation campaign.
"""
import json
import pandas as pd
import numpy as np
import time
import csv
from pathlib import Path
import gzip
import random
import yaml
import logging
from collections import defaultdict
import sys

# Keep things deterministic
RANDOM_SEED = 0

# Where to put the generated data so that it is picked up by stage.sh
GENERATED_DATA_ROOT = "data"

# Interactions will be generated between these dates
FIRST_TIMESTAMP = 1609459200  # 2021-01-01, 00:00:00
LAST_TIMESTAMP = 1611964800  # 2021-01-30, 00:00:00

# Users are set up with 3 news categories on their personas. If [0.6, 0.25, 0.15] it means
# 60% of the time they'll choose a news from the first category, etc.
CATEGORY_AFFINITY_PROBS = [0.6, 0.15, 0.10, 0.10, 0.05]

# After a news, there are this many news within the category that a user is likely to jump on next.
# The purpose of this is to keep recommendations focused within the category if there are too many news
# in a category, because at present the user profiles approach samples news from a category.
NEWS_AFFINITY_N = 4

# from 0 to 1. If 0 then news in busy categories get represented less. If 1 then all news same amount.
NORMALISE_PER_PRODUCT_WEIGHT = 1.0

# With this probability a news interaction will be with the news discounted
# Here we go the other way - what is the probability that a news that a user is already interacting
# with is discounted - depending on whether user likes discounts or not
# DISCOUNT_PROBABILITY = 0.2
# DISCOUNT_PROBABILITY_WITH_PREFERENCE = 0.5

IN_PRODUCTS_FILENAME = "rss-feed-3"
IN_USERS_FILENAME = "users.json.gz"

PROGRESS_MONITOR_SECONDS_UPDATE = 30

# This is where stage.sh will pick them up from
out_items_filename = f"{GENERATED_DATA_ROOT}/items.csv"
out_users_filename = f"{GENERATED_DATA_ROOT}/users.csv"
out_interactions_filename = f"{GENERATED_DATA_ROOT}/interactions.csv"

# The meaning of the below constants is described in the relevant notebook.

# Minimum number of interactions to generate
min_interactions = 6000
# min_interactions = 50000

# Percentages of each event type to generate
# view_news_percent = .07
news_liked_percent = .3
news_bookmarked_percent = .1
news_shared_percent = .02


def generate_user_items(out_users_filename, out_items_filename, in_users_filename, in_news_filename):

    Path(out_items_filename).parents[0].mkdir(parents=True, exist_ok=True)
    Path(out_users_filename).parents[0].mkdir(parents=True, exist_ok=True)

    # Product info is stored in the repository
    # with open(in_news_filename, 'r') as f:
    news = []
    for line in open(in_news_filename, 'r').readlines():
        parsed_line = json.loads(line)
        news.append(parsed_line['_source'])

    news_df = pd.DataFrame(news)

    # User info is stored in the repository - it was automatically generated
    with gzip.open(in_users_filename, 'r') as f:
        users = json.load(f)

    users_df = pd.DataFrame(users)

    news_dataset_df = news_df[['id', 'source', 'pubDate', 'url', 'image', 'title', 'summary', 'category', 'tags', 'raw_html_content']]
    news_dataset_df = news_dataset_df.rename(columns={'id': 'ITEM_ID', 'category': 'CATEGORY', 'tags': 'TAGS'})
    news_dataset_df = news_dataset_df[news_dataset_df['pubDate'] > '2021-01-15']
    news_dataset_df['TAGS'] = news_dataset_df['TAGS'].apply(lambda tags: '|'.join(tags))
    news_dataset_df = news_dataset_df[['ITEM_ID', 'CATEGORY', 'TAGS']]
    news_dataset_df.to_csv(out_items_filename, index=False)

    users_dataset_df = users_df[['id', 'age', 'gender']]
    users_dataset_df = users_dataset_df.rename(columns={'id': 'USER_ID', 'age': 'AGE', 'gender': 'GENDER'})

    users_dataset_df.to_csv(out_users_filename, index=False)

    return users_df, news_df


def generate_interactions(out_interactions_filename, users_df, news_df):
    """Generate items.csv, users.csv from users and news dataframes makes interactions.csv by simulating some
    shopping behaviour."""

    # Count of interactions generated for each event type
    news_viewed_count = 0
    news_bookmarked_count = 0
    news_liked_count = 0
    news_shared_count = 0

    Path(out_interactions_filename).parents[0].mkdir(parents=True, exist_ok=True)

    # ensure determinism
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    start_time_progress = int(time.time())
    next_timestamp = FIRST_TIMESTAMP
    seconds_increment = int((LAST_TIMESTAMP - FIRST_TIMESTAMP) / min_interactions)
    next_update_progress = start_time_progress + PROGRESS_MONITOR_SECONDS_UPDATE / 2

    if seconds_increment <= 0:
        raise AssertionError(f"Should never happen: {seconds_increment} <= 0")

    print('Minimum interactions to generate: {}'.format(min_interactions))
    print('Starting timestamp: {} ({})'.format(next_timestamp, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(next_timestamp))))
    print('Seconds increment: {}'.format(seconds_increment))

    print("Generating interactions... (this may take a few minutes)")
    interactions = 0

    subsets_cache = {}

    user_to_news = defaultdict(set)

    category_affinity_probs = np.array(CATEGORY_AFFINITY_PROBS)

    print("Writing interactions to: {}".format(out_interactions_filename))

    with open(out_interactions_filename, 'w') as outfile:
        f = csv.writer(outfile)
        f.writerow(["ITEM_ID", "USER_ID", "EVENT_TYPE", "TIMESTAMP"])

        category_frequencies = news_df.category.value_counts()
        category_frequencies /= sum(category_frequencies.values)

        interaction_news_counts = defaultdict(int)

        user_category_to_first_prod = {}
        news_affinities_bycat = {}

        all_categories = news_df.category.unique()
        for category in all_categories:
            news_cat = news_df.loc[news_df.category == category]
            news_cat = news_cat.id.values
            affinity_matrix = sum([np.roll(np.identity(len(news_cat)), [0, i], [0, 1]) for i in range(NEWS_AFFINITY_N)])
            np.random.shuffle(affinity_matrix)
            affinity_matrix = affinity_matrix.T
            np.random.shuffle(affinity_matrix)
            affinity_matrix = affinity_matrix.astype(bool)  # use as boolean index
            affinity_matrix = affinity_matrix | np.identity(len(news_cat), dtype=bool)

            news_infinities = [news_cat[row] for row in affinity_matrix]

            news_affinities_bycat[(category)] = {
                news_cat[i]: news_df.loc[news_df.id.isin(news_infinities[i])] for i in range(len(news_cat))
            }

        while interactions < min_interactions:
            if (time.time() > next_update_progress):
                rate = interactions / (time.time() - start_time_progress)
                to_go = (min_interactions - interactions) / rate
                print('Generated {} interactions so far (about {} seconds to go)'.format(interactions, int(to_go)))
                next_update_progress += PROGRESS_MONITOR_SECONDS_UPDATE

            user = users_df.loc[random.randint(0, users_df.shape[0] - 1)]

            # Determine category affinity from user's persona
            persona = user['persona']
            preferred_categories = persona.split('_')

            p = category_affinity_probs
            # p_normalised = (category_affinity_probs * category_frequencies[preferred_categories].values)
            # p_normalised /= p_normalised.sum()
            # p = NORMALISE_PER_PRODUCT_WEIGHT * p_normalised + (1 - NORMALISE_PER_PRODUCT_WEIGHT) * category_affinity_probs

            # Select category based on weighted preference of category order.
            category = np.random.choice(preferred_categories, 1, p=p)[0]

            # Here, in order to keep the number of products that are related to a product,
            # we restrict the size of the set of products that are recommended to an individual
            # user - in effect, the available subset for a particular category/gender
            # depends on the first product selected, which is selected as per previous logic
            # (looking at category affinities and gender)
            usercat_key = (user['id'], category)  # has this user already selected a "first" product?
            if usercat_key in user_category_to_first_prod:
                # If a first product is already selected, we use the product affinities for that product
                # To provide the list of products to select from
                first_prod = user_category_to_first_prod[usercat_key]
                news_subset_df = news_affinities_bycat[(category)][first_prod]
            else:
                # If the user has not yet selected a first product for this category
                # we do it according to the old logic of choosing between all products for gender
                # Check if subset data frame is already cached for category & gender
                news_subset_df = subsets_cache.get(category)
                if news_subset_df is None:
                    # Select products from selected category without gender affinity or that match user's gender
                    news_subset_df = news_df.loc[(news_df['category'] == category)].dropna()
                    # Update cache
                    subsets_cache[category] = news_subset_df

            # Pick a random product from gender filtered subset
            news = news_subset_df.sample().iloc[0]

            interaction_news_counts[news.id] += 1

            user_to_news[user['id']].add(news['id'])

            if usercat_key not in user_category_to_first_prod:
                user_category_to_first_prod[usercat_key] = news['id']

            # interaction_news_counts[news.id] += 1

            # user_to_news[user['id']].add(news['id'])
            this_timestamp = next_timestamp + random.randint(0, seconds_increment)
            next_timestamp += seconds_increment

            num_interaction_sets_to_insert = 1
            newsCount = list(interaction_news_counts.values())
            newsCount_max = max(newsCount) if len(newsCount) > 0 else 0
            newsCount_min = min(newsCount) if len(newsCount) > 0 else 0
            newsCount_avg = sum(newsCount) / len(newsCount) if len(newsCount) > 0 else 0
            if interaction_news_counts[news.id] * 2 < newsCount_max:
                num_interaction_sets_to_insert += 1
            if interaction_news_counts[news.id] < newsCount_avg:
                num_interaction_sets_to_insert += 1
            if interaction_news_counts[news.id] == newsCount_min:
                num_interaction_sets_to_insert += 1

            for _ in range(num_interaction_sets_to_insert):
                f.writerow([news['id'],
                            user['id'],
                            'news_viewed',
                            this_timestamp])
                next_timestamp += seconds_increment
                news_viewed_count += 1
                interactions += 1

                # if view news then like news
                if news_liked_count < int(news_viewed_count * news_liked_percent):
                    this_timestamp += random.randint(0, int(seconds_increment / 2))
                    f.writerow([news['id'],
                                user['id'],
                                'news_liked',
                                this_timestamp])
                    interactions += 1
                    news_liked_count += 1

                if news_bookmarked_count < int(news_viewed_count * news_bookmarked_percent):
                    this_timestamp += random.randint(0, int(seconds_increment / 2))
                    f.writerow([news['id'],
                                user['id'],
                                'news_bookmarked',
                                this_timestamp])
                    interactions += 1
                    news_bookmarked_count += 1

                if news_shared_count < int(news_viewed_count * news_shared_percent):
                    this_timestamp += random.randint(0, int(seconds_increment / 2))
                    f.writerow([news['id'],
                                user['id'],
                                'news_shared',
                                this_timestamp])
                    interactions += 1
                    news_shared_count += 1

    print("Interactions generation done.")
    print(f"Total interactions: {interactions}")
    print(f"Total news viewed: {news_viewed_count}")
    print(f"Total news liked: {news_liked_count}")
    print(f"Total news bookmarked: {news_bookmarked_count}")
    print(f"Total news shared: {news_shared_count}")

    globals().update(locals())   # This can be used for inspecting in console after script ran or if run with ipython.
    print('Generation script finished')


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    users_df, news_df = generate_user_items(out_users_filename, out_items_filename, IN_USERS_FILENAME, IN_PRODUCTS_FILENAME)
    generate_interactions(out_interactions_filename, users_df, news_df)
