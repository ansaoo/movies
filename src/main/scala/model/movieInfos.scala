package model

/**
  * Created by sasoo on 29/07/17.
  */
case class Infos (
                  id: Long,
                  title: String,
                  sentence: String,
                  rate: Long,
                  playCount: String
                 )
case class RecentMovies (
                        title: String,
                        genre: String,
                        director: String,
                        synopsis: String,
                        rate: Long
                        )