
import re

robert = 'Robert'
rubin = 'Rubin'
ashcraft = 'Ashcraft'
doogie = 'Doogie'
muggle = 'Muggle'

# Keep the first letter of the name, and drop all occurrences of non-initial a, e, h, i, o, u, w, y
robert = 'Rbrt'
rubin = 'Rbn'
ashcraft = 'Ascrft'
doogie = 'Dg'
muggle = 'Mggl'

# Replace the remaining letters with the following numbers:
# b, f, p, v→ 1
# c, g, j, k, q, s, x, z → 2
# d, t → 3
# l → 4
# m, n→ 5
# r → 6
robert = 'R163'
rubin wft = 'A22613'
doogie = 'D2'
muggle = 'M224'

# Replace any sequences of identical numbers , only if they derive from two
# or more letters that were adjacent in the original name, with a single number
# (i.e., 666→ 6).
robert = 'R163'
rubin = 'R15'
ashcraft = 'A2613'
doogie = 'D2'
muggle = 'M224'


# Convert to the form Letter Digit Digit Digit by dropping digits
# past the third (if necessary) or padding with trailing zeros (if necessary).
robert = 'R163'
rubin = 'R150'
ashcraft = 'A261'
doogie = 'D200'
muggle = 'M224'