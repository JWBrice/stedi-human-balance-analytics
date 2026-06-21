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

# Read the research-approved Step Trainer sensor records.
step_trainer_trusted = spark.read.json(
    f"s3://{bucket}/step_trainer/step_trainer_trusted/"
)

# Read the research-approved mobile accelerometer records.
accelerometer_trusted = spark.read.json(
    f"s3://{bucket}/accelerometer/accelerometer_trusted/"
)

# The files may preserve original camelCase names, so normalize them.
if "sensorReadingTime" in step_trainer_trusted.columns:
    step_trainer_trusted = step_trainer_trusted.withColumnRenamed(
        "sensorReadingTime", "sensorreadingtime"
    )

if "distanceFromObject" in step_trainer_trusted.columns:
    step_trainer_trusted = step_trainer_trusted.withColumnRenamed(
        "distanceFromObject", "distancefromobject"
    )

# Spark may use either timeStamp or timestamp.
if "timeStamp" in accelerometer_trusted.columns:
    accelerometer_trusted = accelerometer_trusted.withColumnRenamed(
        "timeStamp", "timestamp"
    )

machine_learning_curated = step_trainer_trusted.join(
    accelerometer_trusted,
    step_trainer_trusted.sensorreadingtime == accelerometer_trusted.timestamp,
    "inner"
).select(
    step_trainer_trusted.sensorreadingtime,
    step_trainer_trusted.distancefromobject,
    step_trainer_trusted.step_serial,
    accelerometer_trusted.timestamp,
    accelerometer_trusted.user,
    accelerometer_trusted.x,
    accelerometer_trusted.y,
    accelerometer_trusted.z
)

machine_learning_curated.write.mode("overwrite").json(
    f"s3://{bucket}/machine_learning/machine_learning_curated/"
)

job.commit()
