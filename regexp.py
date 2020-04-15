class RegularExpressions:
    regexps = {
        'blank_line': r'^\s*$',
        'comment': r'#.*',
        'line_break': r'\n',
        'statement': r'^(\s*)(\w+):\s*(.*)$'
    }
