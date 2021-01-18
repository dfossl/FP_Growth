import FPGrowth
import argparse

parser = argparse.ArgumentParser(description='Perform FP-Growth On Dataset.')

parser.add_argument('-f',
                    dest="filename",
                    type=str,
                    nargs=1,
                    help='File directory of data file.',
                    required=True)

parser.add_argument('-minsup',
                    "-m",
                    type=int,
                    dest="minsup",
                    nargs=1,
                    help="Minimum support percent. Must be integer [0-100]",
                    required=True,
                    metavar="[0-100]",
                    choices=range(0,101))

parser.add_argument('-o',
                    dest="outputfile",
                    type=str,
                    nargs=1,
                    help='output file directory.',
                    required=True)

args = parser.parse_args()


FPG = FPGrowth.FPGrowth()

FPG.FPGrowth(filename = args.filename[0], minimumsup=args.minsup[0])
FPG.resultstofile(filename=args.outputfile[0])
FPG.printterminal()


