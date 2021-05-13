from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import  declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from datetime import  datetime, timedelta


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def main():
    while True:
        print('''1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit''')
        today = datetime.today()
        entry = input()
        if entry == '1':
            rows = session.query(Table).filter(Table.deadline == today.date()).order_by(Table.deadline).all()
            print('Today', today.day, today.strftime('%b') + ':')
            if not rows:
                print('Nothing to do!')
            else:
                for row in rows:
                    print(row.task)
        if entry == '2':
            for i in range(7):
                loop_day = today + timedelta(days=i)
                rows = session.query(Table).filter(Table.deadline == loop_day.date()).order_by(Table.deadline).all()
                print()
                print(loop_day.strftime('%A %d %b:'))
                if not rows:
                    print('Nothing to do!')
                else:
                    for j in range(len(rows)):
                        print(str(j + 1) + '.', rows[j].task)
        if entry == '3':
            rows = session.query(Table).order_by(Table.deadline).all()
            print('All tasks:')
            for i in range(len(rows)):
                print(str(i + 1) + '.', rows[i].task + '.', int(rows[i].deadline.strftime('%d')), rows[i].deadline.strftime('%b'))
        elif entry == '4':
            rows = session.query(Table).filter(Table.deadline < today.date()).order_by(Table.deadline).all()
            print('Missed tasks:')
            if not rows:
                print('Nothing is missed!')
            else:
                for i, row in enumerate(rows):
                    print(str(i + 1) + '.', row.task + '.', int(rows[i].deadline.strftime('%d')), rows[i].deadline.strftime('%b'))
            print()
        elif entry == '5':
            print('Enter task')
            entry_task = input()
            print('Enter deadline')
            entry_deadline = input()
            session.add(Table(task=entry_task, deadline=datetime(*[int(date) for date in entry_deadline.split('-')])))
            session.commit()
            print('The task has been added!')
        elif entry == '6':
            rows = session.query(Table).order_by(Table.deadline).all()
            print('Choose the number of the task you wamt to delete:')
            for i in range(len(rows)):
                print(str(i + 1) + '.', rows[i].task + '.', int(rows[i].deadline.strftime('%d')), rows[i].deadline.strftime('%b'))
            choice = int(input())
            session.delete(rows[choice - 1])
            session.commit()
            print('The task has been deleted!')
            print()
        elif entry == '0':
            print('Bye!')
            break

main()