from mysql.connector import connect, Error


def _dbQuery(sql, fetch=False):
    try:
        with connect(
                host='mysql.osinvladislav.myjino.ru',
                user='046502789_aloe',
                password='aloevera',
                database='osinvladislav_aloevera'
        ) as db:
            cursor = db.cursor()
            cursor.execute(sql)

            if fetch:
                return cursor.fetchall()
            else:
                db.commit()
                return cursor
    except Error:
        return False


def auth(login, password, telegram_id):
    answer = _dbQuery(
        "SELECT * FROM `users` WHERE (`login` = '" + login + "' OR `email` = '" + login + "') AND `password` = '" + password + "'",
        fetch=True)

    if answer:
        answ = _dbQuery(
            "UPDATE `users` SET `telegram_id`='" + telegram_id + "' WHERE `id`=" + str(answer[0][0]))
        return True
    else:
        return False

def complete(task_id) -> bool:

    return True


def getEventsForUser(id):
    user_id = _dbQuery(f"SELECT * FROM `users` WHERE `telegram_id` = {str(id)}", fetch=True)
    #print(f"getEventsForUser({user_id})")
    answer = _dbQuery(
        "SELECT * FROM `user_plants` WHERE `user_id` = '" + str(user_id[0][0]) + "'", fetch=True)

    if answer:
        events = []
        for answ in answer:
            ans = _dbQuery(
                "SELECT * FROM `events` WHERE `plant_id` = '" + str(answ[0]) + "'", fetch=True)

            for an in ans:
                a = _dbQuery(
                    "SELECT * FROM `event_types` WHERE `id` = '" + str(an[2]) + "'", fetch=True)

                events.append([a[0][1], an[3], an[4]])
        print(events)
        return events
    else:
        return False

if __name__ == "__main__":
    print(getEventsForUser(1))
