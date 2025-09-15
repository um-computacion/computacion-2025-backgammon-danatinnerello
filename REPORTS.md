# Automated Reports
## Coverage Report
```text
Name               Stmts   Miss  Cover   Missing
------------------------------------------------
cli/__init__.py        0      0   100%
cli/cli.py            70     11    84%   48, 62, 87, 93-103, 108
core/__init__.py       0      0   100%
core/board.py         70      4    94%   58, 71, 90, 96
core/checker.py       14      0   100%
core/dice.py          24      1    96%   40
core/game.py          32      0   100%
core/player.py        30      1    97%   20
------------------------------------------------
TOTAL                240     17    93%

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
