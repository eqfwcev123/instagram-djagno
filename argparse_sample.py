# argparse = argument 분석
import argparse

parser = argparse.ArgumentParser(description='argparse practice')  # ArgumentParser 객체 생성
parser.add_argument('foo', nargs='+')  # 각 cli 인자가 어떻게 파싱될지 지정.
args = parser.parse_args()  # add_argument 로 각 인자가 어떻게 파싱될지 지정하고, parse_args로 적용

# add_argument()
# name or flags ---> Either a name or a list of option strings, e.g. foo or -f, --foo.
# action ---> The basic type of action to be taken when this argument is encountered at the command line.
# nargs ---> The number of command-line arguments that should be consumed.
# const ---> A constant value required by some action and nargs selections.
# default ---> The value produced if the argument is absent from the command line.
# type ---> The type to which the command-line argument should be converted.
# choices ---> A container of the allowable values for the argument.
# required ---> Whether or not the command-line option may be omitted (optionals only).
# help ---> A brief description of what the argument does.
# metavar ---> A name for the argument in usage messages.
# dest ---> The name of the attribute to be added to the object returned by parse_args().
