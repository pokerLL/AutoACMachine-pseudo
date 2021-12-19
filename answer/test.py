from settings import *

if __name__ == "__main__":
    print(BASE_DIR)
    print(LOG_DIR)
    with open(LOG_DIR + sep + "wrong_url.txt", "r+") as f:
        print(f.readline())
