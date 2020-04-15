from re import compile, RegexFlag


class RegularExpressions:
    regexps = {
        'blank_line': r'^\s*$',
        'comment': r'#.*',
        'line_break': r'\n',
        'statements': compile("^(\\s*)(\\w+):\\s*(.*)$", flags=RegexFlag.IGNORECASE | RegexFlag.MULTILINE)
    }
