library(ggplot2)
library(ggridges)

# LOAD DATA
cwd = paste(getwd(),"/src/interchange/", sep="")
gcc = read.csv(paste(cwd, "original.txt2",sep=""), header=FALSE, col.names=c("time"))
gcc$type = "ijk with option"
MNP = read.csv(paste(cwd, "MNP.txt2",sep=""), header=FALSE, col.names=c("time"))
MNP$type = "jik"
NMP = read.csv(paste(cwd, "NMP.txt2",sep=""), header=FALSE, col.names=c("time"))
NMP$type = "ijk"
MPN = read.csv(paste(cwd, "MPN.txt2",sep=""), header=FALSE, col.names=c("time"))
MPN$type = "jki"
NPM = read.csv(paste(cwd, "NPM.txt2",sep=""), header=FALSE, col.names=c("time"))
NPM$type = "ikj"
PMN = read.csv(paste(cwd, "PMN.txt2",sep=""), header=FALSE, col.names=c("time"))
PMN$type = "kji"
PNM = read.csv(paste(cwd, "PNM.txt2",sep=""), header=FALSE, col.names=c("time"))
PNM$type = "kij"


dat <- rbind(gcc,MNP,NMP, MPN,NPM,PMN,PNM)
dat$time <- dat$time/1000


ggplot(dat, aes(x = time, y = type, fill = type)) +
  geom_density_ridges(
    aes(point_color = type, point_fill = type),
    alpha = .2, point_alpha = 1, jittered_points = TRUE
  ) +labs(
    title = 'Density distribution of different loop order',
    subtitle = 'Order of character is the loop order. e.g loop order of ijk is i, j, and k from outermost loop to innermost loop. ',
    x = "Millisecond",
    y = "") + theme_minimal() + theme(legend.position = "none")
  







# vio