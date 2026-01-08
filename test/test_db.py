from backend.databases import save_to_db, get_all_messages

print("Running DB unit test")

ok = save_to_db("Testing message from test folder")

print("Insert status:", ok)

rows = get_all_messages()

print("Fetched rows:", rows)
