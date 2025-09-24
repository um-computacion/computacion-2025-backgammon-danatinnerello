# Automated Reports
## Coverage Report
```text
Name               Stmts   Miss  Cover   Missing
------------------------------------------------
cli/__init__.py        0      0   100%
cli/cli.py            90      5    94%   79, 93, 126, 136, 142
core/__init__.py       0      0   100%
core/board.py         94     10    89%   33-35, 52, 56, 77, 80, 84, 88, 103
core/checker.py       14      0   100%
core/dice.py          24      1    96%   40
core/game.py          32      0   100%
core/player.py        30      1    97%   20
------------------------------------------------
TOTAL                284     17    94%

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
