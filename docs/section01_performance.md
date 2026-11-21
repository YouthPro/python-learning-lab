# Section 01: Advanced performance assessment

All 30 problems have two separate, opt-in checks labelled **Advanced Time Tests** and **Advanced Memory Tests**. Exercise solutions remain TODOs; no implementation is substituted for your submission.

## Get your submission results

From the repository root, with the existing virtual environment active:

```bash
# One problem, by name or ID
python scripts/assess_section01.py --problem two_sum
python scripts/assess_section01.py --problem 04

# Several problems, or all 30
python scripts/assess_section01.py --problem two_sum moving_average read_lines
python scripts/assess_section01.py
```

The grader prints a table and writes `datasets/processed/section01_assessment/results.json` and `results.md`. Use `--output PATH` to keep different submissions separately. Reports record a UTC timestamp, interpreter/platform, exact limits, individual samples, and SHA-256 hashes of the exercise modules. No extra dependencies are needed beyond the existing pytest environment.

Each row contains:

- **Correctness:** status and number of existing correctness cases passed / cases selected, including boundary tests. The existing three correctness modules run with `--strict-exercises`; xfail and skipped tests cannot produce a correctness pass.
- **Advanced Time Tests:** measured seconds / required seconds, their ratio, and status.
- **Advanced Memory Tests:** measured MiB / required MiB, their ratio, and status. JSON stores the precise byte values.
- **Overall:** PASS only when correctness, time, and memory all pass. A fast wrong answer remains a failure.

A ratio of `0.70x` uses 70% of the allowance; `1.20x` is 20% over. Equality at the limit passes. Unimplemented code reports `not_implemented`, with **no invented measurement or zero ratio**. A worker that cannot complete reports its timeout/error instead of a passing result. The command exits 0 only when all selected problems pass; otherwise it exits 1.

After you submit an implementation, run this command or ask the assistant to run it. The resulting report provides the requested correctness, time/required-time, and memory/required-memory feedback for that exact source version.

## Advanced Time Tests

`time.perf_counter()` measures the complete workload. The reported time is the **median of three runs** by default (`--repeats N` overrides this). Inputs are rebuilt and callable `cache_clear()` hooks are called before each sample. Importing the solution, interpreter startup, input/expected-result construction, garbage collection before the call, and result validation are excluded. Normal GC during execution remains enabled. Fibonacci includes a cold query plus repeated cache lookups in each sample.

Generators are fully consumed **inside** the measurement. Their consumers retain only a count, checksum and last item; they do not turn streamed output into a list. Consumer overhead is included in the published allowance. File input is generated locally immediately before measurement, so this tests file-processing code with a warm filesystem cache rather than cold-disk throughput.

Time is measured in a different process from allocation tracing, because tracemalloc can substantially slow Python execution. The time check measures Python's clock, independently of the learner's timer decorator.

## Advanced Memory Tests

`tracemalloc` measures **peak incremental Python allocations during the complete operation**, once in a fresh process. Existing input objects, expected results, imports and input files are excluded. Return values, temporary copies, caches created during execution and streamed values currently being consumed are included. The output remains alive until after the peak is read; validation runs after tracing stops.

This is **not whole-process RSS**, and does not account for arbitrary native-extension allocations. The Section 01 targets are Python/standard-library implementations. Returning an eager list where a generator is required may fail correctness as well as memory. Unavoidable output storage is allowed: matrix transposition and Cartesian products have much larger limits than line readers.

On platforms supporting `resource.RLIMIT_AS`, workers also have a **512 MiB process address-space guard** to protect against accidental explosive allocations. This guard is separate from the graded per-problem memory allowance. Unix operation deadlines and a parent wall-clock watchdog stop runaway implementations; the report distinguishes `timeout`, `worker_timeout`, `memory_guard` and `worker_error`. Parent timeout includes preparation/imports, so it does not pretend to be an exact execution-time measurement.

## Limits and intended complexity

Limits apply to the **whole described workload**, not one scalar call. They are fixed, visible in [cases.py](../phase1_python_programming/section01_data_structures/assessment/cases.py), and intended for 64-bit CPython. Expected complexities describe elementary operations; string lengths, callback costs and integer bit sizes still matter. The additional space column includes required output while excluding the already-created input.

