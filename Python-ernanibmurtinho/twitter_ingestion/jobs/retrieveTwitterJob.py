from pyspark import Row
from pyspark.sql.functions import asc, unix_timestamp, col, from_json
from twitter_ingestion.jobs.jobBase import JobBase
from twitter_ingestion.utils import twitter, timer
from pyspark.sql.types import *
import json


class JobRetrieveTweets(JobBase):

    def __init__(self, pex_file=None):
        super().__init__(pex_file)
        self.job_name = "JobRetrieveTwitter"
        self.submit_args = " --deploy-mode client --master 'local[4]' --driver-memory 4g --executor-memory 4g --num-executors 2 --executor-cores 2 --conf spark.dynamicAllocation.enabled=false pyspark-shell"

    @timer
    def retrieve_service(self, consumer_key,
                         consumer_secret,
                         access_token,
                         access_token_secret):
        self.log_process("[STEP 3] - Making the authentication! ")
        auth = twitter.TwitterService(consumer_key, consumer_secret, access_token, access_token_secret)
        self.log_process("[STEP 4] - Retrieving data from twitter! ")
        return auth.get_tweets_from_tag(search_tag='#Corinthians', page_limit=1, count_tweet=100)

    def build_df(self, result):
        df = self.spark.createDataFrame([Row(**i) for i in result])
        df = df.select(
            col("message_id"),
            unix_timestamp(col("message_created_at")).alias("message_created_at"),
            col("text"),
            col("author"),
            col("user_id"),
            unix_timestamp(col("user_created_at")).alias("user_created_at"),
            col("user_name"),
            col("user_screen_name"))
        df = df.selectExpr("*", "CAST(year(current_date) AS INT) as year",
                           "CAST(month(current_date) AS INT) as month",
                           "CAST(day(current_date) AS INT) as day")
        df = df.sort("message_created_at",
                     "user_created_at",
                     "user_name"
                     )
        return df

    def struct_df(self, df):
        df.createOrReplaceTempView("tweets")
        result = self.spark.sql("""
        SELECT user_name, 
            to_json(struct(collect_list(str_to_map(Concat(
            'user_id:', user_id, ","
            ,'user_created_at:', user_created_at, ","
            ,'user_name:', '"', user_name, '"', ","
            ,'user_screen_name:', user_screen_name)))[0])) as author,
            to_json(struct(collect_list(str_to_map(Concat(
             'message_id:', message_id, ","
            ,'message_created_at:', message_created_at, ","
            ,'text:', '"', text, '"', ","
            ,'author:', author))))) as message
        FROM tweets
        GROUP BY user_name
        ORDER BY user_name,
                 get_json_object(author, '$.user_created_at'), 
                 get_json_object(message, '$.message_created_at')
        """)

        result_schema = self.spark.sql("""
        SELECT user_name, collect_list(str_to_map(Concat(
            'user_id:', user_id, ","
            ,'user_created_at:', user_created_at, ","
            ,'user_name:', '"', user_name, '"', ","
            ,'user_screen_name:', user_screen_name)))[0] as author,
            collect_list(str_to_map(Concat(
             'message_id:', message_id, ","
            ,'message_created_at:', message_created_at, ","
            ,'text:', '"', text, '"', ","
            ,'author:', author))) as message
        FROM tweets
        GROUP BY user_name
        ORDER BY user_name, author.user_created_at
        """)

        result_schema.printSchema()
        result_schema.show(2, truncate=False, vertical=True)
        schema_author_result = result_schema.select('author').schema.json()
        schema_message_result = result_schema.select('message').schema.json()

        result_struct = result.withColumn("author", from_json(col("author"),
                                                              StructType.fromJson(json.loads(schema_author_result))))
        result_struct = result_struct.withColumn("message", from_json(col("message"), StructType.fromJson(
            json.loads(schema_message_result))))

        self.log_process("[STEP 8] - Checking the schema struct generated! ")
        result_struct.printSchema()

        result = result.selectExpr("*", "CAST(year(current_date) AS INT) as year",
                                   "CAST(month(current_date) AS INT) as month",
                                   "CAST(day(current_date) AS INT) as day")

        return result

    def assert_frame_equal_with_sort_twitter(self, results, expected):
        check_value = True if results.columns == expected.columns \
                      and results.filter("message_id is not null").count() \
                      == expected.filter("message_id is not null").count() \
                      and results.dtypes == expected.dtypes \
                      else False
        assert check_value, "please, check your data!"

    def run(self):
        super().run()
        consumer_key = 'fill with your own'
        consumer_secret = 'fill with your own'
        access_token = 'fill with your own'
        access_token_secret = 'fill with your own'
        bearer_token = 'fill with your own'
        self.log_process("[STEP 1] - token loaded ")
        self.log_process(f"[step 2] - starting requests ")
        result = self.retrieve_service(consumer_key, consumer_secret, access_token, access_token_secret)
        self.log_process(f"[step 5] - end of requests ")
        self.log_process(f"[step 6] - building df ")
        df = self.build_df(result)
        self.log_process(f"[step 7] - the df contains {df.count()} lines ")
        self.log_process(f"[step 8] - showing df first rows ")
        df.show(10, truncate=False)
        nested_df = self.struct_df(df)
        expected = self.spark.read.parquet("result/test_parquet/")
        self.log_process(f"[step 9] - checking df structure ")
        self.assert_frame_equal_with_sort_twitter(df, expected)
        self.log_process(f"[step 10] - writing df to disk ")
        nested_df.coalesce(1).write.mode("append") \
            .partitionBy('year', 'month', 'day') \
            .parquet("result/twitter_ingestion/")
        self.log_process("[Twitter search job] - Ended")
