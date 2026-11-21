"""Public stress-test budgets. These are advanced targets, not correctness requirements."""

from dataclasses import dataclass

MIB = 1024 * 1024
SECTION = "phase1_python_programming.section01_data_structures"


@dataclass(frozen=True)
class Case:
    id: str
    name: str
    module: str
    seconds: float
    memory_mib: float
    workload: str
    expected_time: str
    expected_space: str
    aliases: tuple[str, ...] = ()

    @property
    def target_module(self) -> str:
        return f"{SECTION}.exercises.{self.module}"

    @property
    def tests(self) -> tuple[str, ...]:
        return (f"test_{self.name}", *self.aliases)


# Seconds are for a complete workload (including iterator consumption), not one call.
CASES = (
    Case(
        "01",
        "word_frequency",
        "basic_structures",
        0.25,
        2,
        "300,000 words, 64 distinct words; large input string",
        "O(characters)",
        "O(vocabulary)",
    ),
    Case(
        "02",
        "first_unique_char",
        "basic_structures",
        0.15,
        0.125,
        "300,000 repeated characters then one unique character",
        "O(n)",
        "O(alphabet)",
    ),
    Case(
        "03",
        "deduplicate",
        "basic_structures",
        0.20,
        12,
        "100,000 distinct integers repeated twice",
        "O(n) expected",
        "O(unique + output)",
    ),
    Case(
        "04",
        "two_sum",
        "basic_structures",
        0.25,
        18,
        "120,000 integers; only solution at final two positions",
        "O(n) expected",
        "O(n)",
    ),
    Case(
        "05",
        "group_anagrams",
        "basic_structures",
        0.30,
        10,
        "60,000 two-character Unicode words, 30,000 anagram groups",
        "O(n L log L) or O(n L)",
        "O(n + signatures)",
    ),
    Case(
        "06",
        "top_k_frequent",
        "basic_structures",
        0.30,
        9,
        "100,000 distinct integers twice, request k=10",
        "O(n + u log k) target",
        "O(u + k)",
    ),
    Case(
        "07",
        "merge_intervals",
        "basic_structures",
        0.25,
        12,
        "60,000 reversed, disjoint intervals",
        "O(n log n)",
        "O(n + output)",
    ),
    Case(
        "08",
        "longest_unique_substring",
        "basic_structures",
        0.30,
        2,
        "100,000 Unicode characters, including a run of 10,000 distinct characters",
        "O(n)",
        "O(distinct characters)",
    ),
    Case(
        "09",
        "is_valid_parentheses",
        "basic_structures",
        0.20,
        3,
        "100,000 opening brackets followed by 100,000 closing brackets",
        "O(n)",
        "O(depth)",
    ),
    Case(
        "10",
        "flatten_list",
        "basic_structures",
        0.25,
        5,
        "60,000 small nested lists producing 180,000 items",
        "O(nodes + output)",
        "O(depth + output)",
    ),
    Case(
        "11",
        "rotate_matrix",
        "basic_structures",
        0.25,
        5,
        "600 x 600 matrix, return a new matrix",
        "O(rows x columns)",
        "O(output)",
        ("test_rotate_invalid",),
    ),
    Case(
        "12",
        "transpose_matrix",
        "basic_structures",
        0.20,
        5,
        "400 x 900 rectangular matrix",
        "O(rows x columns)",
        "O(output)",
        ("test_transpose_invalid",),
    ),
    Case(
        "13",
        "moving_average",
        "advanced_structures",
        0.25,
        0.25,
        "120,000 streamed integers, window=1,024",
        "O(n)",
        "O(k)",
        ("test_moving_average_invalid",),
    ),
    Case(
        "14",
        "chunked",
        "advanced_structures",
        0.20,
        0.25,
        "200,000 streamed integers, batches of 128",
        "O(n)",
        "O(batch size)",
        ("test_chunked_invalid",),
    ),
    Case(
        "15",
        "sliding_window",
        "advanced_structures",
        0.25,
        0.25,
        "80,000 streamed integers, window=32; consume every tuple",
        "O(n k) including output",
        "O(k)",
        ("test_sliding_window_invalid",),
    ),
    Case(
        "16",
        "merge_sorted",
        "advanced_structures",
        0.20,
        0.125,
        "two one-shot streams containing 100,000 integers each",
        "O(n + m)",
        "O(1)",
        ("test_merge_sorted_can_consume_infinite_streams",),
    ),
    Case(
        "17",
        "binary_insert",
        "advanced_structures",
        0.10,
        4,
        "200,000 sorted integers, insert in the middle without mutation",
        "O(n) including result copy",
        "O(output)",
        ("test_binary_insert_preserves_input",),
    ),
    Case(
        "18",
        "parse_log_line",
        "advanced_structures",
        0.25,
        0.125,
        "20,000 valid log lines plus a 300,000-character malformed line",
        "O(total characters) target",
        "O(line + result)",
    ),
    Case(
        "19",
        "extract_emails",
        "advanced_structures",
        0.30,
        1,
        "50,000 repeated addresses, 32 unique addresses",
        "O(text length) target",
        "O(unique addresses)",
    ),
    Case(
        "20",
        "LRUCache",
        "advanced_structures",
        0.30,
        2,
        "capacity 4,096; 30,000 full-capacity refresh/get/put cycles",
        "O(1) expected per operation",
        "O(capacity)",
        ("test_lru_cache", "test_lru_invalid"),
    ),
    Case(
        "21",
        "memoized_fibonacci",
        "advanced_structures",
        0.10,
        0.5,
        "cold F(32), then 1,000 repeated F(32) queries",
        "O(n) additions cold, O(1) cache lookup",
        "O(n) entries; O(n²) cached integer bits",
        ("test_fibonacci", "test_fibonacci_negative", "test_fibonacci_uses_cache"),
    ),
    Case(
        "22",
        "cartesian_pairs",
        "advanced_structures",
        0.20,
        18,
        "500 x 500 one-shot inputs, materialize 250,000 pairs",
        "O(n m)",
        "O(output)",
    ),
    Case(
        "23",
        "group_consecutive",
        "iterators_generators",
        0.20,
        6,
        "200,000 streamed integers in 50,000 runs of length four",
        "O(n)",
        "O(number of runs)",
    ),
    Case(
        "24",
        "compose",
        "iterators_generators",
        0.20,
        0.5,
        "compose 64 functions and call the result 5,000 times",
        "O(functions) per call",
        "O(functions)",
    ),
    Case(
        "25",
        "safe_map",
        "iterators_generators",
        0.20,
        5,
        "100,000 streamed strings, half valid integers and half invalid",
        "O(n) plus callback cost",
        "O(output)",
    ),
    Case(
        "26",
        "timer",
        "iterators_generators",
        0.20,
        0.125,
        "wrap once, then call a trivial callback 50,000 times",
        "O(1) wrapper overhead per call",
        "O(1) per call",
    ),
    Case(
        "27",
        "retry",
        "iterators_generators",
        0.25,
        0.125,
        "10,000 calls; each succeeds on attempt three",
        "O(attempts x callback cost)",
        "O(1) retained state",
        ("test_retry_exhausted", "test_retry_invalid"),
    ),
    Case(
        "28",
        "iter_file_batches",
        "iterators_generators",
        0.25,
        0.5,
        "two UTF-8 files, 120,000 lines of 64 characters, batches of 128",
        "O(total file size)",
        "O(batch size x line length)",
        ("test_file_batches", "test_batches_cross_file", "test_batches_invalid"),
    ),
    Case(
        "29",
        "read_lines",
        "iterators_generators",
        0.20,
        0.125,
        "UTF-8 file, 120,000 lines of 64 characters",
        "O(total file size)",
        "O(line length)",
    ),
    Case(
        "30",
        "custom_sort",
        "iterators_generators",
        0.30,
        7,
        "100,000 deterministic unordered integers, stable key sorting",
        "O(n log n)",
        "O(n)",
    ),
)
BY_ID = {case.id: case for case in CASES}
BY_NAME = {case.name: case for case in CASES}


def select_cases(problems: list[str] | None = None) -> list[Case]:
    if not problems:
        return list(CASES)
    selected = set()
    for value in problems:
        key = value.zfill(2) if value.isdigit() else value
        case = BY_ID.get(key) or BY_NAME.get(key)
        if case is None:
            raise ValueError(f"Unknown Section 01 problem: {value}")
        selected.add(case.id)
    return [case for case in CASES if case.id in selected]
