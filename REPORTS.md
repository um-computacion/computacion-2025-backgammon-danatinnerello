# Automated Reports
## Coverage Report
```text
Name               Stmts   Miss  Cover   Missing
------------------------------------------------
core/__init__.py       0      0   100%
core/board.py         52      2    96%   55, 68
core/checker.py       14      0   100%
core/dice.py          24      2    92%   37, 40
core/game.py          28      0   100%
core/player.py        28      1    96%   18
------------------------------------------------
TOTAL                146      5    97%

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
