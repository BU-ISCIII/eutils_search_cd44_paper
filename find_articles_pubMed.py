#!/usr/bin/env python3
import argparse
import sys
from datetime import datetime
import requests
from urllib.parse import urlparse
import urllib.request ,  urllib.error
import os,  json
from progressbar import ProgressBar
from time import sleep

def check_arg(args=None):
    text_description = str('This program creates a csv file with the number of match found for each gene include in the gene file list.')

    parser = argparse.ArgumentParser(prog = 'find_articles_pubMed.py',
                                    formatter_class=argparse.RawDescriptionHelpFormatter,
                                    description = text_description)
    parser.add_argument('-v' ,'--version', action='version', version='%(prog)s 0.0.1')
    parser.add_argument('-c', '--condition', help= 'Conditions to be matched according to pubmed search syntax. p.e "(METASTASIS)+OR+(INVASION)"', type=str, nargs='+')
    parser.add_argument('-file','-input_file', help = 'File name where the result data are dumped')
    parser.add_argument('-out','-output_file', help = 'File name where the result data are dumped')




    return parser.parse_args()



if __name__ == '__main__' :

    if len (sys.argv) == 1 :
        print('Usage: find_articles_pubMed.py -c cond1, cond2 -in input_file.txt -out result.xlsx ')
        print('Try  find_articles_pubMed.py --help for more information.')
        exit(2)
    arguments = check_arg(sys.argv[1:])
    if not os.path.isfile(arguments.file):
        print('Input file ', arguments.file,  ' does not exists')
        exit(0)
    condition = '+'.join(arguments.conditions)
    condition_list = condition.replace("/", "%2F")

    api_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?'
    database = 'pubmed'
    fh = open(arguments.file, 'r')
    lines = fh.readlines()
    fh_out = open(arguments.out, 'w')
    fh_out.write('GENE, Repeticiones\n')
    pbar = ProgressBar ()

    for item_in_file in pbar (lines) :

        item_in_file = item_in_file.rstrip()
        address =  '%sdb=%s&term=%s+AND+%s&retmode=json' %(api_url ,database, item_in_file, condition_list)
        request = urllib.request.Request(address)
        response = urllib.request.urlopen(request)
        data = json.load(response)
        try:
            number_of_items = data['esearchresult']['count']
        except:
            number_of_items ='NaN'
            print ('\nError in count', item_in_file, '\n')
        fh_out.write(item_in_file + ',' + number_of_items +'\n')
        sleep(0.5)
    fh_out.close()
