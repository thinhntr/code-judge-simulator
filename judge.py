import os
import sys
import subprocess
from time import perf_counter
from os import listdir
from os.path import join
from typing import Optional

try:
    # noinspection PyShadowingBuiltins
    from natsort import natsorted as sorted
except ImportError:
    pass


def report(
        filename: str,
        input_text: str,
        user_output_text: str,
        correct_output_text: str,
        user_runtime: float,
        runtime_limit: Optional[int],
        is_rte: bool,
        is_tle: bool,
        verbose: bool = False
):
    """Print test results to screen"""

    if is_rte:
        test_result = 'RTE'
        rte_tests.add(filename)
    elif is_tle:
        test_result = 'TLE'
        tle_tests.add(filename)
    elif user_output_text == correct_output_text:
        test_result = 'PASS'
        pass_tests.add(filename)
    else:
        test_result = 'FAILED'
        failed_tests.add(filename)

    mark = '✅'
    if test_result != 'PASS':
        mark = '❌'

    _MAX_LEN = 42
    _SPACES = 9
    test_filename = 'TEST {}: '.format(filename)
    padding1 = _MAX_LEN - len(test_filename) - _SPACES
    padding2 = _SPACES - len(test_result) - 2

    report_text = ['{}{}{}{}{}\n'.format(test_filename, ' ' * padding1, test_result, ' ' * padding2, mark)]

    # Additional information
    if verbose:
        report_text.append('Input\n{}\n'.format(input_text))
        report_text.append('Correct output\n{}\n'.format(correct_output_text))

        if test_result not in ['TLE']:
            report_text.append('Your output\n{}\n'.format(user_output_text))
            report_text.append("Correct output's length: {}\n".format(len(correct_output_text)))
            report_text.append("Your    output's length: {}\n".format(len(user_output_text)))

        if test_result != 'RTE':
            report_text.append('\nRan in {:.3f} s\n'.format(user_runtime))

        if time_limit:
            report_text.append('Runtime limit: {:.3f}s\n'.format(runtime_limit))

    report_text.append('{}\n'.format('-' * _MAX_LEN))

    print(''.join(report_text), end='')

    return test_result


if __name__ == '__main__':

    try:
        f = open(sys.argv[1])
    except FileNotFoundError:
        print(sys.argv[1] + ' not found')
        raise
    f.close()

    python_file = sys.argv[1]

    test_folder = sys.argv[2]

    try:
        time_limit = float(sys.argv[3])
    except IndexError:
        time_limit = None
    except ValueError:
        time_limit = None

    is_verbose = False
    if sys.argv[-1] == '-v':
        is_verbose = True

    num_inputs = len(os.listdir(os.path.join(test_folder, 'inp')))

    command = ['python', python_file]

    pass_tests = set()
    failed_tests = set()
    rte_tests = set()
    tle_tests = set()
    # Run tests and report
    inp_files_name = sorted(listdir(join(test_folder, 'inp')))
    for test_id in inp_files_name:
        inp = open(join(test_folder, 'inp', test_id))
        out = open(join(test_folder, 'out', test_id))

        correct_output = out.read()

        rte = False
        tle = False
        start = perf_counter()
        try:
            process_output = subprocess.run(
                command,
                stdin=inp,
                check=True,
                text=True,
                capture_output=True,
                timeout=time_limit
            ).stdout
        except subprocess.CalledProcessError as exc:
            rte = True
            process_output = exc.stderr
        except subprocess.TimeoutExpired:
            tle = True
            process_output = ''

        process_runtime = perf_counter() - start

        inp.seek(0)
        test_input = inp.read()

        return_code = report(
            test_id,
            test_input,
            process_output,
            correct_output,
            process_runtime,
            time_limit,
            rte,
            tle,
            is_verbose
        )

        inp.close()
        out.close()

    with open(os.path.join(test_folder, 'summary.txt'), 'w') as summary:
        pt_len = len(pass_tests)
        ft_len = len(failed_tests)
        rte_len = len(rte_tests)
        tle_len = len(tle_tests)

        total = pt_len + ft_len + rte_len + tle_len

        summary.write("TOTAL TEST(s): {}\n\n".format(total))

        summary.write("{} PASS TEST(s)\n".format(pt_len))

        for filename in sorted(pass_tests):
            summary.write("{} ".format(filename))
        summary.write('\n\n')

        summary.write("{} FAILED TEST(s)\n".format(ft_len))

        for filename in sorted(failed_tests):
            summary.write("{} ".format(filename))
        summary.write('\n\n')

        summary.write("{} RTE TEST(s)\n".format(rte_len))

        for filename in sorted(rte_tests):
            summary.write("{} ".format(filename))
        summary.write('\n\n')

        summary.write("{} TLE TEST(s)\n".format(tle_len))

        for filename in sorted(tle_tests):
            summary.write("{} ".format(filename))
        summary.write('\n\n')
