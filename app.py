from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index')
def home():
    return index()


@app.route('/comic')
def comic():
    datalist = []
    con = sqlite3.connect('bilibili_comic.db')
    cur = con.cursor()
    sql = "select * from bilibili_comic"
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    cur.close()
    con.close()
    return render_template('comic.html', comics=datalist)


@app.route('/watch')
def watch():
    watch = ['<100', '100-1000', '1000-1w', '1w-10w', '10w-100w', '100w-1000w', '>1000w']
    num = []
    con = sqlite3.connect('bilibili_comic.db')
    cur = con.cursor()
    sql = '''select case when watch<=100 then 1
    when watch>100 and watch<=1000 then 2
    when watch>1000 and watch<=10000 then 3
    when watch>10000 and watch<=100000 then 4
    when watch>100000 and watch<=1000000 then 5
    when watch>1000000 and watch<=10000000 then 6
    when watch>10000000 then 7
    else 0 end as watch,count(*) as counts from bilibili_comic
        group by case when watch<=100 then 1
    when watch>100 and watch<=1000 then 2
    when watch>1000 and watch<=10000 then 3
    when watch>10000 and watch<=100000 then 4
    when watch>100000 and watch<=1000000 then 5
    when watch>1000000 and watch<=10000000 then 6
    when watch>10000000 then 7
    else 0 end
        '''
    data = cur.execute(sql)
    for item in data:
        num.append(item[1])
    cur.close()
    con.close()
    return render_template('watch.html',watch=watch,num=num)


@app.route('/coin')
def coin():
    coin = ['<10','10-100', '100-1000', '1000-1w', '1w-10w', '10w-100w']
    num = []
    con = sqlite3.connect('bilibili_comic.db')
    cur = con.cursor()
    sql = '''select case when coin<=10 then 1
        when coin>10 and coin<=100 then 2
        when coin>100 and coin<=1000 then 3
        when coin>1000 and coin<=10000 then 4
        when coin>10000 and coin<=100000 then 5
        when coin>100000 then 6
        else 0 end as coin,count(*) as counts from bilibili_comic
            group by case when coin<=10 then 1
        when coin>10 and coin<=100 then 2
        when coin>100 and coin<=1000 then 3
        when coin>1000 and coin<=10000 then 4
        when coin>10000 and coin<=100000 then 5
        when coin>100000 then 6
        else 0 end
            '''
    data = cur.execute(sql)
    for item in data:
        num.append(item[1])
    cur.close()
    con.close()
    return render_template('coin.html',coin=coin,num=num)


@app.route('/word')
def word():
    return render_template('word.html')


if __name__ == '__main__':
    app.run()
