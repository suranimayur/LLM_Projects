from pyspark.sql import SparkSession

# Create SparkSession
spark = SparkSession.builder \
    .appName("SparkSessionExample") \
    .getOrCreate()

# Sample DataFrame
data = [("Alice", 25), ("Bob", 30)]
df = spark.createDataFrame(data, ["Name", "Age"])

# Show DataFrame
df.show()

# Stop SparkSession
spark.stop()
