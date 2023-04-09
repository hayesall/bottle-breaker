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

1. Login, and make a post as a *different* user. e.g.: If you are logged in as `alice`, make a post as `bob`. (*Hint*: Inspect the HTML around the post.)
2. Open two browser windows (e.g. Chrome and Firefox, or Chrome + Chrome Incognito), and log in as two different users. e.g.: `alice` and `bob`. Make a post as `alice` that executes JavaScript code when `bob` logs in.
3. Delete a post made by another user.

## Legal Points

### Disclaimer

This project is for educational purposes only. Understanding how exploits work is important, but you should not use this information to attack websites without the owner's consent. I am not responsible for damage you cause, and this knowledge should be applied toward preventing attacks, not launching them.

I live in the United States, and I am not a lawyer. For others in the United States, computer "hacking" is broadly defined and possibly punishable under the terms specified in the *Computer Fraud and Abuse Act* and related policy. Your local jurisdiction may have different terms, depending on the state or country where you reside.

**Related readings for people in the United States**:

- https://www.justice.gov/jm/jm-9-48000-computer-fraud
- https://www.law.cornell.edu/uscode/text/18/1030

### License

This project is available under the terms of the MIT License or Apache 2.0 License, at your choosing. See the `LICENSE-MIT` or `LICENSE-APACHE` files for more information.
