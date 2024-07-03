from database.DB_connect import DBConnect
from model.stato import Stato

# DAO Copia incolla per velocizzare
class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getYearAvv():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct year(s.`datetime`) as data, count(s.id) as peso
                    from sighting s 
                    group by year(s.`datetime`)
                    order by s.`datetime` """
        cursor.execute(query, ())
        for row in cursor:
            result.append(row["shape"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getStates(anno):
        """ stati con almeno un avvistamento nell'anno"""
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from state s 
                    where s.id in (select distinct s2.state 
                    from sighting s2
                    where year(s2.datetime) = %s"""

        cursor.execute(query,(anno,))

        for row in cursor:
            result.append(Stato(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getConnessioni(anno):
        """ stati collegati in base ad avvistamenti in serie temporale"""
        """ [(id_stato1 , id_stato2)]"""

        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.s1 as stat1, t2.s2 as stat2
                    from
                    (select s.state as s1, max(s.`datetime`) as m1  
                    from sighting s 
                    where year(s.`datetime`) = "2010"
                    group by s.state) as t1,
                    (select s.state as s2, min(s.`datetime`) as m2
                    from sighting s 
                    where year(s.`datetime`) = %s
                    group by s.state) as t2
                    where t1.s1 != t2.s2 and t1.m1 > t2.m2
                    """

        cursor.execute(query,(anno,) )

        for row in cursor:
            result.append((row["stat1"], row["stat2"]))

        cursor.close()
        conn.close()
        return result
