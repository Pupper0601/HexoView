import json


class JsonHandle:
    def __init__(self):
        with open('data.json') as file:
            self.data = json.load(file)

        self.__create_table()

    def __create_table(self):
        if "hexo_article" not in self.data:
            self.data["hexo_article"] = []

        if "hexo_user" not in self.data:
            self.data["hexo_user"] = []

    def find_view(self, view_data):
        if type(view_data) != dict:
            view_data = json.loads(view_data)

        view_id = None
        for article in self.data["hexo_article"]:
            if article["address"] == view_data["address"]:
                view_id = article["id"]
                break

        if view_id is None:
            return {"v1": 0, "v2": 0, "v3": 0, "v4": 1, "v5": 0, "v6": 0, "v7": 0, "v8": 0, "v9": 0}

        view = {"v1": 0, "v2": 0, "v3": 0, "v4": 0, "v5": 0, "v6": 0, "v7": 0, "v8": 0, "v9": 0}
        for user in self.data["hexo_user"]:
            if user["id"] == view_id:
                view[view_data["view"]] += 1

        return view

    def insert_view(self, view_data):
        if type(view_data) != dict:
            view_data = json.loads(view_data)

        view_id = None
        for article in self.data["hexo_article"]:
            if article["address"] == view_data["address"]:
                view_id = article["id"]
                break

        if view_id is None:
            view_id = len(self.data["hexo_article"]) + 1
            self.data["hexo_article"].append({"id": view_id, "address": view_data["address"]})

        for user in self.data["hexo_user"]:
            if user["id"] == view_id and user["ip"] == view_data["ip"]:
                self.data["hexo_user"].remove(user)
                break

        self.data["hexo_user"].append({"ip": view_data["ip"], "id": view_id, view_data["view"]: 1})

        with open('data.json', 'w') as file:
            json.dump(self.data, file)

        return self.find_view({"address": view_data["address"]})


if __name__ == '__main__':
    jh = JsonHandle()
    a = jh.insert_view({"address": "https://pupper.cn/posts/b3426ccb.html", "ip": "127.0.0.12", "view": "view4"})
    print(a)
