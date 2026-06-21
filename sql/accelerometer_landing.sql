CREATE EXTERNAL TABLE IF NOT EXISTS stedi.accelerometer_landing (
  timestamp bigint,
  user string,
  x double,
  y double,
  z double
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://stedi-jeanbrice-d609/accelerometer/landing/';
