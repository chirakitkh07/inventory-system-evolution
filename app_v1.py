# app_v1.py — Inventory Management System (Legacy Version)
# Technical Debt: global state, cryptic variable names, mixed I/O + logic

x = []          # global inventory list
n = 0           # global item counter (ID seed)

def add():
    global x, n
    a = input("Enter product name: ")
    b = input("Enter quantity: ")
    c = input("Enter price: ")
    q = input("Enter category: ")
    n += 1
    r = {"id": n, "name": a, "qty": int(b), "price": float(c), "cat": q}
    x.append(r)
    print("Added.")

def view():
    global x
    if len(x) == 0:
        print("No items.")
        return
    for i in x:
        print(f"[{i['id']}] {i['name']} | Qty:{i['qty']} | Price:{i['price']} | Cat:{i['cat']}")

def srch():
    global x
    a = input("Enter name to search: ")
    res = []
    for i in x:
        if a.lower() in i["name"].lower():
            res.append(i)
    if len(res) == 0:
        print("Not found.")
    else:
        for i in res:
            print(f"[{i['id']}] {i['name']} | Qty:{i['qty']} | Price:{i['price']} | Cat:{i['cat']}")

def upd():
    global x
    a = int(input("Enter ID to update: "))
    for i in x:
        if i["id"] == a:
            b = input("New name (blank=keep): ")
            c = input("New qty (blank=keep): ")
            d = input("New price (blank=keep): ")
            if b != "":
                i["name"] = b
            if c != "":
                i["qty"] = int(c)
            if d != "":
                i["price"] = float(d)
            print("Updated.")
            return
    print("Not found.")

def dlt():
    global x
    a = int(input("Enter ID to delete: "))
    for i in x:
        if i["id"] == a:
            x.remove(i)
            print("Deleted.")
            return
    print("Not found.")

def tot():
    global x
    s = 0
    for i in x:
        s += i["qty"] * i["price"]
    print(f"Total inventory value: {s:.2f}")

def menu():
    while True:
        print("\n=== Inventory System v1 ===")
        print("1. Add product")
        print("2. View all")
        print("3. Search")
        print("4. Update")
        print("5. Delete")
        print("6. Total value")
        print("0. Exit")
        ch = input("Choice: ")
        if ch == "1":
            add()
        elif ch == "2":
            view()
        elif ch == "3":
            srch()
        elif ch == "4":
            upd()
        elif ch == "5":
            dlt()
        elif ch == "6":
            tot()
        elif ch == "0":
            print("Bye.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    menu()
