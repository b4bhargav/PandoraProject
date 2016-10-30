from pyspark import SparkContext, SparkConf, StorageLevel
import json
import argparse

def filter_and_project(rdd):
    for r in rdd:
        data = r.decode('ISO-8859-1').split(" ")
        prefix = data[1].split(":")
        if len(prefix) <= 1 and data[1].isalnum():
            yield (str(data[0]), (data[1], data[2]))


def sort_return_top_ten(rdd):
    for r in rdd:
        for language, rs_list in r:
            result_dict = {}
            val = sorted(rs_list, reverse=True, key=lambda x: int(x[1]))
            result_dict[language] = val[:11]
            yield result_dict

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--app_name", default="ModelMetrics")
    parser.add_argument("--i_input_path")
    parser.add_argument("--o_output_path")
    args = parser.parse_args()

    conf = SparkConf().setAppName("Pandora_app")
    conf.set('spark.ui.showConsoleProgress', False)  # It just comes messed up with the rest of the logs
    conf.set('spark.shuffle.memoryFraction', '0.6')
    conf.set('spark.storage.memoryFraction', '0.3')
    conf.set('spark.kryoserializer.buffer', '256m')
    conf.set('spark.kryoserializer.buffer.max', '512m')
    sc = SparkContext(conf=conf)

    input_rdd = sc.textFile(args.i_input_path)
    filter_rdd = input_rdd.mapPartitions()
    grouped_rdd = filter_rdd.groupByKey().mapValues(list).mapPartitions(sort_return_top_ten)
    result_rdd = grouped_rdd.map(lambda x: json.dumps(x))
    saveAsTextFile(args.o_output_path)
