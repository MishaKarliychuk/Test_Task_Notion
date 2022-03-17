import requests

from services import get_needed_query, get_periodicity_of_cart, get_cart_type_days_and_periodicity, get_new_due_dates, move_cart_to_TODO, update_due_date, update_set_date
from config import DATABASE_ID, headers
import datetime
import schedule

def main():
    today = datetime.datetime.now().date()

    # достаем все записи с TO_DO и DONE
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    pages = requests.post(url, headers=headers).json()['results']
    done_list = get_needed_query(pages)
    if done_list[0]['properties'].get('Count_done') == None or done_list[0]['properties'].get('Count_done').get('number') == None:
        pages = requests.post(url, headers=headers).json()['results']
        done_list = get_needed_query(pages, update_count=True)

    for cart in done_list:
        # Set Date
        cart_set_date = cart['properties']['Set date']['date']['start'].split('-')
        cart_set_date = datetime.date(int(cart_set_date[0]), int(cart_set_date[1]), int(cart_set_date[2]))

        if cart_set_date > today:
            continue

        elif cart_set_date < today:
            # Due Date
            cart_due_date = cart['properties']['Due Date']['date']['start'].split('-')
            cart_due_date = datetime.date(int(cart_due_date[0]), int(cart_due_date[1]), int(cart_due_date[2]))

            # Type_days & Periodicity
            cart_periodicity_list = get_periodicity_of_cart(cart['properties']['Periodicity']['multi_select'])
            cart_type_days, cart_periodicity = get_cart_type_days_and_periodicity(cart_periodicity_list)  # [Mon] & 1t/w

            # Формируем новые Due Date
            new_due_dates = get_new_due_dates(today, cart_set_date, cart_type_days, cart_periodicity,
                                              cart['properties']['Count_done']['number'], cart['id'])
            new_due_dates.sort()
            new_due_date = new_due_dates[0]

            # Считаем Set date
            if cart_periodicity == 'Daily':
                new_set_date = new_due_date
            elif '/w' in cart_periodicity:
                new_set_date = new_due_date - datetime.timedelta(1)
            elif '/2w' in cart_periodicity:
                new_set_date = new_due_date - datetime.timedelta(1)
            elif '/m' in cart_periodicity:
                new_set_date = new_due_date - datetime.timedelta(7 * 1)
            elif '/2m' in cart_periodicity or '/3m' in cart_periodicity:
                new_set_date = new_due_date - datetime.timedelta(7 * 2)
            else:
                raise ValueError(f"Неверное значение в cart_periodicity: {cart_periodicity}")

            # print(cart_periodicity, '    ', *cart_type_days, '   ', new_due_date, '   ', new_set_date)

            update_set_date(cart['id'], new_set_date)
            update_due_date(cart['id'], new_due_date)


        elif cart_set_date == today:
            move_cart_to_TODO(cart['id'])

while(True):
    main()
    a = schedule.every(1).days.do(main)
    schedule.run_pending()