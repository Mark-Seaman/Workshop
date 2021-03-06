from datetime import datetime
from os.path import exists
from os import system
from sys import argv

from days import days_ago


def todo_command():
    for d in recent_dates():
        edit_task_file(d)


def recent_dates(days=3):
    start = datetime.today()
    return [ days_ago(start, days-d-1) for d in range(days) ]


task_default = '''%s

Grow 0

    3, 3, 1, 1
    weight: 20    
    
People 0
    

Fun 0
    

'''


def edit_task_file(date):
    f = 'Documents/info/days/%s' % date
    if not exists(f):
        open(f, 'w').write(task_default % datetime.now().strftime("%A"))
    system('e %s' % f)


if __name__ == '__main__':
    print(todo_command())
