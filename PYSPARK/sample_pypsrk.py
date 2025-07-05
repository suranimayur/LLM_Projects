from pyspark.sql import SparkSession

# Initialize Spark session
spark = SparkSession.builder \
    .appName("ExampleApp") \
    .getOrCreate()

# Set log level
spark.sparkContext.setLogLevel("DEBUG")

# Example DataFrame operation
data = [("Alice", 1), ("Bob", 2)]
df = spark.createDataFrame(data, ["Name", "Age"])
df.show()

# Stop Spark session
spark.stop()
