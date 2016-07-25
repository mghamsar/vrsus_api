import MySQLdb
from flask import jsonify, request, Response, make_response
from config import Config

class Db:

    def __init__(self):
        return None


    def runQuery(self,query):
        dbConnect = MySQLdb.connect(host=Config.MYSQL_DATABASE_HOST, user=Config.MYSQL_DATABASE_USER, 
            passwd=Config.MYSQL_DATABASE_PASSWORD,
            db=Config.MYSQL_DATABASE_DB,
            port=Config.MYSQL_DATABASE_PORT)
        
        cursor = dbConnect.cursor()

        try:
            cursor.execute(query)
            data = cursor.fetchall()
            return data
        except MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                return None
            except IndexError:
                print "MySQL Error: %s" % str(e)
                return None