These are advanced efficiency targets, independent of functional correctness. They deliberately expose quadratic scans, repeated window sums, list-based LRU refresh, unbounded cache retention, full-input materialization and unnecessary intermediate collections. Correct solutions with the same asymptotic complexity can still have different constants. A finite stress suite is evidence of efficiency on these inputs, **not a proof of Big-O complexity or a universal ranking of all correct algorithms**.

| ID | Problem | Time limit (s) | Memory limit (MiB) | Workload | Expected time | Expected additional space |
|---|---|---:|---:|---|---|---|
| 01 | `word_frequency` | 0.25 | 2 | 300,000 words, 64 distinct words; large input string | O(characters) | O(vocabulary) |
| 02 | `first_unique_char` | 0.15 | 0.125 | 300,000 repeated characters then one unique character | O(n) | O(alphabet) |
| 03 | `deduplicate` | 0.20 | 12 | 100,000 distinct integers repeated twice | O(n) expected | O(unique + output) |
| 04 | `two_sum` | 0.25 | 18 | 120,000 integers; only solution at final two positions | O(n) expected | O(n) |
| 05 | `group_anagrams` | 0.30 | 10 | 60,000 two-character Unicode words, 30,000 anagram groups | O(n L log L) or O(n L) | O(n + signatures) |
| 06 | `top_k_frequent` | 0.30 | 9 | 100,000 distinct integers twice, request k=10 | O(n + u log k) target | O(u + k) |
| 07 | `merge_intervals` | 0.25 | 12 | 60,000 reversed, disjoint intervals | O(n log n) | O(n + output) |
| 08 | `longest_unique_substring` | 0.30 | 2 | 100,000 Unicode characters, including a run of 10,000 distinct characters | O(n) | O(distinct characters) |
| 09 | `is_valid_parentheses` | 0.20 | 3 | 100,000 opening brackets followed by 100,000 closing brackets | O(n) | O(depth) |
| 10 | `flatten_list` | 0.25 | 5 | 60,000 small nested lists producing 180,000 items | O(nodes + output) | O(depth + output) |
| 11 | `rotate_matrix` | 0.25 | 5 | 600 x 600 matrix, return a new matrix | O(rows x columns) | O(output) |
| 12 | `transpose_matrix` | 0.20 | 5 | 400 x 900 rectangular matrix | O(rows x columns) | O(output) |
| 13 | `moving_average` | 0.25 | 0.25 | 120,000 streamed integers, window=1,024 | O(n) | O(k) |
| 14 | `chunked` | 0.20 | 0.25 | 200,000 streamed integers, batches of 128 | O(n) | O(batch size) |
| 15 | `sliding_window` | 0.25 | 0.25 | 80,000 streamed integers, window=32; consume every tuple | O(n k) including output | O(k) |
| 16 | `merge_sorted` | 0.20 | 0.125 | two one-shot streams containing 100,000 integers each | O(n + m) | O(1) |
| 17 | `binary_insert` | 0.10 | 4 | 200,000 sorted integers, insert in the middle without mutation | O(n) including result copy | O(output) |
| 18 | `parse_log_line` | 0.25 | 0.125 | 20,000 valid log lines plus a 300,000-character malformed line | O(total characters) target | O(line + result) |
| 19 | `extract_emails` | 0.30 | 1 | 50,000 repeated addresses, 32 unique addresses | O(text length) target | O(unique addresses) |
| 20 | `LRUCache` | 0.30 | 2 | capacity 4,096; 30,000 full-capacity refresh/get/put cycles | O(1) expected per operation | O(capacity) |
| 21 | `memoized_fibonacci` | 0.10 | 0.5 | cold F(32), then 1,000 repeated F(32) queries | O(n) additions cold, O(1) cache lookup | O(n) entries; O(n²) cached integer bits |
| 22 | `cartesian_pairs` | 0.20 | 18 | 500 x 500 one-shot inputs, materialize 250,000 pairs | O(n m) | O(output) |
| 23 | `group_consecutive` | 0.20 | 6 | 200,000 streamed integers in 50,000 runs of length four | O(n) | O(number of runs) |
| 24 | `compose` | 0.20 | 0.5 | compose 64 functions and call the result 5,000 times | O(functions) per call | O(functions) |
| 25 | `safe_map` | 0.20 | 5 | 100,000 streamed strings, half valid integers and half invalid | O(n) plus callback cost | O(output) |
| 26 | `timer` | 0.20 | 0.125 | wrap once, then call a trivial callback 50,000 times | O(1) wrapper overhead per call | O(1) per call |
| 27 | `retry` | 0.25 | 0.125 | 10,000 calls; each succeeds on attempt three | O(attempts x callback cost) | O(1) retained state |
| 28 | `iter_file_batches` | 0.25 | 0.5 | two UTF-8 files, 120,000 lines of 64 characters, batches of 128 | O(total file size) | O(batch size x line length) |
| 29 | `read_lines` | 0.20 | 0.125 | UTF-8 file, 120,000 lines of 64 characters | O(total file size) | O(line length) |
| 30 | `custom_sort` | 0.30 | 7 | 100,000 deterministic unordered integers, stable key sorting | O(n log n) | O(n) |

