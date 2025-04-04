from config.db import pgsqlConn, sql
import json

class usersRepo:
    def selectAllOrById(self, id=0, limit=15):
        cur = pgsqlConn.cursor()
        stmt = sql.SQL('''
            SELECT
                u.id,
                u.firstname,
                u.lastname,
                u.email,
                u.status,
                u.createdat,
                u.updatedat,
                json_build_object(
                    'id', r.id,
                    'name', r.name,
                    'status', r.status
                ) AS role,
                json_agg(
                    json_build_object(
                        'id', rr.id,
                        'name', rr.resources,
                        'status', rr.status
                    )
                ) AS resources
            FROM users u
            LEFT JOIN users_rol ur ON u.id = ur.user_id
            LEFT JOIN rol r ON ur.rol_id = r.id
            LEFT JOIN resources_rol rr ON r.id = rr.rol_id
            WHERE (%s = 0 OR u.id = %s)
            GROUP BY
                u.id,
                u.firstname,
                u.lastname,
                u.email,
                u.status,
                u.createdat,
                u.updatedat,
                r.id,
                r.name,
                r.status
            LIMIT %s;
        ''')
        cur.execute(stmt, (id, id, limit))
        data = cur.fetchall()
        cur.close()
        result = []
        for row in data:
            user_dict = {
                "id": row[0],
                "firstname": row[1],
                "lastname": row[2],
                "email": row[3],
                "status": row[4],
                "createdat": row[5].isoformat() if row[5] else None,
                "updatedat": row[6].isoformat() if row[6] else None,
                "role": row[7],
                "resources": row[8]
            }
            result.append(user_dict)
        return result

    def get_by_conditions(self, conditions=None):
        cur = pgsqlConn.cursor()

        select_part = sql.SQL(',').join(map(sql.Identifier, ['id', 'firstname', 'lastname', 'email', 'status', 'createdat', 'updatedat']))

        if conditions:
            where_clauses = [
                sql.SQL("{} = %s").format(sql.Identifier(col))
                for col in conditions.keys()
            ]
            where_part = sql.SQL(' AND ').join(where_clauses)
            query = sql.SQL('SELECT CAST(row_to_json(row) as text) FROM (SELECT {} FROM users WHERE {}) row;').format(
                select_part,
                where_part
            )
            cur.execute(query, tuple(conditions.values()))
        else:
            query = sql.SQL('SELECT CAST(row_to_json(row) as text) FROM (SELECT {} FROM users) row;').format(
                select_part
            )
            cur.execute(query)

        data = cur.fetchall()
        cur.close()
        return [json.loads(row[0]) for row in data]

    def insert(self, user_data, rol_id):
        try:
            cur = pgsqlConn.cursor()

            user_columns = ['firstname', 'lastname', 'email', 'password']
            user_values = tuple(user_data[col] for col in user_columns)
            stmt = sql.SQL("INSERT INTO users ({}) VALUES ({}) RETURNING id").format(
                sql.SQL(',').join(map(sql.Identifier, user_columns)),
                sql.SQL(',').join(sql.Placeholder() * len(user_columns))
            )
            cur.execute(stmt, user_values)
            user_id = cur.fetchone()[0]

            users_rol_data = {
                'user_id': user_id,
                'rol_id': rol_id
            }
            users_rol_columns = ['user_id', 'rol_id']
            users_rol_values = tuple(users_rol_data[col] for col in users_rol_columns)
            stmt = sql.SQL("INSERT INTO users_rol ({}) VALUES ({})").format(
                sql.SQL(',').join(map(sql.Identifier, users_rol_columns)),
                sql.SQL(',').join(sql.Placeholder() * len(users_rol_columns))
            )
            cur.execute(stmt, users_rol_values)

            pgsqlConn.commit()
            cur.close()
            return user_id
        except Exception as e:
            print(f"Error: {e}")
            pgsqlConn.rollback()
            return False

    def update(self, record_id, data):
        try:
            cur = pgsqlConn.cursor()
            set_clause = sql.SQL(',').join(
                sql.SQL('{} = {}').format(sql.Identifier(col), sql.Placeholder()) for col in data.keys()
            )
            stmt = sql.SQL("UPDATE users SET {} WHERE id = %s").format(
                set_clause
            )
            values = tuple(data[col] for col in data.keys()) + (record_id,)
            cur.execute(stmt, values)
            pgsqlConn.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def delete(self, record_id):
        try:
            cur = pgsqlConn.cursor()
            stmt = sql.SQL("DELETE FROM users WHERE id = %s")
            cur.execute(stmt, (record_id,))
            pgsqlConn.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False