# maintainer: Adam Budziak
import argparse
import os
import subprocess
from os import walk, path
from tempfile import mkstemp
from enum import Enum

import tests
import failures
import ignored

tests_dct = tests.main
failures_dct = failures.main
ignored_dct = ignored.main

INPUT_DIR = "./in"
OUTPUT_DIR = "./out"
FAILURES_DIR = "./failures"

# You may want to adjust these. Both absolute and relative paths
# are supported
COMPILER_PATH = "../compiler"
INTERPRETER_PATH = "../interpreter/interpreter"


class CompilerModes(Enum):
    STDIN_STDOUT = 1
    PARAM_FILE_OUT = 2
    CONST_FILE_OUT = 3


COMPILER_MODE = CompilerModes.STDIN_STDOUT
COMPILER_PARAMS = {}


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class NoMetaError(Exception):
    pass


class CompilationFailed(Exception):
    pass


class CompilationNotFailed(Exception):
    pass


class CompilationException(Exception):
    pass


class Summary():
    def __init__(self):
        self.failed = 0
        self.passed = 0
        self.compilation_failed = 0
        self.compilation_didnt_fail = 0
        self.no_meta = 0
        self.ignored = 0
        self.exceptions = 0

    def __str__(self):
        res = bcolors.BOLD + "Summary: \n" + bcolors.ENDC

        if self.passed > 0:
            res += bcolors.OKGREEN + "Passed: " + str(self.passed) + '\n'

        if self.failed > 0:
            res += bcolors.FAIL + "Failed: " + str(self.failed) + '\n'

        if self.compilation_failed > 0:
            res += (bcolors.FAIL + "Compilation failed: "
                    + str(self.compilation_failed)) + "\n"

        if self.compilation_didnt_fail > 0:
            res += (bcolors.FAIL + "Compilation didn't fail but it should: "
                    + str(self.compilation_didnt_fail)) + "\n"

        if self.ignored > 0:
            res += (bcolors.WARNING + "Ignored tests: "
                    + str(self.ignored)) + "\n"

        if self.exceptions > 0:
            res += (bcolors.FAIL + "Exceptions thrown: "
                    + str(self.exceptions) + '\n')

        res += bcolors.ENDC
        return res


class TestSubject:
    def __init__(self, *, input_fpath, meta):
        self.input_fpath = input_fpath
        self.meta = meta

    def _compile(self, compiled):
        try:
            compile_to_file(self.input_fpath, compiled)
            self.meta['real_output'] = "Compiled"
        except CompilationFailed:
            self.meta['real_output'] = "Compilation failed"
            raise CompilationFailed()
        except Exception as e:
            self.meta['real_output'] = e
            raise CompilationException()

    def test(self, input_, output_, should_run=True):
        self.expected = output_
        compiled = get_compile_file()
        self._compile(compiled)
        if not should_run:
            return

        try:
            result = subprocess.check_output(
                [INTERPRETER_PATH, compiled], input=input_
            )
        except Exception as e:
            # this could be improved, more info would be nice
            self.meta['real_output'] = e
            raise RuntimeError()

        self.meta['real_output'] = parse_output(result.decode('utf-8'))
        os.remove(compiled)
        return self.meta['real_output'] == output_


def get_compile_file():
    if COMPILER_MODE != CompilerModes.CONST_FILE_OUT:
        return mkstemp()[1]
    else:
        return COMPILER_PARAMS['OUTPUT_FILE']


def compile_to_file(input_fpath, output_fpath):
    if COMPILER_MODE == CompilerModes.STDIN_STDOUT:
        with open(input_fpath) as input_f:
            try:
                compiled = subprocess.check_output(
                    [COMPILER_PATH], stdin=input_f
                )
            except subprocess.CalledProcessError:
                raise CompilationFailed()

            with open(output_fpath, 'wb') as output_f:
                output_f.write(compiled)

    elif COMPILER_MODE == CompilerModes.PARAM_FILE_OUT:
        with open(input_fpath) as input_f:
            return_code = subprocess.call(
                [COMPILER_PATH, output_fpath], stdin=input_f
            )
            if return_code != 0:
                raise CompilationFailed()

    elif COMPILER_MODE == CompilerModes.CONST_FILE_OUT:
        with open(input_fpath) as input_f:
            return_code = subprocess.call(
                [COMPILER_PATH], stdin=input_f
            )
            if return_code != 0:
                raise CompilationFailed()


def parse_output(raw_output):
    return [int(line.split('>')[1].strip())
            for line in raw_output.split('\n')
            if len(line.split('>')) > 1]


def load_input(input_):
    return '\n'.join(str(i) for i in input_).encode('utf-8')


def print_ignored(input_fpath):
    print(bcolors.WARNING, "WARNING: Test ignored: ",
          input_fpath, bcolors.ENDC)


def print_no_meta(input_fpath):
    print(bcolors.WARNING, "WARNING: No meta for ", input_fpath, bcolors.ENDC)


def invalid_meta(input_fpath):
    print(bcolors.WARNING, "WARNING: Invalid meta for ",
          input_fpath, bcolors.ENDC)


def print_error(subj, error_name):
    print(bcolors.FAIL, error_name,
          bcolors.ENDC, bcolors.BOLD, subj.input_fpath, bcolors.ENDC, '\n',
          bcolors.BOLD, subj.meta['title'], bcolors.ENDC, '\n',
          "Expected output: ", subj.expected, "\n",
          "Real output: ", subj.meta['real_output'])


