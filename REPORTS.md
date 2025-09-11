# Automated Reports
## Coverage Report
```text
Name               Stmts   Miss  Cover   Missing
------------------------------------------------
cli/__init__.py        0      0   100%
core/__init__.py       0      0   100%
core/board.py         55      2    96%   58, 71
core/checker.py       14      0   100%
core/dice.py          24      2    92%   37, 40
core/game.py          32      2    94%   33, 42
core/player.py        30      2    93%   17, 20
------------------------------------------------
TOTAL                155      8    95%

```
## Pylint Report
```text
************* Module .pylintrc
.pylintrc:1:0: F0011: error while parsing the configuration: While reading from '.pylintrc' [line 59]: section 'REPORTS' already exists (config-parse-error)
************* Module main.py
main.py:1:0: F0001: No module named main.py (fatal)
************* Module test.py
test.py:1:0: F0001: No module named test.py (fatal)

```
