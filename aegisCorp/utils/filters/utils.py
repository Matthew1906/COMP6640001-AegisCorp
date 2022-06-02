def currency(price:int):
    price_str = str(price)
    prefix_index = len(price_str)%3 if len(price_str)%3!=0 else 3
    prefix = price_str[:prefix_index]
    suffix = price_str[prefix_index:]
    return 'Rp' + prefix +''.join(["." + suffix[i*3:3*i+3] for i in range(len(price_str)//3) if suffix[i*3:i*3+3]!='']) + ',00'

def format_id(id):
    count = len(str(id))
    return "0"*(3-count) + str(id)

def format_date(date):
    return date.strftime("%d/%m/%Y")