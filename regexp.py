from re import compile, RegexFlag

class RegularExpressions:
    regexps = {
        'blank_line': compile("^\\s+$", flags=RegexFlag.IGNORECASE | RegexFlag.MULTILINE),
        'comment': compile("#.*$", flags=RegexFlag.IGNORECASE | RegexFlag.MULTILINE),
        'statements': compile("^(\\s*)(\\w+):\\s*(.*)$", flags=RegexFlag.IGNORECASE | RegexFlag.MULTILINE)
    }
