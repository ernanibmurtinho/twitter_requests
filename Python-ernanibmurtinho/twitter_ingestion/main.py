import argparse
import os
import sys
import glob
from twitter_ingestion.jobs.retrieveTwitterJob import JobRetrieveTweets

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Twitter retriever')
    parser.add_argument("--retrieveTweets", help="process the retrieve tweets process")

    args = parser.parse_args()

    sys.path.append(os.path.realpath(glob.glob('*.pex')[0]))
    pex_file = os.path.basename([path for path in sys.path if path.endswith('.pex')][0])
    os.environ['PYSPARK_PYTHON'] = "./" + pex_file

    if args.retrieveTweets:
        jobRetrieveTweets = JobRetrieveTweets(pex_file)
        jobRetrieveTweets.execute()

    else:
        print("Pass the step do want to execute! Use -h parameter for help.")

