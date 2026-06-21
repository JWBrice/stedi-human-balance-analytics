CREATE EXTERNAL TABLE IF NOT EXISTS stedi.step_trainer_landing (
  sensorreadingtime bigint,
  serialnumber string,
  distancefromobject int
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://stedi-jeanbrice-d609/step_trainer/landing/';
