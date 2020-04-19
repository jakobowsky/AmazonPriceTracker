def convert_price_toNumber(price, currency):
    price = price.split(currency)[1]
    try:
        price = price.split("\n")[0] + "." + price.split("\n")[1]
    except:
        Exception()
    try:
        price = price.split(",")[0] + price.split(",")[1]
    except:
        Exception()
    return float(price)