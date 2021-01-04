library(ggplot2)
library(ggridges)

# LOAD DATA
cwd = paste(getwd(),"/src/blocking/", sep="")
a = read.csv(paste(cwd, "100_txt",sep=""), header=FALSE, col.names=c("time"))
a$type = "100"
b = read.csv(paste(cwd, "200_txt",sep=""), header=FALSE, col.names=c("time"))
b$type = "200"
c = read.csv(paste(cwd, "300_txt",sep=""), header=FALSE, col.names=c("time"))
c$type = "300"
d = read.csv(paste(cwd, "400_txt",sep=""), header=FALSE, col.names=c("time"))
d$type = "400"
e = read.csv(paste(cwd, "500_txt",sep=""), header=FALSE, col.names=c("time"))
e$type = "500"
f = read.csv(paste(cwd, "600_txt",sep=""), header=FALSE, col.names=c("time"))
f$type = "600"
g = read.csv(paste(cwd, "700_txt",sep=""), header=FALSE, col.names=c("time"))
g$type = "700"
h = read.csv(paste(cwd, "800_txt",sep=""), header=FALSE, col.names=c("time"))
h$type = "800"
i = read.csv(paste(cwd, "900_txt",sep=""), header=FALSE, col.names=c("time"))
i$type = "900"
j = read.csv(paste(cwd, "1000_txt",sep=""), header=FALSE, col.names=c("time"))
j$type = "1000"
k = read.csv(paste(cwd, "1100_txt",sep=""), header=FALSE, col.names=c("time"))
k$type = "1100"
l = read.csv(paste(cwd, "1200_txt",sep=""), header=FALSE, col.names=c("time"))
l$type = "1200"
n = read.csv(paste(cwd, "1300_txt",sep=""), header=FALSE, col.names=c("time"))
n$type = "1300"
m = read.csv(paste(cwd, "1400_txt",sep=""), header=FALSE, col.names=c("time"))
m$type = "1400"
o = read.csv(paste(cwd, "1500_txt",sep=""), header=FALSE, col.names=c("time"))
o$type = "1500"
#dat <- rbind(a,c,e,g,i,k,n,o)
dat <- rbind(a,b,c,d,e,f,g,h,i,j,k,l,n,m,o)
dat$time <- dat$time / 1000
dat$type = as.factor(dat$type)
p = ggplot(dat, aes(x=type, y=time)) +
  geom_violin(trim=FALSE, fill='#A4A4A4', color="darkred")+
  geom_boxplot(width=0.1) + theme_minimal()+
  scale_y_continuous("Millisecond", breaks = round(seq(3500, 7000, by = 300),1)) +
  labs(title = "Time Use in different implementations", 
       subtitle = "Different performance in non-unroll, manual unroll and unroll with gcc option",
       x = "",
       y = "") +
  theme_minimal() +
  theme(legend.position = "none")
p
ggplot(data = dat, aes(x=type, y=time)) + geom_boxplot(aes(fill=type))


ggplot(dat, aes(x = time, y = type, fill = type)) +
  geom_density_ridges(
    aes(point_color = type, point_fill = type),
    alpha = .2, point_alpha = 1, jittered_points = TRUE
  ) +labs(
    title = 'Density distribution of different loop order',
    subtitle = 'Order of character is the loop order. e.g loop order of ijk is i, j, and k from outermost loop to innermost loop. ',
    x = "Millisecond",
    y = "") +scale_x_continuous("Millisecond", breaks = round(seq(800, 2500, by = 100),1)) + theme_minimal() + theme(legend.position = "none")


