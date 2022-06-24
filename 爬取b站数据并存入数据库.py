import requests
import json
from multiprocessing.dummy import Pool as ThreadPool
import time
import sqlite3, csv, re

# http://api.bilibili.com/x/web-interface/newlist?rid={rid}&pn={pn}&ps={ps}
comic_list = []
urls = []


def get_url():
    url = 'http://api.bilibili.com/x/web-interface/newlist?rid=32&pn='
    for i in range(1, 333):
        urls.append(url + str(i) + '&ps=50')


def get_message(url):
    time.sleep(0.5)
    head = {
        'accept-encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69'
    }
    try:
        r = requests.get(url, timeout=5, headers=head)
        print(r)
        time.sleep(0.1)
        data = json.loads(r.text)['data']['archives']
        for j in range(len(data)):
            content = {}
            content['title'] = data[j]['title']
            content['view'] = data[j]['stat']['view']
            content['danmaku'] = data[j]['stat']['danmaku']
            content['favorite'] = data[j]['stat']['favorite']
            content['coin'] = data[j]['stat']['coin']
            comic_list.append(content)
    except Exception as e:
        print(e)


def write_to_file(comic_list):
    with open('./bilibili-comic.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['title', 'view', 'danmaku', 'favorite', 'coin']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        try:
            writer.writerows(comic_list)
        except Exception as e:
            print(e)


get_url()
pool = ThreadPool(4)
pool.map(get_message, urls)
pool.close()
write_to_file(comic_list)

dbpath = 'bilibili_comic.db'
file = 'bilibili-comic.csv'
s = re.compile('\d+')
q1 = re.compile('"')


def main():
    datalist = Datalist(file)
    saveData2db(datalist, dbpath)


def Datalist(file):
    with open(file, 'r', encoding='utf8') as f:
        datalist = csv.reader(f)
        datalist = list(datalist)
    return datalist


def saveData2db(datalist, dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for i in range(1, len(datalist)):
        data = datalist[i]
        if re.findall(q1, data[0]):
            data[0] = "'" + data[0] + "'"
        else:
            data[0] = '"' + data[0] + '"'
        print(data, type(data[0]), type(data[2]))
        sql = '''
        insert into bilibili_comic(
        name,watch,danmaku,favorite,coin)
        values(%s)''' % ",".join(data)
        print(sql)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()


def init_db(dbpath):
    sql = '''
    create table bilibili_comic
    (
    id integer primary key autoincrement,
    name varchar,
    watch numeric,
    danmaku numeric,
    favorite numeric,
    coin numeric
        )
    '''
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
    print('生成数据库成功')
