balance = {'usd': float(0)}

def get_price(symbol, source):
    if source == 'coingecko':
        return source.get_open_price(symbol)
    elif source == 'cmc':
        return source.get_opening_price(symbol)
    elif source == 'kraken':
        return source.get_opening_price(symbol, 'usd', 1, 1)
    return source.get_price(symbol)

def sell(source, symbol, amount, price=None):
    if not price:
        price = get_price(symbol, source)
    if amount > balance[symbol]:
        return False
    balance[symbol] -= amount
    balance['usd'] += amount * price
    return True

def buy(source, symbol, amount, price=None):
    if not price:
        price = get_price(symbol, source)
    desired_usd = amount * price
    if desired_usd > balance['usd']:
        return False
    balance[symbol] += float(amount)
    balance['usd'] -= desired_usd
    return True
    
def get_balance(symbol):
    return balance[symbol]

def set_balance(symbol, amount):
    balance[symbol] = amount
