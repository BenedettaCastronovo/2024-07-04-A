from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getY():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct YEAR(s.`datetime`) as y
                        from sighting s 
                        order by `datetime` DESC"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["y"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getS(y):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        result = []
        query = """select distinct shape
                    from sighting s 
                    where s.shape is not null and year(s.`datetime`) = %s
                    order by shape"""
        cursor.execute(query, (y,))

        for row in cursor:
            result.append(row["shape"])
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getN(y, s):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        result = []
        query = """select distinct *
                    from sighting
                    where shape = %s and year(`datetime`) = %s"""
        cursor.execute(query, (s, y))
        for row in cursor:
            result.append(Sighting(**row))
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    #def has_edge(u, v):
    def getA(y, s):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        res = []
        #query = """select s1.id, s2.id, s1.`datetime`, s2.`datetime`
         #           from sighting s1, sighting s2
          #          where s1.state = s2.state and s1.id = %s and s2.id = %s
           #         """
        query="""select s1.id as a1, s2.id as a2
                from sighting s1, sighting s2
                where s1.state = s2.state and s1.id<>s2.id and s1.`datetime` < s2.`datetime` and year(s1.datetime) = %s and s1.shape = %s
                  and year(s2.datetime) = %s and s2.shape = %s"""
        #cursor.execute(query, (u.id, v.id))
        cursor.execute(query, (y, s, y, s))
        for row in cursor:
            res.append((row["a1"], row["a2"]))
        cursor.close()
        cnx.close()
        #if len(res) > 0:
          #  return True
        #return False
        return res
