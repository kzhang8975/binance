import errno    
import os

def save_symbol_fullbook_data(symbol, fullbook_data, path):
    try:
        os.makedirs(path)
        fullbook_data.to_csv(path + '/' + '%s.csv' % symbol)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            fullbook_data.to_csv(path + '/' + '%s.csv' % symbol)
        else:
            raise
