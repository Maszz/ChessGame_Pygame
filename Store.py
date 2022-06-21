from StoreItem import StoreItem


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
            print("Created new instance of {}".format(class_))

        return instances[class_]

    return getinstance


@singleton
class Store:
    def __init__(self):
        self.storeObj: dict[str, StoreItem] = dict[str, StoreItem]()
        self.storeItem = StoreItem

    def __getitem__(self, key: str) -> StoreItem:
        return self.storeObj[key]

    def __setitem__(self, key: str, value: StoreItem) -> None:
        self.storeObj[key] = value


# if __name__ == '__main__':
#     store = Store()
