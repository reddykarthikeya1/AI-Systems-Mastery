# Beginner Playground - PL/SQL, Packages and Triggers

> *"A trigger is a motion-sensor light. Wonderful when you want it. Unnerving when you cannot remember installing it and it keeps coming on."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no
server, no `pip install`, no account to sign up for. You can read it in ten
minutes and run it in one:

```bash
python 00_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints
`All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import sqlite3
```

---

## 1. Logic that lives in the database

PL/SQL is a full programming language running *inside* Oracle. Two reasons it
exists:

1. **Fewer round trips.** Looping in your application means a network trip per
   row. The same loop inside the database means one trip in total.
2. **Rules nobody can skip.** A check in your API is bypassed by anyone with a
   SQL prompt. A check in the database is not.

SQLite has triggers too, so you can watch the mechanism work right here.

```python
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
```

---

## 2. The motion sensor

`FOR EACH ROW` is the phrase that matters. The trigger body runs once per
*changed row*, not once per statement.

```python
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
```

---

## 3. One statement, five hundred hidden writes

Now raise everybody's pay with a single `UPDATE`. You wrote one statement. The
database performs 501 writes.

Nothing is wrong here - this is exactly what you asked for. The danger is that
the cost is invisible at the call site. Someone reading the application code sees
one cheap-looking `UPDATE`.

```python
before = hr.execute("SELECT COUNT(*) FROM salary_audit").fetchone()[0]
hr.execute("UPDATE employee SET salary = salary + 500")
hr.commit()
after = hr.execute("SELECT COUNT(*) FROM salary_audit").fetchone()[0]

print(f"audit rows before: {before}, after one UPDATE statement: {after}")
assert after - before == 500, "the trigger fired once per row, not once per statement"
print("One line of SQL. Five hundred trigger executions.")
```

---

## 4. Why packages exist

A **package** groups related procedures behind a declared interface: a
specification (what callers may use) and a body (how it works). You can rewrite
the body without breaking a single caller.

It is the same idea as a module in any language - and the same discipline. The
alternative, a few hundred standalone procedures with names like
`UPD_EMP_SAL_V2_FINAL`, is a real thing you will meet in a real system.

```python
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
```

---

## 5. Predict before you run

One `UPDATE` statement changes 500 rows, and there is an `AFTER UPDATE ...
FOR EACH ROW` trigger on the table. How many times does the trigger body run -
once, or 500 times? How many audit rows appear?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

Triggers give you an audit trail nobody can bypass - not even someone with a
direct SQL prompt. They also make a one-line `UPDATE` do arbitrary hidden work,
which is why "the deploy was fine but the batch job now takes four hours" so
often ends at a trigger.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
