from config.db import pgsqlConn, sql

class authRepo:
    def selectLogin(self, email=None, password=None):
        if not email or not password:
            return False

        cur = pgsqlConn.cursor()
        stmt = sql.SQL('''
            SELECT
                u.id
            FROM users u
            WHERE u.email = %s AND u.password = %s
            LIMIT 1;
        ''')
        cur.execute(stmt, (email, password))
        data = cur.fetchone()
        cur.close()

        return bool(data)
