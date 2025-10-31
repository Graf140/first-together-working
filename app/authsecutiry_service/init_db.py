from models.database import get_db_action, close_db_action

def table_exists(table_name: str) -> bool:
    connection = get_db_action()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = %s
            );
        """, (table_name,))
        result = cursor.fetchone()
        return result[0] if result else False
    except Exception as e:
        print("Ошибка при проверке таблицы:", e)
        return False
    finally:
        cursor.close()
        close_db_action(connection)

def main():
    if not table_exists('users'):
        connection = get_db_action()
        cursor = connection.cursor()
        try:
            cursor.execute("""
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    mail varchar(100) UNIQUE NOT NULL,
                    phone VARCHAR(20) UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    date_create TIMESTAMP DEFAULT NOW()
                )
            """)
            connection.commit()
            print("Таблица 'users' создана")
        except Exception as e:
            print("Ошибка при создании таблицы 'users':", e)
            connection.rollback()
        finally:
            cursor.close()
            close_db_action(connection)
    else:
        print("Таблица 'users' уже существует")

    if not table_exists('user_session'):
        connection = get_db_action()
        cursor = connection.cursor()
        try:
            cursor.execute("""
                CREATE TABLE user_session (
                    id SERIAL PRIMARY KEY,
                    token TEXT NOT NULL,
                    status bool DEFAULT FALSE
                )
            """)

            connection.commit()
            print("Таблица 'user_session' создана")
        except Exception as e:
            print("Ошибка при создании таблицы 'user_session':", e)
            connection.rollback()
        finally:
            cursor.close()
            close_db_action(connection)
    else:
        print("Таблица 'user_session' уже существует")

if __name__ == "__main__":
    main()