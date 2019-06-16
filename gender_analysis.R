if (!require(ggplot2)) {
  install.packages("ggplot2", repos="http://cran.us.r-project.org")
}
library("ggplot2")
if (!require(plyr)) {
  install.packages("plyr", repos="http://cran.us.r-project.org")
}
library(plyr)
if (!require(data.table)) {
  install.packages("data.table", repos="http://cran.us.r-project.org")
}
library(data.table)
if (!require(grid)) {
  install.packages("grid", repos="http://cran.us.r-project.org")
}
library(grid)

workingDir = '/Users/michaeltauberg/projects/movies'
setwd(workingDir)


GenerateGenderGraphs <- function(mdata, data_name, csv_field_name) {
# paramaterize this all  - START

  mdata$gross = as.numeric(as.character(mdata$gross))
  movie_data = mdata[grep("United States", mdata$country), ] # US movies only - misses gladiator - fix country?
  movie_data = movie_data[grep("English", movie_data$language), ]
  u = movie_data[movie_data$gender == "unknown",]
  f = movie_data[movie_data$gender == "female",]
  m = movie_data[movie_data$gender == "male",]
  
  year_stats = c()
  movie_data$year = factor(movie_data$year)
  for (year in levels(droplevels(movie_data$year))) {
    print(year)
    movie_data_year = movie_data[movie_data$year == year,]
    #actors_year = actors_year[complete.cases(actors_year), ]
    u = movie_data_year[movie_data_year$gender == "unknown",]
    f = movie_data_year[movie_data_year$gender == "female",]
    m = movie_data_year[movie_data_year$gender == "male",]
    percent_male = as.numeric(nrow(m)/nrow(movie_data_year)*100)
    percent_female = as.numeric(nrow(f)/nrow(movie_data_year)*100)
    percent_unknown = as.numeric(nrow(u)/nrow(movie_data_year)*100)
    row = c(year,nrow(m), nrow(f), nrow(u), percent_male, percent_female, percent_unknown)
    year_stats = rbind(year_stats,row)
  }
  
  year_stats = as.data.frame(year_stats)
  colnames(year_stats) = c("year","num_males","num_females","num_unknown","percent_male","percent_female", "percent_unknown")
  year_stats = year_stats[year_stats$year != "2000",]
  
  
  year_stats$percent_female = as.numeric(as.character(year_stats$percent_female))
  year_stats$year = as.numeric(year_stats$year)
  p = ggplot(year_stats, aes(x=year, y=percent_female)) + geom_point()
  p = p  + geom_smooth(method='lm', se = FALSE) 
  p = p + ggtitle(sprintf("Percentage of Female Hollywood %s since 2000", data_name))
  p = p + theme(axis.text.x=element_text(angle=90, hjust=1))
  p = p + theme(axis.text=element_text(size=16), axis.title=element_text(size=14))
  p = p + ylab(sprintf("Percentage of Female %s (percent)", data_name)) + xlab("Year") 
  p = p  + theme_minimal() 
  p = p + scale_x_discrete(limits = c(2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018))
  ggsave(filename = sprintf("./%s_percent_female.png", data_name), plot=p, width=5, height=3.5) 
  
  # plot all 3 over time
  #test = as.data.frame(t(year_stats))  
  stats = melt(year_stats, id=c("year"))
  stats = stats[grep("percent", stats$variable),]
  stats$value = as.numeric(as.character(stats$value))
  
  gender_palette <- c("#81FFF4","pink", "#C8CFCE")
  stats = stats[stats$year != 1,]
  stats = stats[stats$year != 20,]
  p = ggplot(stats, aes(x=year, y=value, group=variable)) + geom_line(aes(colour=variable), size=1)
  p = p + ggtitle(sprintf("Percent Male, Female, and Uknown %s over time  (percentage/time)", data_name))
  p = p + xlab("Year") + ylab("%") # add axis labels
  #p = p + theme(axis.text.x = element_text(angle = 90, hjust = 1))
  p = p + theme(text = element_text(size=10), axis.text.x=element_text(angle=90, hjust=1))
  p = p  + theme_minimal() 
  p = p + scale_color_manual(values=gender_palette)
  ggsave(filename = sprintf("./%s_percentages_time.png", data_name), plot=p, width=7, height=5.5) 
  
  movie_data_2018 = movie_data[movie_data$year == "2018",]
  movie_data_2018 = ddply(movie_data_2018, csv_field_name, summarise, gross = sum(gross, na.rm=TRUE)  )
  movie_data_2018 = movie_data_2018[order(movie_data_2018$gross, decreasing=TRUE),]
  
  # make a pie chart 
  gender_palette <- c("pink","#81FFF4","#C8CFCE")
  year_stats_2018 = year_stats[year_stats$year == 19, ]
  #percentages = c(year_stats_2018)
  t_year_stats_2018 = t(year_stats_2018)
  t_year_stats_2018 = as.data.frame(melt(t_year_stats_2018[c(5,6,7),]))
  t_year_stats_2018$group = c("percent male", "percent female", "percent unknown")
  t_year_stats_2018$value = as.numeric(as.character(t_year_stats_2018$value))
  p = ggplot(t_year_stats_2018, aes(x="", y=value, fill=group)) + geom_bar(width = 1, stat = "identity")
  p = p + coord_polar("y", start=0) + scale_fill_manual(values=gender_palette) 
  p = p  + theme_void() 
  p = p + ggtitle(sprintf("Gender Balance of All %s in 2018 Movies", data_name))
  ggsave(filename = sprintf("./2018_%s_piechart.png", data_name), plot=p, width=6, height=6) 
  
  # this can't be the same for all
  #gender_palette <- c("pink","#81FFF4")
  #top_movie_data_2018 = movie_data_2018[1:15,] 
  #top_movie_data_2018$gender = c('M','F','F','M','M','M','M','F','M','M','M','M','M','F','M')
  #top_movie_data_2018 = top_movie_data_2018[order(top_movie_data_2018$gross, decreasing=TRUE),]
  #top_movie_data_2018$starring = factor(top_movie_data_2018$starring, levels = top_movie_data_2018$starring[order(top_movie_data_2018$gross, decreasing=TRUE)])
  #p = ggplot(top_movie_data_2018, aes(x=starring, y=gross, fill=gender)) + geom_bar(stat="identity") 
  #p = p + ggtitle(sprintf("Top 15 U.S. %s in 2018 by Box Office Gross (dollars)", data_name))
  #p = p + theme(axis.text.x=element_text(angle=90, hjust=1))
  #p = p + theme(axis.text=element_text(size=16), axis.title=element_text(size=14))
  #p = p + xlab("Actor") + ylab("Total Box Office in 2018") 
  #p = p + scale_fill_manual(values=gender_palette) 
  #ggsave(filename = sprintf("./%s_top15.png", data_name) , plot=p, width=9, height=8)
  
  #gender_palette <- c("pink","#81FFF4")
  #top_movie_data_2018 = movie_data_2018[1:15,] 
  #top_movie_data_2018$gender = c('M','M','F','M','M','M','M','M','F','M','M','F','M','M','F')
  #top_movie_data_2018 = top_movie_data_2018[order(top_movie_data_2018$gross, decreasing=TRUE),]
  #top_movie_data_2018$producer = factor(top_movie_data_2018$producer, levels = top_movie_data_2018$producer[order(top_movie_data_2018$gross, decreasing=TRUE)])
  #p = ggplot(top_movie_data_2018, aes(x=producer, y=gross, fill=gender)) + geom_bar(stat="identity") 
  #p = p + ggtitle(sprintf("Top 15 U.S. %s in 2018 by Box Office Gross (dollars)", data_name))
  #p = p + theme(axis.text.x=element_text(angle=90, hjust=1))
  #p = p + theme(axis.text=element_text(size=16), axis.title=element_text(size=14))
  #p = p + xlab("Producer") + ylab("Total Box Office in 2018") 
  #p = p + scale_fill_manual(values=gender_palette) 
  #ggsave(filename = sprintf("./%s_top15.png", data_name) , plot=p, width=9, height=8)
  
  #gender_palette <- c("#81FFF4")
  #top_movie_data_2018 = movie_data_2018[1:15,] 
  #top_movie_data_2018$gender = c('M','M','M','M','M','M','M','M','M','M','M','M','M','M','M')
  #top_movie_data_2018 = top_movie_data_2018[order(top_movie_data_2018$gross, decreasing=TRUE),]
  #top_movie_data_2018$director = factor(top_movie_data_2018$director, levels = top_movie_data_2018$director[order(top_movie_data_2018$gross, decreasing=TRUE)])
  #p = ggplot(top_movie_data_2018, aes(x=director, y=gross, fill=gender)) + geom_bar(stat="identity") 
  #p = p + ggtitle(sprintf("Top 15 U.S. %s in 2018 by Box Office Gross (dollars)", data_name))
  #p = p + theme(axis.text.x=element_text(angle=90, hjust=1))
  #p = p + theme(axis.text=element_text(size=16), axis.title=element_text(size=14))
  #p = p + xlab("Director") + ylab("Total Box Office in 2018") 
  #p = p + scale_fill_manual(values=gender_palette) 
  #ggsave(filename = sprintf("./%s_top15.png", data_name) , plot=p, width=9, height=8)
  
  #gender_palette <- c("#81FFF4")
  #top_movie_data_2018 = movie_data_2018[1:15,] 
  #top_movie_data_2018$gender = c('M','M','M','M','M','M','M','M','M','M','M','M','M','M','M')
  #top_movie_data_2018 = top_movie_data_2018[order(top_movie_data_2018$gross, decreasing=TRUE),]
  #top_movie_data_2018$writer = factor(top_movie_data_2018$writer, levels = top_movie_data_2018$writer[order(top_movie_data_2018$gross, decreasing=TRUE)])
  #p = ggplot(top_movie_data_2018, aes(x=writer, y=gross, fill=gender)) + geom_bar(stat="identity") 
  #p = p + ggtitle(sprintf("Top 15 U.S. %s in 2018 by Box Office Gross (dollars)", data_name))
  #p = p + theme(axis.text.x=element_text(angle=90, hjust=1))
  #p = p + theme(axis.text=element_text(size=16), axis.title=element_text(size=14))
  #p = p + xlab("Writer") + ylab("Total Box Office in 2018") 
  #p = p + scale_fill_manual(values=gender_palette) 
  #ggsave(filename = sprintf("./%s_top15.png", data_name) , plot=p, width=9, height=8)
  
  gender_palette <- c("pink", "#81FFF4")
  top_movie_data_2018 = movie_data_2018[1:15,] 
  top_movie_data_2018$gender = c('M','M','M','M','M','M','M','M','M','F','M','M','M','M','M')
  top_movie_data_2018 = top_movie_data_2018[order(top_movie_data_2018$gross, decreasing=TRUE),]
  top_movie_data_2018$music = factor(top_movie_data_2018$music, levels = top_movie_data_2018$music[order(top_movie_data_2018$gross, decreasing=TRUE)])
  p = ggplot(top_movie_data_2018, aes(x=music, y=gross, fill=gender)) + geom_bar(stat="identity") 
  p = p + ggtitle(sprintf("Top 15 U.S. %s in 2018 by Box Office Gross (dollars)", data_name))
  p = p + theme(axis.text.x=element_text(angle=90, hjust=1))
  p = p + theme(axis.text=element_text(size=16), axis.title=element_text(size=14))
  p = p + xlab("Musician") + ylab("Total Box Office in 2018") 
  p = p + scale_fill_manual(values=gender_palette) 
  ggsave(filename = sprintf("./%s_top15.png", data_name) , plot=p, width=9, height=8)
  

}
####################################################
###################################################################################
####################################################




