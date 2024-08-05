# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 17:16:20 2024

@author: JacopoBaldacci
"""

import logger as log
from os import path
from argparse import ArgumentParser, RawTextHelpFormatter

def main(args_main):
    log.info('+++++++++      Program Started  +++++++++   ')

    try:
        pass
    
    except Exception as err:
   
        log.error('######### Program Ended with Errors ######### {}'.format(err))

        return None

    return 0

if __name__ == '__main__':
    parser = ArgumentParser(description = 'description:\n  Main\n'
                                                  'This sw does this and that ...',
                                      usage = '\n  __main__.py \n',
                                      formatter_class = RawTextHelpFormatter)
    parser.add_argument('mode', choices=['D1Run', 'D2Run'],
                        help="D1Run is for the prediction of the next day. Train seq2seq model nad run this kind of model"
                            "if possible (not missed data in acutal data, exc). \n"
                            "D2Run is for next 2 days prediction. Train RandomForest model and run this kind of model. \n")
    parser.add_argument('-p', '--path',
                        default = path.dirname(path.abspath("__file__")),
                        help='path')
    # args_main = parser.parse_args()
    args_main = parser.parse_args()
    main(args_main)
