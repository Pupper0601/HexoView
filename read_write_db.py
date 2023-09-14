import json
import os


def find_db(data):
    os.system("sudo chmod 777 ./db.json")
    if type(data) != dict:
        data = json.loads(data)

    with open("db.json", "r+", encoding="utf8") as f:
        read_data = json.loads(f.read())
        print(read_data)
        if data["address"] in read_data.keys():
            return read_data[data["address"]]["items"]
        else:
            read_data[data["address"]] = {"users": {},
                                          "items": {"view1": 0, "view2": 0, "view3": 0, "view4": 0, "view5": 0,
                                                    "view6": 0, "view7": 0, "view8": 0, "view9": 0}}
            res = read_data[data["address"]]["items"]
            read_data = json.dumps(read_data, ensure_ascii=False)
            print(read_data)
            f.truncate(0)
            f.seek(0, 0)
            f.write(read_data)
            return res


def insert_db(data):
    if type(data) != dict:
        data = json.loads(data)
    address = data["address"]
    ip = data["ip"]
    view = data["view"]
    with open("db.json", "r+", encoding="utf8") as f:
        db = json.loads(f.read())
        if address not in db.keys():
            db[address] = {"users": {},
                           "items": {"view1": 0, "view2": 0, "view3": 0, "view4": 0, "view5": 0,
                                     "view6": 0, "view7": 0, "view8": 0, "view9": 0}}
        ip_keys_list = db[address]["users"].keys()
        if ip in ip_keys_list:
            for i in db[address]["users"][ip].keys():
                if i != view:
                    db[address]["users"][ip][i] = 0
                else:
                    db[address]["users"][ip][i] = 1
        else:
            db[address]["users"][ip] = {}
            for i in range(1, 10):
                v = "view" + str(i)
                if v != view:
                    db[address]["users"][ip][v] = 0
                else:
                    db[address]["users"][ip][v] = 1
        print(db[address]["users"])

        for i in db[address]["items"].keys():
            db[address]["items"][i] = 0
            for j in db[address]["users"].keys():
                db[address]["items"][i] += db[address]["users"][j][i]
        print(db[address]["items"])

        res = db[address]["items"]
        read_data = json.dumps(db, ensure_ascii=False)
        print(read_data)
        f.truncate(0)
        f.seek(0, 0)
        f.write(read_data)
        return res


if __name__ == '__main__':
    # jh = JsonHandle()
    # a = jh.insert_view({"address": "https://pupper.cn/posts/b3426ccb.html", "ip": "127.0.0.12", "view": "view4"})
    # print(a)

    # a = find_db({"address": "https://pupper.cn/posts/b343444.html"})
    # print(a)
    b = insert_db({"address": "https://pupper.cn/posts/b3426ccc.html", "ip": "127.0.0.1", "view": "view9"})
    print(b)
