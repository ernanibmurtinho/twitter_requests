from datetime import date, datetime
from pyspark.sql import SparkSession, HiveContext
import os


class JobBase:
    """
        Classe base para os jobs a serem executados no EMR
    """

    def __init__(self, pex_file=None):
        self.pex_file = pex_file
        self.spark = None
        self.sc = None
        self.job_name = ""
        self.submit_args = "--conf spark.driver.memory=4G --executor-memory 4G pyspark-shell"

    def log_process(self, msg):
        now = datetime.now()
        print('%s - %s' % (now.strftime('%Y-%m-%d-%H:%M:%S'), msg))

    def run(self):

        os.environ["PYSPARK_SUBMIT_ARGS"] = self.submit_args

        self.spark = SparkSession \
            .builder \
            .appName(self.job_name) \
            .config("spark.submit.deployMode", "client") \
            .config("spark.app.name", "Twitter retriever") \
            .config("spark.ui.showConsoleProgress", "true") \
            .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
            .getOrCreate()

        self.sc = self.spark.sparkContext

        self.log_process("[START] - {}".format(self.job_name))

    def execute(self):
        try:
            self.log_process("[START] - {}".format(self.job_name))

            self.run()

        except Exception as e:
            self.log_process('[ERRO] - %s' % e)

            # Raise the error again to output the log
            raise
        else:
            self.log_process("[SUCCESS] - {}".format(self.job_name))
        finally:
            self.log_process("[FINISH] - {}".format(self.job_name))
