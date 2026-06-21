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

customer_landing = spark.read.json(
    f"s3://{bucket}/customer/landing/"
)

customer_trusted = customer_landing.filter(
    customer_landing.shareWithResearchAsOfDate.isNotNull()
).selectExpr("email as customer_email")

accelerometer_landing = spark.read.json(
    f"s3://{bucket}/accelerometer/landing/"
)

accelerometer_trusted = accelerometer_landing.join(
    customer_trusted,
    accelerometer_landing.user == customer_trusted.customer_email,
    "inner"
).select(
    accelerometer_landing["*"]
)

accelerometer_trusted.write.mode("overwrite").json(
    f"s3://{bucket}/accelerometer/accelerometer_trusted/"
)

job.commit()
