import json
def register(message):
    msg_list = json.loads(message)
    new_username, new_password = msg_list[1], msg_list[2]
    with open("Main.json", "r") as f:
        data = json.load(f)
    if new_username in data["Password"]:
        response = "username_taken"
    else:
        data["Password"][new_username] = new_password
        with open("main.json", "w") as f:
            json.dump(data, f)
        response = "success"
    return response

message = '["register", "new_user", "aaa"]'
registration_response = register(message)
print(registration_response)