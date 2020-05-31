def reformat_pred(pred, data_list):
    labels = pred[0]
    labels = [label[0] for label in labels]
    scores = pred[1]
    scores = [sc.item() for sc in scores]
    pred_out = zip(labels, scores, data_list)
    return [*pred_out]

import numpy as np
from matplotlib import pyplot as plt

def generate_scores(df, thr, print_ = 1):
    df['sentiment_pred'] = np.where(((df['label'] == '__label__4')&
                                (df['score'] > thr)),1,
                                   np.where(((df['label'] == '__label__0')&
                                             (df['score'] > thr)), -1, 0))
    
    df['sentiment_or_0_pred'] = np.where(df['sentiment_pred'].isin([1,-1]),df['sentiment_pred'],
                                     df['sentiment'])
    
    df['ones_match'] = np.where(((df['sentiment_pred'] == 1) &
                                (df['sentiment'] == 1)), 1, 0)
    df['zeros_match'] = np.where(((df['sentiment_pred'] == -1) &
                                (df['sentiment'] == -1)), 1, 0)
    df['all_match'] = np.where(((df['ones_match'] == 1) |
                               (df['zeros_match'] == 1)), 1, 0)
    df['all_or_0_match'] = np.where((((df['ones_match'] == 1) |
                                      (df['zeros_match'] == 1)) |
                                      (df['sentiment_pred'] == 0)), 1, 0)

    positive_match = len(df[df['ones_match']==1])
    negative_match = len(df[df['zeros_match']==1])

    real_positives = len(df[df['sentiment']==1])
    real_negatives = len(df[df['sentiment']==-1])

    all_match = len(df[df['all_match']==1])
    all_or_0_match = len(df[df['all_or_0_match']==1])
    
    if print_ == 1:
        print(f'ratio_pos_match {positive_match/real_positives}, ratio_neg_match {negative_match/real_negatives}')
        print('All coincidences: ' + str(all_match/len(df)))
        print('All coincidences_plus_0: ' + str(all_or_0_match/len(df)))
    
    else:
        pass
    
    return df, 1.00*positive_match/real_positives, 1.00*negative_match/real_negatives, all_match/len(df), all_or_0_match/len(df)
  
    
def plot_results(df):
    ones_match = []
    zeros_match = []
    all_match = []
    all_or_0_match = []
    thrs = list(np.arange(-1,1,step = 0.05))
    pred_thr = []
    for thr in thrs:
        
        df, ones_match_thr, zeros_match_thr, all_match_thr, all_or_0_match_thr = generate_scores(df, thr, print_=0);
        ones_match.append(ones_match_thr)
        zeros_match.append(zeros_match_thr)
        all_match.append(all_match_thr)
        all_or_0_match.append(all_or_0_match_thr)

    plt.plot(thrs, ones_match)
    plt.plot(thrs, zeros_match)
    plt.plot(thrs, all_match)
    plt.plot(thrs, all_or_0_match)

    plt.legend(['pos_match', 'neg_match', 'all_match', 'all_or_0_match'], loc='upper left')

    plt.show() 
    
    return ones_match, zeros_match, all_match, all_or_0_match


    
def generate_scores_blob(df, trh=0.6, print_ = 1):
    df['ones_match'] = np.where(((df['sentiment_blob'] > trh)&
                                (df['sentiment'] == 1)), 1, 0)
    df['zeros_match'] = np.where(((df['sentiment_blob'] < -trh)&
                                (df['sentiment'] == -1)), 1, 0)
    df['all_match'] = np.where(((df['ones_match'] == 1) |
                               (df['zeros_match'] == 1)), 1, 0)
    df['all_or_0_match'] = np.where((((df['ones_match'] == 1) |
                                      (df['zeros_match'] == 1)) |
                                      ((df['sentiment_blob'] < trh)&
                                       (df['sentiment_blob'] > -trh))), 1, 0)

    positive_match = len(df[df['ones_match']==1])
    negative_match = len(df[df['zeros_match']==-1])

    real_positives = len(df[df['sentiment']==1])
    real_negatives = len(df[df['sentiment']==-1])
    
    all_match = len(df[df['all_match']==1])
    all_or_0_match = len(df[df['all_or_0_match']==1])
    
    if print_ == 1:
        print(f'ratio_pos_match {positive_match/real_positives}, ratio_neg_match {negative_match/real_negatives}')
        print('All coincidences: ' + str(all_match/len(df)))
        print('All coincidences_plus_0: ' + str(all_or_0_match/len(df)))
    
    else:
        pass
    
    return 1.00*positive_match/real_positives, 1.00*negative_match/real_negatives, all_match/len(df), all_or_0_match/len(df)
  
def plot_results_glob(df):
    ones_match = []
    zeros_match = []
    all_match = []
    all_or_0_match = []
    thrs = list(np.arange(0,1,step = 0.05))
    pred_thr = []
    for thr in thrs:
        
        ones_match_thr, zeros_match_thr, all_match_thr, all_or_0_match_thr = generate_scores_blob(df, thr, print_=0);
        ones_match.append(ones_match_thr)
        zeros_match.append(zeros_match_thr)
        all_match.append(all_match_thr)
        all_or_0_match.append(all_or_0_match_thr)

    plt.plot(thrs, ones_match)
    plt.plot(thrs, zeros_match)
    plt.plot(thrs, all_match)
    plt.plot(thrs, all_or_0_match)

    plt.legend(['ones_match', 'zeros_match', 'all_match', 'all_or_0_match'], loc='upper left')

    plt.show() 
    
    return ones_match, zeros_match, all_match, all_or_0_match

def string_to_float(text):
    try:
        text = float(text)
    except:
        text = 0
    return text

def format_columns(df, column):
    df[column] = df[column].apply(lambda x: str(x).strip())
    df[column] = df[column].apply(lambda x: string_to_float(x))