# Automated Reports
## Coverage Report
```text
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
cli/__init__.py             0      0   100%
cli/cli.py                 66      5    92%   31-32, 84-85, 99
core/__init__.py            0      0   100%
core/board.py             106     13    88%   37-39, 56, 61, 89, 93, 95, 100, 113, 120-122
core/checker.py            14      0   100%
core/dice.py               24      1    96%   40
core/excepcions.py         16      0   100%
core/game.py               96     11    89%   60-67, 82, 93-95, 103
core/player.py             21      2    90%   17, 20
pygame_ui/__init__.py       0      0   100%
-----------------------------------------------------
TOTAL                     343     32    91%

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
