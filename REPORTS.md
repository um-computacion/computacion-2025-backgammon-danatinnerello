# Automated Reports
## Coverage Report
```text
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
cli/__init__.py          0      0   100%
cli/cli.py              62      5    92%   31-32, 80-81, 95
core/__init__.py         0      0   100%
core/board.py          106     13    88%   37-39, 56, 61, 89, 93, 95, 100, 113, 120-122
core/checker.py         14      0   100%
core/dice.py            24      1    96%   40
core/excepcions.py      16      0   100%
core/game.py            91     14    85%   58-61, 71, 74-77, 84-88, 96
core/player.py          21      2    90%   17, 20
--------------------------------------------------
TOTAL                  334     35    90%

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
