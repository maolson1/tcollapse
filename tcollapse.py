import re
import sys

def collapse_groups(file_path, collapse_patterns, remove_patterns, uncollapse_groups):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        collapse_patterns = [re.compile(pattern) for pattern in collapse_patterns]
        remove_patterns = [re.compile(pattern) for pattern in remove_patterns]

        collapsed_lines = []
        group_count = 0
        in_group = False

        for line in lines:
            if any(p.search(line) for p in remove_patterns):
                continue
            elif any(p.search(line) for p in collapse_patterns):
                if not in_group:
                    in_group = True
                if group_count in uncollapse_groups:
                    collapsed_lines.append(line.rstrip())
            else:
                if in_group:
                    in_group = False
                    if group_count not in uncollapse_groups:
                        collapsed_lines.append(f"<<< collapsed # {group_count} >>>")
                    group_count += 1
                collapsed_lines.append(line.rstrip())

        print("\n".join(collapsed_lines))

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tcollapse.py <file_path> [-c <collapse_regex>]... [-r <remove_regex>]... [-u <uncollapse_group>]...")
        sys.exit(1)

    file_path = sys.argv[1]
    collapse_patterns = []
    remove_patterns = []
    uncollapse_groups = set()

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

    collapse_groups(file_path, collapse_patterns, remove_patterns, uncollapse_groups)
