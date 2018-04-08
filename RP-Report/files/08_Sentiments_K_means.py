from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import StandardScaler
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans
from pyspark.sql import SparkSession


spark = SparkSession.builder.appName("TEST").getOrCreate()
'''
Create Dataframe From CSV 
'''
cluster_df = spark.read.csv("/home/iotsys3/PycharmProjects/krishna/Cowrie_Scripts/sentiments.csv",
	header=True,
	inferSchema=True,
	)


'''
Removing Columns that are not needed from DataFrame
'''
#cluster_df = cluster_df.drop("id","date")


'''
Convert Data to Vector as Standardised Scaler 
and Kmeans can only operate on that data
'''
vectorAssembler = VectorAssembler(
		inputCols=["Sentiments"],
		outputCol="features"
	)

''''''
vcluster_df = vectorAssembler.transform(cluster_df)
#vcluster_df.show()
test_df = vectorAssembler.transform(cluster_df)


kmeans = KMeans().setK(2)  # set number of clusters
kmeans = kmeans.setSeed(1)  # set start point
kmodel = kmeans.fit(vcluster_df)

centers = kmodel.clusterCenters()

pred_df = kmodel.transform(test_df)

print("\t**OUTPUT**\n\n\n")
print vcluster_df.show()
print("Centers RK = "+ str(centers))
print(kmodel.summary.clusterSizes)
print("\n\n\n")
pred_df.show(10)
print "Center -1 " + str(centers[0])
print "Center -2 " + str(centers[1])