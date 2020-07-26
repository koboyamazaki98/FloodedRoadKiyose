from django.db import connection

SQL_PHOTO_NEXTSEQNO = \
"select A.YYYYMM, B.MAXSEQNO, (ifnull(B.MAXSEQNO, 0) + 1) as NEXTSEQNO \n" + \
"from \n" + \
"(\n" + \
"select {} as YYYYMM \n" + \
") as A \n" + \
"left outer join (\n" + \
"select YYYYMM, max(SEQNO) as MAXSEQNO \n" + \
"from (\n" + \
"select (CODE / 10000) as YYYYMM, (CODE % 10000) SEQNO from AC01_PHOTO \n" + \
") \n" + \
"group by yyyymm \n" + \
") as B on (A.YYYYMM=B.YYYYMM);"

SQL_MENBER_NO = "select member_no from ac01_member where member_no=%s;"

# Photo テーブルから、新規レコードIDを取得する
def get_photo_nextcode(yyyymm: int) -> int:
    sql = SQL_PHOTO_NEXTSEQNO.format(yyyymm)
    print("get_photo_nextcode - SQL:", sql)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        record = cursor.fetchone()
        print(record)
    seqno = record[2]
    return yyyymm * 10000 + seqno

# Photo テーブルから、新規レコードIDを取得する
def has_member_no(member_no: int) -> bool:
    with connection.cursor() as cursor:
        print("has_member_no - ", SQL_MENBER_NO, " - ", member_no)
        cursor.execute(SQL_MENBER_NO, (str(member_no), ))
        record = cursor.fetchone()
    if record is None:
        return False
    if len(record) == 0:
        return False
    result = record[0]
    if result is None:
        return False
    print("record :", type(result))
    print("record :", result)
    return (result == member_no)
