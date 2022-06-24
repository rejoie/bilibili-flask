import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image  # 图片处理
import numpy as np  # 矩阵运算
import sqlite3, re

p = re.compile('【.*?】|\[.*?\]|\,|\(|\)')

con = sqlite3.connect('bilibili_comic.db')
cur = con.cursor()
sql = 'select name from bilibili_comic'
data = cur.execute(sql)
text = ''
for item in data:
    item = str(item)
    item = re.sub(p, '', item)
    text = text + item
cur.close()
con.close()

cut = jieba.cut(text)
string = ' '.join(cut)
print(len(string))

img = Image.open(r'.\static\assets\img\tree.jpg')  # 打开遮罩图片
img_array = np.array(img)  # 将图片转换成数组
wc = WordCloud(
    background_color='white',
    mask=img_array,
    font_path='STXINGKA.TTF'
)
wc.generate_from_text(string)

# 绘制图片
fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off') # 是否显示坐标轴
# plt.show() # 显示生成词云图片

# 输出词云图片到文件
plt.savefig(r'.\static\assets\img\word.jpg', dpi=500)
