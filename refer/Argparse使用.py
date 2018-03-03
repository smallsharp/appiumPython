import argparse
parser = argparse.ArgumentParser(description="say something about this application !!")
parser.add_argument('--age',  help="this is an optional argument")
result = parser.parse_args()

print(result.age)