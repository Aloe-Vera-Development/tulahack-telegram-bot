from mysql.connector import connect, Error


def _dbQuery(sql, fetch=False):
    try:
        with connect(
                host='hui',
                user='hooi',
                password='hooi',
                database='osinvlaggjhgjdislav_aloevera'
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
    answer = _dbQuery( f"UPDATE `events` SET `completed`='1' WHERE `id`='{task_id}'")
    print(f"complete({task_id}): {answer}")
    if answer:
        return True
    else:
        return False

def getEventsForUser(id):
    user_id = _dbQuery(f"SELECT * FROM `users` WHERE `telegram_id`='{str(id)}'", fetch=True)
    #print(user_id)
    if (user_id):
        print("hi teheran")
        print(f"getEventsForUser({user_id})")
        print(f"USING:{str(user_id[0][-1])}") 
    answer = _dbQuery(
        "SELECT * FROM `user_plants` WHERE `user_id` = '" + str(user_id[0][0]) + "'", fetch=True)
    print(f"getEventsForUser({user_id[0][0]}, {answer})")
    if answer:
        events = []
        for answ in answer:
            ans = _dbQuery(
                "SELECT * FROM `events` WHERE `plant_id` = '" + str(answ[0]) + "'", fetch=True)

            for an in ans:
                a = _dbQuery(
                    "SELECT * FROM `event_types` WHERE `id` = '" + str(an[2]) + "'", fetch=True)
                print("a: " + str(a))
                print("ans: " + str(ans))
                events.append([a[0][1], an[3], an[4], an[0]])
        return events
    else:
        return False

if __name__ == "__main__":
    # response = _dbQuery("INSERT INTO `user_plants` (user_id, plant_id, name, datetime)  VALUES (2, 1, 'Огуречикус легендариус', now())")
    # response = _dbQuery("INSERT INTO `events` (plant_id, type, completed, datetime)  VALUES (5, 1, 0, now())")
    response = _dbQuery("SELECT * FROM `events`", fetch=True)
    
    print(response)
