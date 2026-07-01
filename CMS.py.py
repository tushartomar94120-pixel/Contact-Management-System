"""
=========================================================
        CONTACT MANAGEMENT SYSTEM
=========================================================
Features:
✔ Add Contact
✔ Search Contact (Partial Name Match)
✔ Search by Phone Number
✔ Update Contact
✔ Delete Contact
✔ Display All Contacts
✔ Save Contacts to JSON
✔ Load Contacts Automatically
✔ Backup Contacts
✔ Export to CSV
✔ Contact Categories
✔ Statistics
✔ Input Validation
=========================================================
"""

import json
import csv
import os
import re
from datetime import datetime

DATA_FILE = "contacts.json"
BACKUP_FILE = "contacts_backup.json"


# ======================================================
# Validation Functions
# ======================================================

def validate_name(name):
    name = name.strip().title()

    if len(name) < 2:
        return False, "Name must contain at least 2 characters."

    if not all(char.isalpha() or char.isspace() for char in name):
        return False, "Name should contain only letters and spaces."

    return True, name


def validate_phone(phone):
    phone = phone.strip()

    if re.fullmatch(r"\d{10}", phone):
        return True, phone

    return False, "Phone number must contain exactly 10 digits."


def validate_email(email):
    email = email.strip().lower()

    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if re.fullmatch(pattern, email):
        return True, email

    return False, "Invalid email format."


# ======================================================
# File Operations
# ======================================================

def load_contacts():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except:
            return {}
    return {}


def save_contacts(contacts):
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(contacts, file, indent=4)
    except Exception as e:
        print("Error saving file:", e)


def backup_contacts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as src:
            data = json.load(src)

        with open(BACKUP_FILE, "w") as dst:
            json.dump(data, dst, indent=4)

        print("Backup created successfully.")


def export_csv(contacts):
    with open("contacts.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Name",
            "Phone",
            "Email",
            "Address",
            "Category"
        ])

        for name, info in contacts.items():
            writer.writerow([
                name,
                info["phone"],
                info["email"],
                info["address"],
                info["category"]
            ])

    print("Contacts exported to contacts.csv")


# ======================================================
# CRUD Functions
# ======================================================

def add_contact(contacts):
    print("\nAdd Contact")

    name = input("Name: ")

    valid, result = validate_name(name)

    if not valid:
        print(result)
        return

    name = result

    if name in contacts:
        print("Contact already exists.")
        return

    phone = input("Phone: ")
    valid, result = validate_phone(phone)

    if not valid:
        print(result)
        return

    phone = result

    email = input("Email: ")

    if email:
        valid, result = validate_email(email)
        if not valid:
            print(result)
            return
        email = result

    address = input("Address: ").strip()

    category = input(
        "Category (Family/Friend/Work/Others): "
    ).title().strip()

    if not category:
        category = "Others"

    contacts[name] = {
        "phone": phone,
        "email": email,
        "address": address,
        "category": category,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    save_contacts(contacts)

    print("Contact added successfully.")


def search_contact(contacts):
    keyword = input("Enter name to search: ").strip().lower()

    found = False

    for name, info in contacts.items():
        if keyword in name.lower():
            print("\n---------------------------")
            print("Name:", name)
            print("Phone:", info["phone"])
            print("Email:", info["email"])
            print("Address:", info["address"])
            print("Category:", info["category"])
            found = True

    if not found:
        print("No matching contacts found.")


def search_phone(contacts):
    phone = input("Enter phone number: ").strip()

    for name, info in contacts.items():
        if info["phone"] == phone:
            print("\nContact Found")
            print(name)
            print(info)
            return

    print("Phone number not found.")


def update_contact(contacts):
    name = input("Enter contact name: ").title().strip()

    if name not in contacts:
        print("Contact not found.")
        return

    print("Leave field blank to keep old value.")

    phone = input("New Phone: ")

    if phone:
        valid, result = validate_phone(phone)

        if not valid:
            print(result)
            return

        contacts[name]["phone"] = result

    email = input("New Email: ")

    if email:
        valid, result = validate_email(email)

        if not valid:
            print(result)
            return

        contacts[name]["email"] = result

    address = input("New Address: ")

    if address:
        contacts[name]["address"] = address

    category = input("New Category: ")

    if category:
        contacts[name]["category"] = category.title()

    save_contacts(contacts)

    print("Contact updated successfully.")


def delete_contact(contacts):
    name = input("Enter contact name: ").title().strip()

    if name not in contacts:
        print("Contact not found.")
        return

    confirm = input(
        f"Delete '{name}'? (y/n): "
    ).lower()

    if confirm == "y":
        del contacts[name]
        save_contacts(contacts)
        print("Contact deleted.")
    else:
        print("Cancelled.")


# ======================================================
# Display Functions
# ======================================================

def display_contacts(contacts):
    if not contacts:
        print("No contacts available.")
        return

    print("\n============== CONTACTS ==============")

    for name in sorted(contacts):
        info = contacts[name]

        print("-" * 40)
        print("Name     :", name)
        print("Phone    :", info["phone"])
        print("Email    :", info["email"])
        print("Address  :", info["address"])
        print("Category :", info["category"])


def statistics(contacts):
    print("\nStatistics")

    print("Total Contacts:", len(contacts))

    categories = {}

    for info in contacts.values():
        cat = info["category"]
        categories[cat] = categories.get(cat, 0) + 1

    print("\nCategory Counts")

    for cat, count in categories.items():
        print(cat, ":", count)


# ======================================================
# Menu
# ======================================================

def menu():
    contacts = load_contacts()

    while True:

        print("\n")
        print("=" * 40)
        print(" CONTACT MANAGEMENT SYSTEM ")
        print("=" * 40)

        print("1. Add Contact")
        print("2. Search Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. Display Contacts")
        print("6. Search by Phone")
        print("7. Statistics")
        print("8. Backup Contacts")
        print("9. Export CSV")
        print("0. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_contact(contacts)

        elif choice == "2":
            search_contact(contacts)

        elif choice == "3":
            update_contact(contacts)

        elif choice == "4":
            delete_contact(contacts)

        elif choice == "5":
            display_contacts(contacts)

        elif choice == "6":
            search_phone(contacts)

        elif choice == "7":
            statistics(contacts)

        elif choice == "8":
            backup_contacts()

        elif choice == "9":
            export_csv(contacts)

        elif choice == "0":
            save_contacts(contacts)
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


# ======================================================
# Program Entry
# ======================================================

if __name__ == "__main__":
    menu()