data_name = "Actors"
csvName = "all_actors_movies_gender_gold.csv"
csv_field_name = "starring"
dt = read.csv(csvName)
dt = dt[!duplicated(dt[,c('name',csv_field_name)], fromLast=FALSE),] 
dt = dt[dt$starring != '', ]
GenerateGenderGraphs(dt, data_name, csv_field_name)

data_name = "Producers"
csvName = "all_producers_gender_gold.csv"
csv_field_name = "producer"
dt = read.csv(csvName)
dt = dt[!duplicated(dt[,c('name',csv_field_name)], fromLast=FALSE),] 
dt = dt[dt$producer != '', ]
GenerateGenderGraphs(dt, data_name, csv_field_name)

csvName = "all_writers_gender.csv"
data_name = "Writers"
csv_field_name = "writer"
dt = read.csv(csvName)
dt = dt[!duplicated(dt[,c('name',csv_field_name)], fromLast=FALSE),] 
dt = dt[dt$writer != '', ]
GenerateGenderGraphs(dt, data_name, csv_field_name)

csvName = "all_music_gender.csv"
data_name = "Musicians"
csv_field_name = "music"
dt = read.csv(csvName)
dt = dt[!duplicated(dt[,c('name',csv_field_name)], fromLast=FALSE),] 
dt = dt[dt$music != '', ]
GenerateGenderGraphs(dt, data_name, csv_field_name)

csvName = "all_directors_gender.csv"
data_name = "Directors"
csv_field_name = "director"
dt = read.csv(csvName)
dt = dt[!duplicated(dt[,c('name',csv_field_name)], fromLast=FALSE),] 
dt = dt[dt$director != '', ]
GenerateGenderGraphs(dt, data_name, csv_field_name)
