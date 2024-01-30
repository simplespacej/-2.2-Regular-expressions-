from pprint import pprint
import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
pprint(contacts_list)


def standardize_name(contact):
    full_name = " ".join(contact[:3]).split()
    return full_name + [None] * (3 - len(full_name))


def format_phone_number(phone):
    phone = re.sub(r"[^\d]", "", phone)
    pattern = r"(\d)?(\d{3})(\d{3})(\d{2})(\d{2})(\d*)"
    replacement = r"+7(\2)\3-\4-\5"
    if phone.startswith("8"):
        phone = "7" + phone[1:]
    formatted_phone = re.sub(pattern, replacement, phone)
    if re.search(r"\d{4}$", formatted_phone):
        formatted_phone = re.sub(r"(\d{4})$", r" доб.\1", formatted_phone)
    return formatted_phone


processed_contacts = {}
for contact in contacts_list[1:]:
    full_name = standardize_name(contact)
    key = tuple(full_name[:2])

    if key not in processed_contacts:
        processed_contacts[key] = full_name + contact[3:]
    else:
        for i in range(3, 7):
            processed_contacts[key][i] = processed_contacts[key][i] or contact[i]


    if processed_contacts[key][5]:
        processed_contacts[key][5] = format_phone_number(processed_contacts[key][5])


final_contacts_list = [contacts_list[0]] + [value for key, value in processed_contacts.items()]


with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(final_contacts_list)
