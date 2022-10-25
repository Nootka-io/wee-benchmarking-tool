import difflib
from statistics import mean
import json
from pathlib import Path
from .tokenizer import tokenize
from collections import Counter


def eval_results(output_dir, extractors_to_eval = []):
    results = {}

    # open ground truth
    with open('./datasets/scrappinghub_aeb/ground-truth.json') as f:
        ground_truth = json.load(f)
    # tokenize ground truth
    # ground_truth = tokenize(ground_truth)

    # open all the extractions
    for path in sorted(Path(f'output/{output_dir}').glob('*.json')):
        if not extractors_to_eval:
            pass
        elif path.stem not in extractors_to_eval:
            continue

        confusion_matrix = {
            'true_positives': 0,
            'true_negatives': 0,
            'false_positives': 0,
            'false_negatives': 0,
        }
        all_similarities = []
        name = path.stem
        results[name] = {
            'items_sec': None,
            'similarity': {
                'recall': None,
                'precision': None,
                'fscore': None,
                'accuracy': None,
                'mean_similarity': None,
            },
            'complex': {
                'recall': None,
                'precision': None,
                'fscore': None,
                'accuracy': None,
            },
        }
        with open(str(path)) as f:
            pred_results = json.load(f)

        # items per second the number of items extracted / total_time
        results[name]['items_sec'] = len(pred_results['extracts'].keys()) / pred_results['elapsed_time']

        # tokenize the extracted results

        if pred_results['extracts'].keys() != ground_truth['extracts'].keys():
            raise ValueError('prediction keys do not match ground truth')

        confusion_matrix_list = []
        for key in ground_truth['extracts'].keys():
            # we compare the tokenized strings and build the confussion matrix
            # gt_shingles = _all_shingles(ground_truth['extracts'][key].get('articleBody', ''), 4)
            # pred_shingles = _all_shingles(pred_results['extracts'][key].get('articleBody', ''), 4)
            gt_tokens = tokenize(ground_truth['extracts'][key].get('articleBody', ''))
            pred_tokens = tokenize(pred_results['extracts'][key].get('articleBody', ''))

            # accuracy the difference between the 2 vectors
            # accuracy = float(gt_tokens == pred_tokens)

            # similarity scoring
            temp_sim = difflib.SequenceMatcher(None, ground_truth['extracts'][key].get('articleBody', ''), pred_results['extracts'][key].get('articleBody', ''))
            similarity_ratio = temp_sim.ratio()
            all_similarities.append(similarity_ratio)
            if similarity_ratio > 0.90:
                # it's correct
                confusion_matrix['true_positives'] += 1
            else:
                confusion_matrix['false_negatives'] += 1
                confusion_matrix['false_positives'] += 1

            # complex scoring
            confusion_matrix_list.append(do_complex_scoring(gt_tokens, pred_tokens))
        complex_scores = scores_from_cm(confusion_matrix_list)
        results[name]['complex'] = complex_scores

        # aggregate similarity scoring
        # confusion_matrix['false_positives'] = len(ground_truth['extracts'].keys()) - len(pred_results['extracts'].keys())
        # recall - Recall = TruePositives / (TruePositives + FalseNegatives)
        results[name]['similarity']['recall'] = (confusion_matrix['true_positives'] / (confusion_matrix['true_positives'] + confusion_matrix['false_negatives']))
        # precision - Precision = TruePositives / (TruePositives + FalsePositives)
        results[name]['similarity']['precision'] = confusion_matrix['true_positives'] / (confusion_matrix['true_positives'] + confusion_matrix['false_positives'])
        # f1score - (2 * Precision * Recall) / (Precision + Recall)
        results[name]['similarity']['fscore'] = (2 * results[name]['similarity']['precision'] * results[name]['similarity']['recall']) / (results[name]['similarity']['precision'] + results[name]['similarity']['recall'])
        # accuracy -
        results[name]['similarity']['accuracy'] = (confusion_matrix['true_positives']) / len(pred_results['extracts'].keys())
        results[name]['similarity']['mean_similarity'] = mean(all_similarities)

    return results


def do_complex_scoring(gt_tokens, pred_tokens):
    tp = fp = fn = tn = 0
    pred_token_counts = dict(Counter(gt_tokens))
    gt_token_counts = dict(Counter(pred_tokens))
    for key in (set(gt_token_counts) | set(pred_token_counts)):
        true_count = gt_token_counts.get(key, 0)
        pred_count = pred_token_counts.get(key, 0)
        tp += min(true_count, pred_count)
        fp += max(0, pred_count - true_count)
        fn += max(0, true_count - pred_count)
    cm = [tp, fp, fn, tn]
    cm_s = sum(cm)
    # Normalize metrics so that longer texts do not have more weight.
    if cm_s > 0:
        cm = [tp/cm_s, fp/cm_s, fn/cm_s, tn/cm_s]
    # breakpoint()
    return tuple(cm)

def scores_from_cm(cm):
    precision = mean([
        precision_score(tp, fp, fn) for tp, fp, fn, tn in cm
        if tp + fp > 0])
    recall = mean([
        recall_score(tp, fp, fn) for tp, fp, fn, tn in cm
        if tp + fn > 0])
    f1 = 2 * precision * recall / (precision + recall)
    accuracy = sum([(tp+tn) for tp, fp, fn, tn in cm]) / sum([(tp+tn+fn+tn) for tp, fp, fn, tn in cm])
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'fscore': f1,

    }

def precision_score(tp: float, fp: float, fn: float) -> float:
    if fp == fn == 0:
        return 1.
    if tp == fp == 0:
        return 0.
    return tp / (tp + fp)


def recall_score(tp: float, fp: float, fn: float) -> float:
    if fp == fn == 0:
        return 1.
    if tp == fn == 0:
        return 0.
    return tp / (tp + fn)