# Taken from https://stackoverflow.com/questions/34818723/export-notebook-to-pdf-without-code/45029786#45029786

import argparse
import textwrap

def strip_code_blocks(infile,outfile):
    with open(infile, 'r') as html_file:
        content = html_file.read()

    # Get rid off prompts and source code
    content = content.replace("div.input_area {","div.input_area {\n\tdisplay: none;")    
    content = content.replace(".prompt {",".prompt {\n\tdisplay: none;")

    f = open(outfile, 'w')
    f.write(content)
    f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='stripCodeFromHtml',
        description='Removes code blocks from notebook exported to html  \n ',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''
                python stripCodeFromHtml infile -keywords --options
                ''')
    )
    parser.add_argument(
        'infile',  type=str, help='Path to notebook html file'
    )
    
    parser.add_argument(
        '-o','--outfile', default=None, type=str, help='Path to output html without code blocks'
    )
    args = parser.parse_args()


    if not args.outfile:
        outfile = args.infile
    else:
        outfile = args.outfile

    strip_code_blocks(args.infile,outfile)
