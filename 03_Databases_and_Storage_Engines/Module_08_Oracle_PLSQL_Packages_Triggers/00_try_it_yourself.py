"""Beginner playground for Module 08 - PL/SQL, Packages and Triggers.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_W3_BEGINNER_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import sqlite3

# ---------------------------------------- 1. Logic that lives in the database
hr = sqlite3.connect(":memory:")
hr.execute("CREATE TABLE employee (id INTEGER PRIMARY KEY, name TEXT, salary INTEGER)")
hr.execute('''
    CREATE TABLE salary_audit (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id   INTEGER,
        old_pay  INTEGER,
        new_pay  INTEGER
    )
''')
hr.executemany("INSERT INTO employee VALUES (?, ?, ?)",
               [(i, f"employee{i}", 50_000) for i in range(1, 501)])
hr.commit()
print("employees on file:", hr.execute("SELECT COUNT(*) FROM employee").fetchone()[0])


# ------------------------------------------------------- 2. The motion sensor
hr.execute('''
    CREATE TRIGGER audit_salary_change
    AFTER UPDATE OF salary ON employee
    FOR EACH ROW
    BEGIN
        INSERT INTO salary_audit (emp_id, old_pay, new_pay)
        VALUES (OLD.id, OLD.salary, NEW.salary);
    END
''')

hr.execute("UPDATE employee SET salary = salary + 1000 WHERE id = 7")
hr.commit()
trail = hr.execute("SELECT emp_id, old_pay, new_pay FROM salary_audit").fetchall()
print("audit trail after one change:", trail)
assert trail == [(7, 50_000, 51_000)], "nobody had to remember to write this row"


# ------------------------------- 3. One statement, five hundred hidden writes
before = hr.execute("SELECT COUNT(*) FROM salary_audit").fetchone()[0]
hr.execute("UPDATE employee SET salary = salary + 500")
hr.commit()
after = hr.execute("SELECT COUNT(*) FROM salary_audit").fetchone()[0]

print(f"audit rows before: {before}, after one UPDATE statement: {after}")
assert after - before == 500, "the trigger fired once per row, not once per statement"
print("One line of SQL. Five hundred trigger executions.")


# ------------------------------------------------------ 4. Why packages exist
class PayrollPackage:
    # Public: what callers are allowed to touch.
    def give_raise(self, emp_id, amount):
        if amount <= 0:
            raise ValueError("a raise must be positive")
        self._write(emp_id, amount)

    # Private: free to change, because nothing outside calls it.
    def _write(self, emp_id, amount):
        hr.execute("UPDATE employee SET salary = salary + ? WHERE id = ?", (amount, emp_id))
        hr.commit()


payroll = PayrollPackage()
payroll.give_raise(7, 2_000)
final_pay = hr.execute("SELECT salary FROM employee WHERE id = 7").fetchone()[0]
print("employee 7 final salary:", final_pay)
assert final_pay == 53_500, "50000 + 1000 + 500 + 2000"

try:
    payroll.give_raise(7, -100)
    raise AssertionError("the interface should have refused that")
except ValueError as exc:
    print("refused by the package interface:", exc)


print()
print("All checks passed.")
