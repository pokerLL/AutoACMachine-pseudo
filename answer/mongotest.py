import pymongo as mg

if __name__ == "__main__":
    mgc = mg.MongoClient("mongodb://localhost:27017/")
    dbs = mgc.list_database_names()

    dotdb = mgc["dotcpp"]
    ll = dotdb.list_collections()
    print(len([i for i in ll]))
