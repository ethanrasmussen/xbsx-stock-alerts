import stock_check as sc
import text_handler as th
from urls import urls
import json, random, time

item_name = 'Xbox One Series X'


while True:
    with open('users.json', 'r') as fp:
        users = json.load(fp)

    # check all global/national/online stores (those that don't require zip code)
    best_buy = [sc.check_bb(urls['best_buy']), urls['best_buy']]
    amazon = [sc.check_amzn(urls['amazon']), urls['amazon']]
    newegg = [sc.check_ne(urls['newegg']), urls['newegg']]
    walmart = [sc.check_wm(urls['walmart']), urls['walmart']]
    gamestop = [sc.check_gs(urls['gamestop']), urls['gamestop']]
    global_stores = [best_buy, amazon, newegg, walmart, gamestop]
    print(f"Store stock check:\n{global_stores}")
    store_names = ['Best Buy', 'Amazon', 'Newegg', 'Walmart', 'Gamestop']
    index = 0
    for store in global_stores:
        if store[0] is True:
            text_msg = f"Good news! {item_name} appears to be in stock at {store_names[index]}. Here's the URL: {store[1]}"
            for user in users:
                th.send_text(th.create_phone_email(user, user['carrier']), 'Item in stock!', text_msg)
        index += 1

    # check target on a per-user basis (as it requires zip code)
    with open('users.json', 'r') as fp:
        users = json.load(fp)
    for user in users:
        if sc.check_tgt(urls['target'], user['zip']) is True:
            text_msg = f"Good news! {item_name} appears to be in stock at your local target. Here's the URL: {urls['target']}"
            th.send_text(th.create_phone_email(user, user['carrier']), 'Item in stock!', text_msg)

    # set random sleep time between 3min & 15min, to avoid spamming sites
    sleep = random.randint(180, 900)
    print(f"Completed round of store stock checks. Sleeping for {sleep} seconds...\n")
    time.sleep(sleep)