## Run the pytest checks directly

```bash
# Both groups, with the exact labels visible in test IDs
python -m pytest phase1_python_programming/section01_data_structures/tests/test_advanced_performance.py --run-advanced -v

# One group or one problem
python -m pytest phase1_python_programming/section01_data_structures/tests --run-advanced -m advanced_time -v
python -m pytest phase1_python_programming/section01_data_structures/tests --run-advanced -m advanced_memory -v
python -m pytest phase1_python_programming/section01_data_structures/tests/test_advanced_performance.py --run-advanced -k two_sum -v

# TODOs also count as failures
python -m pytest phase1_python_programming/section01_data_structures/tests/test_advanced_performance.py --run-advanced --strict-exercises -v
```

Routine pytest runs skip the 60 stress checks unless `--run-advanced` is present. When explicitly enabled, untouched TODOs remain xfail unless strict mode is also requested. This preserves the existing learning workflow. The submission grader is stricter: unfinished work never counts as a pass.

The JSON/Markdown grader is the recommended way to see **passing** measurements as well as failures. Individual pytest checks attach measurement, required value and ratio as test properties and print them in failure messages; `--junitxml=PATH` can save those properties.

## Hardware adjustments

Close busy applications and run stress tests serially rather than using pytest-xdist. If a slower machine needs a different allowance, choose an explicit time multiplier:

```bash
python scripts/assess_section01.py --problem 04 --time-multiplier 2
python -m pytest phase1_python_programming/section01_data_structures/tests/test_advanced_performance.py --run-advanced --advanced-time-multiplier 2
```

The multiplier changes the required time, is recorded in reports, and never changes memory limits. Do not compare ratios across different multipliers or machines as if the conditions were identical. Default measurements use multiplier 1 and three repetitions.

The correctness subprocess has a 30-second total watchdog (`--correctness-timeout` can change it). If it times out, completed results are preserved; pending cases are `incomplete`. Assess one problem at a time to isolate a hanging implementation. Performance workers still run independently for the selected problems.

## Calibration and verification

On the development environment (64-bit CPython 3.12.3, Linux/WSL2), temporary conventional implementations passed all **30 time + 30 memory** workloads. Exercise files were left unchanged. A measurement snapshot is in [section01_performance_calibration.json](section01_performance_calibration.json); these are calibration measurements, **not your submission's results**.

Less efficient implementations were checked against the same default limits:

| Variant | Measurement | Required | Ratio | Outcome |
|---|---:|---:|---:|---|
| Re-sum the moving-average deque each step | 0.685 s | 0.250 s | 2.74x | time failed |
| Refresh LRU by removing a key from a list | 0.577 s | 0.300 s | 1.92x | time failed |
| Read the whole text before yielding lines | 20.194 MiB | 0.125 MiB | 161.55x | memory failed |
| Materialize all word tokens before counting | 16.217 MiB | 2 MiB | 8.11x | memory failed |
| Materialize all email matches before deduplication | 3.323 MiB | 1 MiB | 3.32x | memory failed |
| Sort all frequency keys before slicing Top K | 11.871 MiB | 9 MiB | 1.32x | memory failed |

These numbers are a development snapshot; your measured times will vary. The assessment infrastructure has independent tests for median calculation, input/validation exclusion, output inclusion, incorrect stress results, eager versus streaming allocation, watchdogs, correctness-test attribution, and complete grading of correct, wrong and unfinished submissions in temporary checkouts.

## References

- [Python perf_counter](https://docs.python.org/3/library/time.html#time.perf_counter)
- [Python tracemalloc](https://docs.python.org/3/library/tracemalloc.html)
- [Python resource limits](https://docs.python.org/3/library/resource.html)
