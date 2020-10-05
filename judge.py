import os
import sys
import subprocess
from time import perf_counter
from os import listdir
from os.path import join


def report(
        test_id,
        user_output,
        correct_output,
        user_runtime,
        time_limit,
        rte,
        tle,
        verbose=False
):
    '''
        Print test results to screen
    '''
    report_text = []

    MAX_LEN = 42

    report_text.append('-' * MAX_LEN)
    report_text.append('\n')

    report_text.append('TEST {}: '.format(test_id))
    len_so_far = len(report_text[-1])

    if rte:
        return_code = 'RTE'
    elif tle:
        return_code = 'TLE'
    elif user_output == correct_output:
        return_code = 'PASS'
    else:
        return_code = 'FAILED'

    LEFT_MARGIN = 9
    padding = MAX_LEN - len_so_far - LEFT_MARGIN

    report_text.append(' ' * padding)
    report_text.append(return_code)

    len_so_far += padding
    len_so_far += len(return_code)
    padding = MAX_LEN - len_so_far - 2

    report_text.append(' ' * padding)

    mark = '✅'
    if return_code != 'PASS':
        mark = '❌'

    report_text.append(mark)
    report_text.append('\n')

    # Additional information
    if verbose:
        if return_code not in ['PASS', 'RTE', 'TLE']:
            report_text.append('Correct output\n')
            report_text.append(correct_output)
            report_text.append('\n')

            report_text.append('Your output\n')
            report_text.append(process_output)
            report_text.append('\n')

            report_text.append('Correct output\'s length: ' +
                               str(len(correct_output)))
            report_text.append('\n')
            report_text.append('Your    output\'s length: ' +
                               str(len(process_output)))
            report_text.append('\n')

        if return_code != 'RTE':
            report_text.append('\n')
            report_text.append('Ran in {:.3f} s'.format(process_runtime))
            report_text.append('\n')
        else:
            report_text.append(process_output)

    print(''.join(report_text), end='')


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

        report(
            test_id,
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
