from settings import WRONG_URL_LOG
import pymongo

mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")


class CodeAnswer:
    db_name = ""
    pid = ""
    _type = ""
    url = ""
    code = ""

    def __init__(self, dict=None):
        if dict is not None:
            self.pid = dict["pid"]
            self._type = dict["type"]
            self.url = dict["url"]
            self.code = dict["code"]

    def get_code(self):
        return self.code

    def save(self):
        pass

    def save_to_file(self):
        pass

    def save_to_mongodb(self, dbname):
        self.db_name = dbname
        try:
            db = mongoclient[self.db_name]
            col = db[str(self.pid)]
            col.insert_one(self.to_dict())
        except:
            return False
        return True

    def load_answer(self):
        pid, _type = self.pid, self._type
        ans_list = []
        db = mongoclient[self.db_name]
        col = db[str(pid)]
        rows = col.find({"type": _type})
        for ans in rows:
            del ans["_id"]
            ans_list.append(CodeAnswer(ans))
        return ans_list

    def save_wrong(self):
        with open(WRONG_URL_LOG, "a+") as f:
            f.write(str(self.pid) + "\t" + self.url + "\n")

    def delete(self):
        pass

    def to_dict(self):
        res = {
            "pid": self.pid,
            "type": self._type,
            "url": self.url,
            "code": self.code,
        }
        return res

    def __str__(self):
        return "++++++++++++++++++\n" \
               + str(self.pid) + " " + self.url + " " + self._type \
               + "\n" + self.code \
               + "\n" + "+++++++++++++++++++++++\n"

    def __repr__(self):
        return self.__str__()
