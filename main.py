import sys

from neurophys.cli import run_query

def main():
    if len(sys.argv) < 3 or sys.argv[1] != "query":
        print('Usage: python main.py query "your seach text"')
        return

    query_text = " ".join(sys.argv[2:])
    run_query(query_text)

if __name__ == "__main__":
    main()