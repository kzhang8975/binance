import errno    
import os

def save_fullbook_data(fullbook_data, path):
    try:
        os.makedirs(path)
        fullbook_data.to_csv(path + '/' + 'market_data.csv')
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            fullbook_data.to_csv(path + '/' + 'market_data.csv')
        else:
            raise
