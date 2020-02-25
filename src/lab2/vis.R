#!/usr/bin/env Rscript
library(ggplot2)

args = commandArgs(trailingOnly=TRUE)

if (length(args) != 4) {
    stop("Two params: 1&2.paths to data, 2&3.name of plot", call.=FALSE)
} 


# LOAD DATA
dat = read.csv(args[1], header=FALSE, col.names=c("time"))
dat2 = read.csv(args[2], header=FALSE, col.names=c("time"))

diff_ = dat$time - dat2$time

dat$label <- args[3]
dat2$label <- args[4]
# Rscript vis.R data/Unroll.txt data/Non-unroll.txt Unroll Non-unroll
dat <- rbind(dat,dat2)

diff <- ggplot(data.frame(diff_ = diff_), aes(x = c(1:length(diff_)), y = diff_)) + 
        geom_line(size = 1.5, color = "lightgrey") +
        geom_point(size = 3, color = "steelblue") +
        geom_hline(yintercept = 0, color = "orange")+
        labs(y = "log Millisecond", 
            x = "# of Iter",
            title = paste(args[3]," Versus ", args[4], " Benchmark", sep = ""),
            subtitle = paste("Different performance between ", args[3], " and ", args[4], sep="")) +
        theme_minimal() + theme(legend.position = "none")


ggsave(paste("pic/diff_", args[3],"_", args[4], ".png", sep=""), diff, width = 7, height = 7)


p = ggplot(dat, 
        aes(x = factor(label), 
            y = log(time), 
            color = label)) +
    geom_violin(fill = "cornflowerblue") +
    geom_boxplot(width = .2, 
                fill = "orange",
                outlier.color = "orange",
                outlier.size = 2)+
    scale_y_continuous("Log Millisecond") +
    labs(title = "Time Use in difference CPP code", 
        subtitle = paste("Different performance between ", args[3], " and ", args[4], sep=""),
        x = "",
        y = "") +
    theme_minimal() +
    theme(legend.position = "none")


ggsave(paste("pic/violin_", args[3],"_", args[4], ".png", sep=""), p, width = 7, height = 7)

if (file.exists("Rplots.pdf"))
    file.remove("Rplots.pdf")