import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args['JOB_NAME'], args)

bucket = "stedi-jeanbrice-d609"

# Read trusted customer records.
customer_trusted = spark.read.json(
    f"s3://{bucket}/customer/customer_trusted/"
)

# Read trusted accelerometer readings.
accelerometer_trusted = spark.read.json(
    f"s3://{bucket}/accelerometer/accelerometer_trusted/"
)

# Keep only customers who have accelerometer data.
# dropDuplicates ensures one record per customer.
customers_curated = customer_trusted.join(
    accelerometer_trusted,
    customer_trusted.email == accelerometer_trusted.user,
    "inner"
).select(
    customer_trusted["*"]
).dropDuplicates(["email"])

customers_curated.write.mode("overwrite").json(
    f"s3://{bucket}/customer/customers_curated/"
)

job.commit()
