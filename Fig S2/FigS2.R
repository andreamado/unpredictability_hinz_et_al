library(ggplot2)

#Import data - Carrying capacity measurements of ancestors grown in 4 assay environments
#Dataset includes mean concentration values (CFU/ml) of two technical replicates
figS2data<-read.csv("FigS2-data.csv",na.strings = c("na"),header = T, sep = ",")
str(figS2data)

#Reorder categorical variables
m<-c("LB","M9-Glucose","Urine","Colon")
figS2data$Environment<-factor(figS2data$Environment,levels=m)
figS2data

plotfigS2<-ggplot(data=figS2data,aes(x=Environment,y=CFU_per_ml))+
  theme_bw()+
  geom_boxplot(color="black",size=0.5,alpha=0.4,outlier.shape=NA)+
  geom_point(pch=16,color='darkgray',alpha=0.8,size=2.5,position = position_jitter(width=0.3))+
  scale_y_continuous(trans='log',limits=c(10^7,10^10),breaks=c(10^6,10^7,10^8,10^9,10^10))+
  labs(x="Environment",y="Carrying capacity (CFU/ml)")+
  theme(axis.text.y = element_text(size=10))
plotfigS2
ggsave("FigS2-final.png", plot = plotfigS2, dpi=1200,width =10, height = 10, units = "cm",bg='white')