errors = {
    'FAIL': "Test failed:",
    'COMP_FAIL': "Unexpected compilation failure:",
    'COMP_EXC': "Unexpected compilation exception:",
    'DIDNT_FAIL': "Compilation didn't fail, when it should:",
    'INTER_EXC': "Unexpected interpreter exception:"
}


def print_passed():
    print(
        bcolors.BOLD, '.', bcolors.ENDC, end=""
    )


def load_meta(input_fpath, source):
    try:
        meta = source[input_fpath.split('/', 2)[2]]
    except KeyError:
        raise NoMetaError()
    return meta


class Tester:
    def __init__(self, summary, should_fail=False):
        self.last_ok = False
        self.summary = summary
        self.should_fail = should_fail

    def handle_exc(self, print_fn, *args):
        print()
        print_fn(*args)
        self.last_ok = False

    def test_imp(self, subj):
        inputs = subj.meta['input']
        outputs = subj.meta['output']

        if len(inputs) != len(outputs):
            self.handle_exc(invalid_meta, subj.input_fpath)
            return

        if subj.input_fpath in ignored_dct:
            self.handle_exc(print_ignored, subj.input_fpath)
            self.summary.ignored += 1
            return

        for in_, out_ in zip(inputs, outputs):
            try:
                result = subj.test(load_input(in_), out_,
                                   should_run=(not self.should_fail))
                if self.should_fail:
                    raise CompilationNotFailed()
                if not result:
                    self.summary.failed += 1
                    self.handle_exc(print_error, subj, errors['FAIL'])
                else:
                    print_passed()
                    self.summary.passed += 1
                    self.last_ok = True
            except NoMetaError:
                self.handle_exc(print_no_meta, subj.input_fpath)
                self.summary.no_meta += 1
            except CompilationFailed:
                if not self.should_fail:
                    self.handle_exc(print_error, subj, errors['COMP_FAIL'])
                    self.summary.compilation_failed += 1
                else:
                    print_passed()
                    self.summary.passed += 1
                    self.last_ok = True
            except CompilationException:
                if not self.should_fail:
                    self.handle_exc(print_error, subj, errors['COMP_EXC'])
                    self.summary.compilation_failed += 1
                else:
                    print_passed()
                    self.summary.passed += 1
                    self.last_ok = True
            except CompilationNotFailed:
                self.handle_exc(print_error, subj, errors['DIDNT_FAIL'])
                self.summary.compilation_didnt_fail += 1
            except RuntimeError:
                self.handle_exc(print_error, subj, errors['INTER_EXC'])
                self.summary.exceptions += 1

    def test_dir(self, dir_, fnames):
        if dir_ in ignored_dct:
            self.handle_exc(print_ignored, dir_)
            self.summary.ignored += len(fnames)
            return

        print(bcolors.HEADER, "\nTesting dir: ", dir_, bcolors.ENDC)
        for fname in fnames:
            input_fpath = path.join(dir_, fname)
            try:
                if self.should_fail:
                    meta = load_meta(input_fpath, failures_dct)
                else:
                    meta = load_meta(input_fpath, tests_dct)
            except NoMetaError:
                self.handle_exc(print_no_meta, input_fpath)
                continue

            subj = TestSubject(input_fpath=input_fpath, meta=meta)
            self.test_imp(subj)

    def test_all(self, dir_):
        for (dirpath, dirnames, fnames) in walk(dir_):
            if fnames:
                self.test_dir(dirpath, fnames)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Prosty skrypt automatyzujący proces"
            " testowania kompilatora na JFTT."))
    parser.add_argument('--compiler',
                        help="ścieżka do pliku wykonywalnego kompilatora")
    parser.add_argument('--interpreter',
                        help="ścieżka do pliku wykonywalnego interpretera")
    parser.add_argument(
        '--interpreter_bn',
        help=("ścieżka do pliku wykonywalnego interpretera"
              " dla dużych liczb (nie jest jeszcze wspierany)"))

    parser.add_argument(
        '--compiler_out_to_param_file',
        help=("flaga oznaczająca, że kompilator zwraca"
              " skompilowany kod do pliku"
              " podawanego mu jako parametr"),
        action='store_true'
    )

    parser.add_argument(
        '--compiler_out_to_const_file',
        help=("flaga oznaczająca, że kompilator zwraca skompilowany"
              " kod zawsze do stałego pliku")
    )

    args = parser.parse_args()

    if args.compiler is not None:
        COMPILER_PATH = args.compiler
    if args.interpreter is not None:
        INTERPRETER_PATH = args.interpreter
    if args.interpreter_bn is not None:
        pass
        #  not supported yet
        #  INTERPRETER_BN_PATH = args.interpreter_bn

    if args.compiler_out_to_param_file:
        COMPILER_MODE = CompilerModes.PARAM_FILE_OUT

    if args.compiler_out_to_const_file:
        COMPILER_PARAMS['OUTPUT_FILE'] = args.compiler_out_to_const_file

    summary = Summary()
    tester = Tester(summary)
    tester.test_all(INPUT_DIR)
    print("\n", summary)

    print(bcolors.BOLD, bcolors.HEADER,
          "TESTS FOR FAILURES STARTING...", bcolors.ENDC)

    fail_summary = Summary()
    failures_tester = Tester(fail_summary, should_fail=True)
    failures_tester.test_all(FAILURES_DIR)

    print("\n", fail_summary)
