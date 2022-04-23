def routines_to_routine_table(routines) -> str:
    res = "Задания на сегодня:\n" + "=" * 20 + '\n'
    i = 0
    for routine in routines:
        res += f"{i}.Что: \"{routine[0]}\"\t Выполнено: {'Да' if (routine[1]) else 'Нет'}\n"
        i += 1
    return res

def parse_args(message:str,count:int):
    mes_final = message.split(' ')[1: min(count+1,  len(message.split(' ')))]
    return  mes_final 

