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

customers_curated = spark.read.json(
    f"s3://{bucket}/customer/customers_curated/"
)

step_trainer_landing = spark.read.json(
    f"s3://{bucket}/step_trainer/landing/"
)

customers_curated = customers_curated.withColumnRenamed("serialNumber", "customer_serial")
step_trainer_landing = step_trainer_landing.withColumnRenamed("serialNumber", "step_serial")

step_trainer_trusted = step_trainer_landing.join(
    customers_curated,
    step_trainer_landing.step_serial == customers_curated.customer_serial,
    "inner"
).select(
    step_trainer_landing["*"]
)

step_trainer_trusted.write.mode("overwrite").json(
    f"s3://{bucket}/step_trainer/step_trainer_trusted/"
)

job.commit()
