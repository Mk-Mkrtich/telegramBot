import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from db.migrations.driver_migration import create_driver_table

def main():
    create_driver_table()

if __name__ == "__main__":
    main()
