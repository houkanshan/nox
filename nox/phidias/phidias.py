import math

import dpark

from prelim import MongoUtil, RedisUtil
import redis
import json

feature_list = ['language', 'countries', 'tags', 'rate', 'people',
                'editors', 'directors', 'actors', 'date', 'length', 'types']
mountain_data_key = '1'


class SplitCiterion(object):
    pass


class GiniCiterion(SplitCiterion):

    """
    Gini 2p(1-p)
    """
    def __call__(self, item_count, total_count):
        prob = float(item_count) / total_count
        return 2 * prob * (1.0 - prob)


class CrossEncropyCiterion(SplitCiterion):

    """
    CrossEncropy -plog(p) - (1-p)log(1-p)
    """
    def __call__(self, item_count, total_count):
        prob = float(item_count) / total_count
        try:
            math.log(1-prob)
            math.log(prob)
        except:
            return 0.0
        return -prob * math.log(prob) - (1 - prob) * math.log(1 - prob)


def get_phidias_point(feature_set, citerion=CrossEncropyCiterion):
    """
    through all feature_set to find
    a best split citerion
    """
    feature_rdd = dpark.parallelize(feature_set)
    total_count = feature_rdd.count()

    def _label_count(item):
        return (item, 1)

    def _count_stat(item):
        return (item[0], sum(item[1]))

    def _compute_criterion(item):
        return (item[0], citerion()(item[1], total_count))

    def _max_criterion(item1, item2):
        return item1 if item1[1] > item2[1] else item2

    return feature_rdd.map(_label_count).groupByKey()\
        .map(_count_stat).map(_compute_criterion).sort(key=lambda x: x[1], reverse=True).take(20)


def make_filter(feature, feature_point, data, np):
    rdd = dpark.parallelize(data)

    def _has_feature(item):
        return feature_point in item[feature]

    def _is_feature(item):
        return item[feature] == feature_point

    def _compare_feature(item):
        try:
            result = float(item[feature]) >= float(feature_point)
            return result
        except Exception:
            return False

    def _has_not_feature(item):
        return feature_point not in item[feature]

    def _is_not_feature(item):
        return item[feature] != feature_point

    def _not_compare_feature(item):
        try:
            return float(item[feature]) < float(feature_point)
        except Exception:
            return True

    np_map = {0: set(
        [_has_not_feature, _is_not_feature, _not_compare_feature]),
        1: set([_has_feature, _is_feature, _compare_feature])}

    feature_map = {'language': set([_has_feature, _has_not_feature]),
                   'countries': set([_has_feature, _has_not_feature]),
                   'tags': set([_has_feature, _has_not_feature]),
                   'rate': set([_compare_feature, _not_compare_feature]),
                   'people': set([_compare_feature, _not_compare_feature]),
                   'editors': set([_has_feature, _has_not_feature]),
                   'directors': set([_has_feature, _has_not_feature]),
                   'actors': set([_has_feature, _has_not_feature]),
                   'year': set([_compare_feature, _not_compare_feature]),
                   'length': set([_compare_feature, _not_compare_feature]),
                   'types': set([_has_feature, _has_not_feature])}

    decision = list(np_map[np] & feature_map[feature])[0]
    return rdd.filter(decision).collect()


def get_split_feature(unique_id, Util=RedisUtil):
    util = Util()
    return util.get_split_feature(unique_id)


def get_data(unique_id, Util=RedisUtil):
    util = Util()
    return util.get_data(unique_id)


def get_filter_point(unique_id, Util=RedisUtil):
    util = Util()
    return util.get_filter_points(unique_id)


def append_filter_point(unique_id, points, Util=RedisUtil):
    util = Util()
    util.append_filter_points(unique_id, points)


def set_data(unique_id, data, Util=RedisUtil):
    util = Util()
    util.set_data(unique_id, data)


def set_split_feature(unique_id, feature_point, Util=RedisUtil):
    util = Util()
    util.set_split_feature(unique_id, feature_point)


def get_top_points(feature_list, unique_id, Util=RedisUtil):
    util = Util()
    all_feature_points = []
    for feature in feature_list:
        feature_set = util.get_types(unique_id, feature)
        feature_top = [(feature, i) for i in get_phidias_point(feature_set)]
        all_feature_points += feature_top
    all_feature_points.sort(key=lambda x: x[1][1])
    return all_feature_points[:100]


def set_feature_points(unique_id, points):
    util = RedisUtil()
    for i in points:
        util.r.sadd(unique_id+'fs', i)


def get_feature_points(unique_id):
    util = RedisUtil()
    return r.smembers(unique_id+'fs')


def get_feature_point(unique_id):
    util = RedisUtil()
    util.r.get(unique_id+'f')


def set_feature_point(unique_id, point):
    util = RedisUtil()
    util.r.set(unique_id, point)


def append_filter_points(unique_id):
    point = get_feature_point(unique_id)
    util = RedisUtil()
    util.r.sadd(unique_id+'fp', point)


def get_filter_points(unique_id):
    util = RedisUtil()
    return r.smembers(unique_id+'fp')


def climax(unique_id, np):
    if np == -1:
        feature_points = get_top_points(feature_list, '1')
        feature_points = ["%s:%s:%f" % (i[0], i[1][0], i[1][1]) for in feature_points]
        set_feature_points(unique_id, feature_points)
    if np == 2:
        feature_points = get_feature_points(unique_id)
        append_filter_points(unique_id)
        filtered = list(feature_points - get_filter_points(unique_id))
        set_feature_points(unique_id, filtered)

    else:
        feature_point = get_feature_point(unique_id)
        tem_tuple = feature_point.split(":")
        new_data = make_filter(tem_tuple[
                               0], tem_tuple[1], get_data(unique_id), np)
        set_data(unique_id, new_data)
        feature_points = get_top_points(feature_list, unique_id)
        feature_points = ["%s:%s:%f" % (i[0], i[1][0], i[1][1]) for in feature_points]
        set_feature_points(unique_id, feature_points)

if __name__ == "__main__":
    climax(2, -1)
