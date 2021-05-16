'''
Build a fresh install of MoNoA
'''
from database.db_init import db_init

def build() -> None:
    ''' Initialize database '''
    db_init()

if __name__ == '__main__':
    build()
