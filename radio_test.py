test_dict = {"user1" : {"name":"connor", "age":22}}
new_data = {"name": "conor", "age":23}
print(test_dict["user1"].update(new_data))
print(test_dict)