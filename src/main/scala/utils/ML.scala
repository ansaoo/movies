package utils

import model.Infos
import org.apache.spark.ml.Pipeline
import org.apache.spark.ml.classification.{DecisionTreeClassifier, GBTClassifier, NaiveBayes}
import org.apache.spark.ml.feature._
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.{DataFrame, Row, SparkSession}


/**
  * Created by inti on 16/06/17.
  */
object ML {

  def loadFile(file: RDD[String]): RDD[Row] = {
    file.map(_.split("\t"))
      .flatMap { content =>
        try {
          val id = content(0).toLong
          val genre = content(2).replace(" / ", " ")
          val director = content(3).replace(" / ", " ")
          val userrating = 0*5
          val rating = content(5).toDouble*5
          val rate = if (userrating >= rating) userrating
          else rating.round
          val text = List(content(1), director)
          Some(Infos(id,"0",text.mkString(" "), rate, content(6)))
        }
        catch {
          case e: Exception => None
        }
      }.map{info =>
      Row(info.id,info.title,info.sentence,info.rate,info.playCount)}
  }

  def loadTestFile(file: RDD[String]): RDD[Row] = {
    file.map(_.split("\t"))
      .flatMap { case Array(id, title, genres, synopsis, rate) => {
        val genre = genres.replace(" / ", " ")
//        val director = directors.replace(" / ", " ")
//        genre supprime pour ameliorer le taux
        val text = List(synopsis)
        val playCount = "0"
        println(s"$id ... ok")
        Some(Infos(id.toLong,title,text.mkString(" "), rate.toLong, playCount))
      }}.map{info =>
      Row(info.id,info.title,info.sentence,info.rate,info.playCount)}
  }

  def toDF(rdd: RDD[Infos]): RDD[Row] = {
    rdd.map{info =>
      Row(info.id,info.title,info.sentence,info.rate,info.playCount)}
  }

  def transformData(sentenceData: DataFrame): DataFrame = {
    val tokenizer = new Tokenizer()
      .setInputCol("sentence")
      .setOutputCol("words")
    val hashingTF = new HashingTF()
      .setInputCol(tokenizer.getOutputCol)
      .setOutputCol("rawFeatures")
    val idf = new IDF()
      .setInputCol(hashingTF.getOutputCol)
      .setOutputCol("features")
    val wordsData: DataFrame = tokenizer.transform(sentenceData)
    val featurizedData: DataFrame = hashingTF.transform(wordsData)
    val idfModel: IDFModel = idf.fit(featurizedData)
    idfModel.transform(featurizedData)
  }

  def createPipeline(): Pipeline = {
    val regexTokenizer = new RegexTokenizer()
      .setMinTokenLength(5)
      .setToLowercase(true)
      .setInputCol("sentence")
      .setOutputCol("words")
    val tokenizer = new Tokenizer()
      .setInputCol("sentence")
      .setOutputCol("words")
    val hashingTF = new HashingTF()
      .setInputCol(regexTokenizer.getOutputCol)
      .setOutputCol("rawFeatures")
    val idf = new IDF()
      .setInputCol(hashingTF.getOutputCol)
      .setOutputCol("features")
//    val model = new NaiveBayes()
    val model = new DecisionTreeClassifier()
    val pipeline = new Pipeline()
      .setStages(Array(regexTokenizer, hashingTF, idf, model))
    pipeline
  }
}
