#!/usr/bin/env python3
import re
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tcollapse.py <file_path> [-c <collapse_regex>]... [-r <remove_regex>]... [-u <uncollapse_group>]...")
        sys.exit(1)

    remove_patterns = []
    collapse_patterns = []
    uncollapse_groups = set()

    file_path = sys.argv[1]
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "-c" and i + 1 < len(args):
            collapse_patterns.append(args[i + 1])
            i += 2
        elif args[i] == "-r" and i + 1 < len(args):
            remove_patterns.append(args[i + 1])
            i += 2
        elif args[i] == "-u" and i + 1 < len(args):
            try:
                uncollapse_groups.add(int(args[i + 1]))
            except ValueError:
                print(f"Invalid uncollapse group number: {args[i + 1]}")
                sys.exit(1)
            i += 2
        else:
            print(f"Unexpected argument: {args[i]}")
            sys.exit(1)

    collapse_patterns = [re.compile(pattern) for pattern in collapse_patterns]
    remove_patterns = [re.compile(pattern) for pattern in remove_patterns]

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        collapsed_lines = []
        group_id = 0
        in_group = False
        lines_in_group = 0

        for l in lines:
            if any(p.search(l) for p in remove_patterns):
                continue
            elif any(p.search(l) for p in collapse_patterns):
                if not in_group:
                    in_group = True
                    lines_in_group = 1
                else:
                    lines_in_group += 1
                if group_id in uncollapse_groups:
                    collapsed_lines.append(l.rstrip())
            else:
                if in_group:
                    if group_id not in uncollapse_groups:
                        collapsed_lines.append(f"<< {lines_in_group} line(s) #{group_id} >>")
                    in_group = False
                    lines_in_group = 0
                    group_id += 1
                collapsed_lines.append(l.rstrip())
        if in_group:
            if group_id not in uncollapse_groups:
                collapsed_lines.append(f"<< {lines_in_group} line(s) #{group_id} >>")

        print("\n".join(collapsed_lines))

    except Exception as e:
        print(f"Error: {e}")
