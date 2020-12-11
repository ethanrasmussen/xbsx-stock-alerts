import requests
import json


def check_bb(url:str):
    r = requests.get(url,
                     headers={
                         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
                         'accept-language': 'en-US,en;q=0.9',
                         'accept-encoding': 'gzip, deflate, br',
                         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
                     },
                     data={'skuId': '6428324'})
    if 'Sold Out' in str(r.content):
        return False
    else:
        return True

def check_amzn(url:str):
    r = requests.get(url,
                     headers={
                         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                         'accept-encoding': 'gzip, deflate, br',
                         'accept-language': 'en-US,en;q=0.9',
                         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
                     })
    if 'Currently unavailable' in str(r.content):
        return False
    else:
        return True

def check_wm(url:str):
    r = requests.get(url,
                     headers={
                         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
                     })
    if 'Out of stock' in str(r.content) or 'unavailable' in str(r.content) or 'on backorder' in str(r.content):
        return False
    else:
        return True

def check_gs(url:str):
    r = requests.get(url,
                     headers={
                         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
                     })
    if 'Not Available' in str(r.content):
        return False
    else:
        return True

def check_tgt(url:str, zip):
    s = requests.Session()
    r1 = s.get(url, headers={
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
                     })
    api_key = str(r1.content).split('"apiKey":"')[1].split('"')[0]
    r2 = s.get(f'https://redsky.target.com/v3/stores/nearby/{zip}?key={api_key}&limit=1')
    location = json.loads(r2.text)[0]['locations'][0]['location_id']
    #
    tcin = url.split('/A-')[1]
    r3 = s.get(f'https://redsky.target.com/redsky_aggregations/v1/web/pdp_fulfillment_v1?key={api_key}&tcin={tcin}&store_id={location}&store_positions_store_id={location}&has_store_positions_store_id=true&scheduled_delivery_store_id={location}&pricing_store_id={location}&is_bot=false')
    product_info = json.loads(r3.text)
    #
    order_pickup, in_store, ship_to_store, delivery = True,True,True,True
    #
    try:
        if product_info['data']['product']['fulfillment']['store_options'][0]['order_pickup']['availability_status'] == 'OUT_OF_STOCK':
            order_pickup = False
    except:
        order_pickup = False
    try:
        if product_info['data']['product']['fulfillment']['store_options'][0]['in_store_only']['availability_status'] == 'OUT_OF_STOCK':
            in_store = False
    except:
        in_store = False
    try:
        if product_info['data']['product']['fulfillment']['store_options'][0]['ship_to_store']['availability_status'] == 'OUT_OF_STOCK' or product_info['data']['product']['fulfillment']['store_options'][0]['ship_to_store']['availability_status'] == 'UNAVAILABLE':
            ship_to_store = False
    except:
        ship_to_store = False
    try:
        if 'OUT_OF_STOCK' in str(product_info['data']['product']['fulfillment']).split('shipping_options')[1]:
            delivery = False
    except:
        delivery = False
    return [order_pickup, in_store, ship_to_store, delivery]
    

def check_ne(url:str):
    r = requests.get(url)
    if 'OUT OF STOCK' in str(r.content) and 'SOLD OUT' in str(r.content):
        return False
    else:
        return True