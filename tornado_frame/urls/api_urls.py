#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'
from service.orders.orders_main import Orders
from service.accounts.accounts_main import Accounts
from service.assets.assets_main import Assets
url_patterns = []

# 订单restapi
orders = [(r"/orders/post", Orders.post),(r"/orders/query", Orders.query)]
# 账号restapi
accounts = [(r"/accounts", Accounts)]
# 资产restapi
assets = [(r"/assets", Assets)]

url_patterns.extend(orders)
url_patterns.extend(accounts)
url_patterns.extend(assets)
url_map = dict(url_patterns)