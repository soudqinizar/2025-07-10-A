from database.DB_connect import DBConnect
from model.categorie import Categorie
from model.product import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getAllCategories():
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = "select distinct(c.category_id) , c.category_name from categories c"
        cursor.execute(query,)
        for row in cursor:
            results.append(Categorie(**row))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(categorie):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """select p.*
                    from categories c , products p 
                    where c.category_id = p.category_id 
                    and c.category_id = %s"""
        cursor.execute(query, (categorie.category_id,))
        for row in cursor:
            results.append(Product(**row))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(categorie, da, a):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """select p.product_id , count(distinct(o.order_id)) as numVendite
                    from products p, order_items oi , orders o 
                    where p.product_id = oi.product_id 
                    and o.order_id = oi.order_id 
                    and p.category_id = %s
                    and o.order_date >= %s
                    and o.order_date <= %s
                    group by p.product_id """
        cursor.execute(query, (categorie.category_id, da,a))
        for row in cursor:
            results.append((row["product_id"], row["numVendite"]))
        cursor.close()
        conn.close()
        return results
