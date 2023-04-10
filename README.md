# bottle-breaker

*A small flask application to demonstrate potential security vulnerabilities that may come up when writing web applications. i.e.: cross-site scripting (XSS) vulnerabilities and SQL injection attacks.*

## Setup and run

1. Clone the repository

```bash
git clone https://github.com/hayesall/bottle-breaker.git
cd bottle-breaker
```

2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

## Scavenger Hunt

### 1. Make a post as a *different* user


<details>
<summary><strong>Problem 1 Hints</strong></summary>

<details>
<summary>Hint #1</summary>

The post form on the home page is vulnerable. View page source, read how the `POST` method works, and see if you can make a post as a different user.

</details>

</details>

---

### 2. Trigger JavaScript to execute when users view a post

---

### 3. Delete a post made by another user

You can do this without SQL injection.

<details>
<summary><strong>Problem 3 Hints</strong></summary>

<details>
<summary>Hint #1</summary>

The `delete_post` method in `app.py` is vulnerable. Go to your profile, view page source, and figure out how the form submission works.

</details>

</details>

---

### 4. Use an SQL injection attack to drop the `posts` table

<details>
<summary><strong>Problem 4 Hints</strong></summary>

<details>
<summary>Hint #1</summary>

In SQL, `--` is a comment, meaning that everything after `--` is ignored by the parser.

```sql
DROP TABLE posts; -- This is a comment, everything after the double-dash is ignored
```

</details>

<details>
<summary>Hint #2</summary>

The architecture of an SQL injection attack is to write a query that is (1) valid SQL and passes the server's input validation and the database's query parser, but (2) does something unexpected.

For example, if we have a query that normally inserts a name into a table:

```sql
INSERT INTO users (username) VALUES ('alice');
```

... consider what would happen if `alice` was replaced with `alice'); DROP TABLE posts; -- `. The resulting query would be:

```sql
INSERT INTO users (username) VALUES ('alice'); DROP TABLE posts; -- ');
```

</details>


<details>
<summary>Hint #3</summary>

This site uses SQLite, which is normally built around the `sql.execute()` method. This takes a string as input and executes it as a query.

This method has some built-in security. For example: if you try to execute a query that contains a semicolon (i.e., multiple statements), it will fail with something like:

```python
sqlite3.Warning: You can only execute one statement at a time.
```

If you have a local copy of the code, try finding *which line might be vulnerable* by grepping for a line of code that contains a non-standard execute call:

```bash
git grep -n 'self.curr.execute'
```

`git grep -n` returns the file and line number for each match.

</details>


<details>
<summary>Solution</summary>

Hints 1/2/3 should lead you toward the `/settings` page and "Change Username" form. The form is vulnerable to SQL injection because the `change_username` methods uses a dangerous pattern:

```python
script = f"PRAGMA foreign_keys = ON; UPDATE users SET username = '{new_username}' WHERE username = '{old_username}';"
self.curr.executescript(script)
```

This is vulnerable because the `executescript` method allows multiple statements to be executed at once. If we can insert a semicolon into the `new_username` field and use our knowledge of our `old_username`, we can write a query that drops the `posts` table:

```
alice2' WHERE username = 'alice'; DROP TABLE posts; --
```

</details>


</details>

---

## Legal Points

### Disclaimer

This project is for educational purposes only. Understanding how exploits work is important, but you should not use this information to attack websites without the owner's consent. I am not responsible for damage you cause, and this knowledge should be applied toward preventing attacks, not launching them.

I live in the United States, and I am not a lawyer. For others in the United States, computer "hacking" is broadly defined and possibly punishable under the terms specified in the *Computer Fraud and Abuse Act* and related policy. Your local jurisdiction may have different terms, depending on the state or country where you reside.

**Related readings for people in the United States**:

- https://www.justice.gov/jm/jm-9-48000-computer-fraud
- https://www.law.cornell.edu/uscode/text/18/1030

### License

This project is available under the terms of the MIT License or Apache 2.0 License, at your choosing. See the `LICENSE-MIT` or `LICENSE-APACHE` files for more information.
