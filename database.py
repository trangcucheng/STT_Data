import sqlite3

conn = sqlite3.connect("split_audios.db")
c = conn.cursor()


#  ===== USERS  ======
# c.execute(""" create table users(
#     id integer primary key autoincrement,
#     username text,
#     password text

# )""")
# c.execute("insert into users(username, password) values(?,?)",('admin','0'))
# c.execute("drop table users")

# c.execute("select * from users")
# for item in c.fetchall():
#     print(item)


# ======= LINKS ====
# c.execute("""create table links(
#     id integer primary key autoincrement,
#     name text,
#     url text,
#     time text,
#     gender text,
#     voice text,
#     topic text,
#     user_id int,
#     status text
#     )
# """)

# ====== TOPICS  =====
# c.execute("""create table topics(
#     id integer primary key autoincrement,
#     topic text,
#     url text,
#     description text
# )
# """)


# c.execute("""create table downloaded_audios(
#     id integer primary key autoincrement,
#     original_id integer,
#     url text,
#     description text,
#     folder text
# )
# """)
# c.execute("select * from downloaded_audios")
# for i in c.fetchall():
#     print(i)
# c.execute("drop table downloaded_audios")
# c.execute("update links set status = 'no' where id =10")
# c.execute("insert into topics(")

# items=[
# ('Khác biệt hai nền giáo dục Việt Nam và Mỹ', 'https://www.youtube.com/watch?v=kFfyqMP7qL0', '11:55', 'nam', 'mien_nam', 'giao_duc', 3, 'no'),
# ('Chiến thắng BẠCH ĐẰNG do NGÔ QUYỀN lãnh đạo năm 938', 'https://www.youtube.com/watch?v=YycIqxeq2vI', '11:00', 'nam', 'mien_bac', 'lich_su', 3, 'no'),
# ('Các nước Á, Phi, Mỹ-Latinh (1945 - 2000)', 'https://www.youtube.com/watch?v=zMPDIkQkYj0', '23:01', 'nu', 'mien_trung', 'lich_su', 3, 'no'),
# ('10 dấu hiệu cho thấy bạn đã biết nuôi dưỡng nội tâm', 'https://www.youtube.com/watch?v=dwb8rHyH2ew', '25:04', 'nu', 'mien_nam', 'doi_song', 3, 'no'),
# ('Làm sao để tự tin livestream bán hàng ? 4 bước này sẽ giúp bạn!', 'https://www.youtube.com/watch?v=wWPZhwX9tqM', '04:28', 'nam', 'mien_nam', 
# 'kinh_doanh', 3, 'splited'),
# ('Shark Phú “Vươn Vòi Bạch Tuộc” Đầu Tư Hơn 4 Tỷ Vào Startup Song Sinh! |', 'http://www.youtube.com/watch?v=ZjpCqARCz5U', '17:00', 'nam', 'mien_bac', 'kinh_te', 4, 'no'),
# ('Diễn Biến Lượt Đi Vòng Play-Offs UEFA Champions League', 'https://www.youtube.com/watch?v=OeeDCFIUbQw', '09:38', 'nam', 'mien_bac', 'the_thao', 4, 'splited'),
# ('Ronaldo tỏa sáng, MU đại thắng - Indonesia tự tin thắng Thái 4 bàn như Liver', 'https://www.youtube.com/watch?v=9dNXkSG1nNk', '10:39', 'nam', 'mien_bac', 'the_thao', 4, 'no'),
# ('Tin tức Việt Nam mới nhất hôm nay 01/01/2022 tin tức 24h', 'https://www.youtube.com/watch?v=b9E1VlCtJqA', '16:41', 'nu', 'mien_nam', 'thoi_su', 4, 'no'),
# ('TIN BÃO SỐ 9: Thủ Tướng Họp Khẩn Cấp Bão số 9 Cực Mạnh sẽ càn quét miền Trung', 'https://www.youtube.com/watch?v=TPZCVFVSxN8', '04:12', 'nu', 'mien_bac', 'thoi_tiet', 4, 'splited')
# ]

c.execute("select * from topics")
for i in c.fetchall():
    print(i)

conn.commit()
conn.close()

