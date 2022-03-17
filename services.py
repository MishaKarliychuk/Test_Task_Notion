import requests.sessions
import json
import datetime
from config import headers, type_days_dict

def get_needed_query(pages, update_count=False):
    # to_do_list, done_list = [], []
    done_list = []
    for page in list(pages):
        try:
            if page['properties']['Status']['select']['name'] == 'DONE':
                done_list.append(page)
                if update_count:
                    update_property_Count_done(page['id'], 0)
            # if page['properties']['Status']['select']['name'] == 'TO DO': to_do_list.append(page)
        except TypeError:
            continue
    # return to_do_list, done_list
    return done_list

def update_property_Count_done(pages_id, count):
    url = f"https://api.notion.com/v1/pages/{pages_id}"
    data = {
        "properties": {
            'Count_done': {'id': 'Ui%3F%7D', 'type': 'number', 'number': count}
        }
    }

    requests.request("PATCH", url, headers=headers, data=json.dumps(data))

def update_set_date(pages_id, date):
    url = f"https://api.notion.com/v1/pages/{pages_id}"

    data = {
        "properties": {
            'Set date': {'id': 'qqoh', 'type': 'date', 'date': {'start': str(date), 'end': None, 'time_zone': None}}
        }
    }

    requests.request("PATCH", url, headers=headers, data=json.dumps(data))

def update_due_date(pages_id, date):
    url = f"https://api.notion.com/v1/pages/{pages_id}"

    data = {
        "properties": {
            'Due Date': {'id': 'vb!%7B', 'type': 'date', 'date': {'start': str(date), 'end': None, 'time_zone': None}}
        }
    }

    requests.request("PATCH", url, headers=headers, data=json.dumps(data))
def get_periodicity_of_cart(periodicity_objs):
    periodicity_objs_list = []
    for periodicity_obj in periodicity_objs:
        periodicity_objs_list.append(periodicity_obj)
    return periodicity_objs_list

def get_cart_type_days_and_periodicity(cart_periodicity_list):
    cart_type_days = []
    for cart_periodicity_obj in cart_periodicity_list:
        if cart_periodicity_obj['name'] in type_days_dict.keys():
            cart_type_days.append(cart_periodicity_obj['name'])
        else:
            cart_periodicity = cart_periodicity_obj['name']
    return cart_type_days, cart_periodicity

def get_new_due_dates(today, due_date, cart_type_days, cart_periodicity, count_done, page_id):
    new_due_dates = []

    if cart_periodicity == 'Daily':
        new_due_dates.append(today+datetime.timedelta(1))
        return new_due_dates

    first_part, second_part = cart_periodicity.split("/")

    for cart_type_day in cart_type_days:

        if 'm' in second_part:

            if first_part == '2t' and second_part == 'm':
                if count_done >= 2 and due_date.month == today.month:
                    new_due_dates.append(new_due_dates)
                    return new_due_dates
                else:
                    from_day, to_day = 7, 14

                if due_date.month != today.month:
                    update_property_Count_done(page_id, 0)

            else:
                from_day, to_day = 7, 14
                if second_part == '2m':
                    if due_date + datetime.timedelta(30*2) > today:
                        new_due_dates.append(due_date)
                        return new_due_dates

                if second_part == '3m':
                    if due_date + datetime.timedelta(30*3) > today:
                        new_due_dates.append(due_date)
                        return new_due_dates

                else:
                    from_day, to_day = 7, 14

        else:
            from_day, to_day = 1, 8
            if second_part == '2w' and first_part == '1t':
                if due_date+datetime.timedelta(14) > today:
                    new_due_dates.append(due_date)
                    return new_due_dates


        for i in range(from_day, to_day):
            new_due_date = today + datetime.timedelta(i)
            if new_due_date.weekday() == type_days_dict[cart_type_day]:
                new_due_dates.append(new_due_date)
                break

    return new_due_dates

def move_cart_to_TODO(page_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    data = {
        "properties": {
            "Status": {
                "id": "eA%40u",
                "type": "select",
                "select": {
                    "id": "1",
                    "name":"TO DO",
                    "color":"blue"
                }
            },
        }
    }

    requests.request("PATCH", url, headers=headers, data=json.dumps(data))
