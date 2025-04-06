import random
from typing import List, Set, Tuple
import re

class CustomRegexParser:
    def __init__(self, max_repetitions: int = 5):
        self.max_repetitions = max_repetitions
        self.processing_steps = []

    def parse(self, regex: str) -> List[str]:
        self.processing_steps = []
        self._add_step(f"Starting to parse custom regex: {regex}")
        return self._generate_strings(regex)

    def _add_step(self, step: str):
        self.processing_steps.append(step)

    def _find_matching_parenthesis(self, regex: str, open_pos: int) -> int:
        stack = 1
        for i in range(open_pos + 1, len(regex)):
            if regex[i] == '(':
                stack += 1
            elif regex[i] == ')':
                stack -= 1
                if stack == 0:
                    return i
        return -1

    def _process_alternation(self, content: str) -> List[str]:
        if '|' not in content:
            return [content]
        options = content.split('|')
        self._add_step(f"Split alternation into options: {options}")
        return options

    def _generate_strings(self, regex: str) -> List[str]:
        position = 0
        strings = [""]

        while position < len(regex):
            char = regex[position]

            if char == '(':
                group_end = self._find_matching_parenthesis(regex, position)
                if group_end == -1:
                    self._add_step(f"Error: Unmatched parenthesis at position {position}")
                    return []
                group_content = regex[position+1:group_end]
                self._add_step(f"Processing group: {group_content}")
                options = self._process_alternation(group_content)
                self._add_step(f"Alternation options: {options}")
                next_pos = group_end + 1
                power_operator = None
                power_value = None

                if next_pos < len(regex) and regex[next_pos] in ['^', '+']:
                    power_operator = regex[next_pos]
                    if power_operator == '^' and next_pos + 1 < len(regex) and regex[next_pos + 1].isdigit():
                        power_value = int(regex[next_pos + 1])
                        position = next_pos + 2
                        self._add_step(f"Found power operator: {power_operator}{power_value}")
                    else:
                        power_value = 1
                        position = next_pos + 1
                        self._add_step(f"Found power operator: {power_operator} (interpreted as power of 1)")
                else:
                    position = group_end + 1

                new_strings = []
                for s in strings:
                    if power_operator in ['^', '+'] and power_value is not None:
                        for option in options:
                            new_strings.append(s + option * power_value)
                    else:
                        for option in options:
                            new_strings.append(s + option)
                strings = new_strings

            elif position + 1 < len(regex) and regex[position + 1] == '*':
                char_to_repeat = regex[position]
                self._add_step(f"Processing character with zero or more (*): {char_to_repeat}")
                new_strings = []
                for s in strings:
                    repetitions = random.randint(0, self.max_repetitions)
                    self._add_step(f"Applying zero or more (*) with {repetitions} repetitions")
                    new_strings.append(s + char_to_repeat * repetitions)
                strings = new_strings
                position += 2

            elif position + 1 < len(regex) and regex[position + 1] in ['^', '+']:
                char_to_repeat = regex[position]
                power_operator = regex[position + 1]

                if power_operator == '^' and position + 2 < len(regex) and regex[position + 2].isdigit():
                    power_value = int(regex[position + 2])
                    self._add_step(f"Processing single character with power: {char_to_repeat}{power_operator}{power_value}")
                    new_strings = []
                    for s in strings:
                        new_strings.append(s + char_to_repeat * power_value)
                    strings = new_strings
                    position += 3
                else:
                    self._add_step(f"Processing single character with power: {char_to_repeat}{power_operator} (interpreted as power of 1)")
                    new_strings = []
                    for s in strings:
                        new_strings.append(s + char_to_repeat)
                    strings = new_strings
                    position += 2

            else:
                self._add_step(f"Adding literal character: {char}")
                strings = [s + char for s in strings]
                position += 1

        self._add_step(f"Finished parsing regex, generated {len(strings)} valid string(s)")
        return strings

    def show_processing_steps(self):
        print("Regular Expression Processing Steps:")
        for i, step in enumerate(self.processing_steps, 1):
            print(f"{i}. {step}")

    def generate_all_valid_combinations(self, regex: str, max_samples: int = 10) -> List[str]:
        self._add_step(f"Generating all valid combinations for regex: {regex}")
        result = []
        parts = []
        i = 0
        while i < len(regex):
            if regex[i] == '(':
                end_pos = self._find_matching_parenthesis(regex, i)
                if end_pos == -1:
                    i += 1
                    continue
                group_content = regex[i+1:end_pos]
                options = self._process_alternation(group_content)
                next_pos = end_pos + 1
                if next_pos < len(regex) and regex[next_pos] == '^' and next_pos + 1 < len(regex) and regex[next_pos + 1].isdigit():
                    power = int(regex[next_pos + 1])
                    parts.append(('group_power', options, power))
                    i = next_pos + 2
                elif next_pos < len(regex) and regex[next_pos] == '+':
                    parts.append(('group_power', options, 1))
                    i = next_pos + 1
                else:
                    parts.append(('group', options))
                    i = end_pos + 1
            elif i + 1 < len(regex) and regex[i + 1] == '*':
                char = regex[i]
                parts.append(('zero_or_more', char))
                i += 2
            elif i + 1 < len(regex) and regex[i + 1] == '^' and i + 2 < len(regex) and regex[i + 2].isdigit():
                char = regex[i]
                power = int(regex[i + 2])
                parts.append(('char_power', char, power))
                i += 3
            elif i + 1 < len(regex) and regex[i + 1] == '+':
                char = regex[i]
                parts.append(('char_power', char, 1))
                i += 2
            else:
                parts.append(('char', regex[i]))
                i += 1

        def generate_combinations(parts_index=0, current=""):
            if parts_index >= len(parts):
                result.append(current)
                return
            part_type = parts[parts_index][0]
            if part_type == 'char':
                generate_combinations(parts_index + 1, current + parts[parts_index][1])
            elif part_type == 'group':
                options = parts[parts_index][1]
                for option in options:
                    if len(result) < max_samples:
                        generate_combinations(parts_index + 1, current + option)
            elif part_type == 'group_power':
                options = parts[parts_index][1]
                power = parts[parts_index][2]
                for option in options:
                    if len(result) < max_samples:
                        generate_combinations(parts_index + 1, current + option * power)
            elif part_type == 'zero_or_more':
                char = parts[parts_index][1]
                for count in range(min(4, self.max_repetitions + 1)):
                    if len(result) < max_samples:
                        generate_combinations(parts_index + 1, current + char * count)
            elif part_type == 'char_power':
                char = parts[parts_index][1]
                power = parts[parts_index][2]
                generate_combinations(parts_index + 1, current + char * power)

        generate_combinations()
        if len(result) > max_samples:
            result = result[:max_samples]
            self._add_step(f"Limited to {max_samples} combinations")
        self._add_step(f"Generated {len(result)} valid combinations")
        return result


def main():
    parser = CustomRegexParser(max_repetitions=5)
    regex_patterns = [
        "(S|T)(U|V)w*y+24",
        "L(M|N)O^3P*Q(2|3)",
        "R*S(T|U|V)W(x|y|z)^2"
    ]
    print("Custom Regular Expression Generator\n")
    for i, pattern in enumerate(regex_patterns, 1):
        print(f"\nPattern {i}: {pattern}")
        print("-" * 40)
        valid_strings = parser.parse(pattern)
        if valid_strings:
            print(f"Random valid string: {valid_strings[0]}")
        else:
            print("Failed to generate valid string")
        all_combinations = parser.generate_all_valid_combinations(pattern)
        print(f"\nSample of valid combinations:")
        for j, combo in enumerate(all_combinations[:5], 1):
            print(f"  {j}. {combo}")
        print("\nProcessing steps:")
        parser.show_processing_steps()
        print("=" * 50)

if __name__ == "__main__":
    main()
