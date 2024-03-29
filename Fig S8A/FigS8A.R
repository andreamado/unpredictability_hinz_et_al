library(ggplot2)
library(paletteer)

#Import data - Fitness of each ancestor relative to MG1655-YFP 
#Dataset includes technical replicate measures
fitnessdata<-read.csv("FigS8A-data.csv",na.strings = c("NA"),header = T,sep = ",")

#Reorder categorical variables
anc<-c("MG1655","OLC682","OLC809","OLC969","PB1","PB2","PB4","PB5","PB6","PB10","PB13","PB15")
en<-c("LB","M9-Glucose","Urine","Colon")
fitnessdata$Ancestor<-factor(fitnessdata$Ancestor,levels=anc)
fitnessdata$Environment<-factor(fitnessdata$Environment,levels=en)
str(fitnessdata)

#Color palette
anccolor<-c(paletteer_d("tidyquant::tq_dark"))

plotfigS8A<-ggplot(data=fitnessdata,aes(x=Ancestor,y=fit))+
  theme_bw()+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+
  geom_abline(linewidth=0.5,linetype="dashed",color="darkgrey",aes(slope=0,intercept=1))+
  stat_summary(aes(group = Ancestor,color = Ancestor),fun = mean, geom = "point",size = 1.75) +
  stat_summary(aes(group = Ancestor,color = Ancestor),fun.data = mean_se, geom = "errorbar", width = 0.2) +
  scale_y_continuous(breaks=c(0.75,1,1.25,1.5,1.75,2,2.25,2.5),
                     labels=c(0.75,1.00,1.25,1.5,1.75,2.00,2.25,2.5))+
  scale_fill_manual(values=anccolor)+
  scale_color_manual(values=anccolor)+
  labs(x="Ancestor",y="Relative fitness",color="Genotype")+
  theme(legend.position = "right",legend.title = element_text(size=12),legend.text = element_text(size=10))+
  theme(axis.title.x = element_text(size=12,margin = margin(t = 0.25,unit="cm")))+
  theme(axis.text.x = element_text(size=10))+
  theme(axis.text.x = element_text(angle = 90,hjust=1,vjust=0.5))+
  theme(axis.title.y = element_text(size=12,margin = margin(r = 0.25,unit="cm")))+
  theme(axis.text.y = element_text(size=10))+
  facet_wrap( ~ Environment)+
  theme(strip.background = element_rect(color="black", fill="gray95",linetype="solid"))
plotfigS8A

#Save as png
ggsave("FigS8A-final.png", plot = plotfigS8A, dpi=1200, width = 15, height = 12, units = "cm",bg='white')
