package core

import model.RecentMovies
import org.apache.spark.SparkConf
import org.apache.spark.ml.PipelineModel
import org.apache.spark.ml.evaluation.MulticlassClassificationEvaluator
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.types.{LongType, StringType, StructField, StructType}
import org.apache.spark.sql.{DataFrame, Row, SparkSession}
import utils.ML._

/**
  * Created by sasoo on 27/07/17.
  */
object mlProcess {

  def loadData(): DataFrame = {
//    val conf = new SparkConf().setAppName("Test-App")
//    conf.set("spark.serialization","org.apache.spark.serializer.KyroSerializer")
//    conf.set("spark.io.compression.codec","org.apache.spark.io.SnappyCompressionCodec")
    val sp = SparkSession.builder()
      .appName("SparkSesion")
      .master("local[*]")
      .getOrCreate()

    implicit val dataFile: RDD[String] = sp.sparkContext.textFile("src/main/resources/movie_view.csv")
    implicit val dataRow: RDD[Row] = loadFile(dataFile)
    val dataSchema = StructType(Array(
      StructField("index", LongType, true),
      StructField("title", StringType, true),
      StructField("sentence", StringType, true),
      StructField("label", LongType, true),
      StructField("playCount", StringType, true)
    ))
    sp.createDataFrame(dataRow, dataSchema)
  }

  def createModel(): Unit = {
    val data = loadData()
    val Array(trainingData, testData) = data.randomSplit(Array(0.7,0.3))

    val model = createPipeline().fit(trainingData)
    val predictions = model.transform(testData)
    val evaluator = new MulticlassClassificationEvaluator()
        .setLabelCol("label")
        .setPredictionCol("prediction")
        .setMetricName("accuracy")
    val accuracy = evaluator.evaluate(predictions)
    model.write.overwrite().save("mlModel")
    println(s"***********\n$accuracy\n***********")
  }

  def modelPrediction(testDF: DataFrame): DataFrame = {
    val model = try {
      PipelineModel.load("mlModel")
    }
    catch {
      case e: Exception => createModel(); PipelineModel.load("mlModel")
    }
    model.transform(testDF)
        .select("index","title","prediction")
  }

  def predictRate(recentsRDD: RDD[RecentMovies]): Unit = {
    val sp = SparkSession.builder()
      .appName("SparkSesion")
      .master("local[*]")
      .getOrCreate()
    import sp.implicits._
    val recentsDF = recentsRDD.toDF()
    val prediction = modelPrediction(recentsDF)
  }
}
