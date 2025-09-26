# Automated Reports
## Coverage Report
```text
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
cli/__init__.py          0      0   100%
cli/cli.py              62      5    92%   31-32, 80-81, 95
core/__init__.py         0      0   100%
core/board.py          100     11    89%   33-35, 52, 56, 84, 88, 101, 108-110
core/checker.py         14      0   100%
core/dice.py            24      1    96%   40
core/excepcions.py      16      0   100%
core/game.py            72     11    85%   28, 31, 58-61, 69-71, 79, 92
core/player.py          21      2    90%   17, 20
--------------------------------------------------
TOTAL                  309     30    90%

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
