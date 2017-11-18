import core.mlProcess._
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.types.{LongType, StringType, StructField, StructType}
import org.apache.log4j.Logger
import org.apache.log4j.Level
import utils.ML._

/**
  * Created by sasoo on 27/07/17.
  */
object Boot {

  def main(args: Array[String]): Unit = {
    Logger.getLogger("org").setLevel(Level.OFF)

    val sp = SparkSession.builder()
      .appName("SparkSesion")
      .master("local[*]")
      .getOrCreate()
    val dataSchema = StructType(Array(
      StructField("index", LongType, true),
      StructField("title", StringType, true),
      StructField("sentence", StringType, true),
      StructField("label", LongType, true),
      StructField("playCount", StringType, true)
    ))
    val testFile = sp.sparkContext
      .textFile("scrapy/download/recent_movies.csv")
    val testRow = loadTestFile(testFile)
    val test = sp.createDataFrame(testRow,dataSchema)
    createModel()
//    modelPrediction(test)
////      .orderBy(desc("prediction"))
//      .coalesce(1)
//      .write//
//      .format("json")
//      .save("results")
  }

}
