library(ggplot2)
library(paletteer)

#Import data - Fitness of each ancestor relative to MG1655-YFP 
#Dataset includes mean of 4 technical replicate measures
figS11data<-read.csv("FigS11-data.csv",na.strings = c("NA"),header = T,sep = ",")

#Reorder categorical variables
anc<-c("OLC809","PB2","PB5","PB6","PB10","MG1655","OLC682","OLC969","PB1","PB4","PB13","PB15")
en<-c("LB","M9-Glucose","Urine","Colon")
figS11data$Ancestor<-factor(figS11data$Ancestor,levels=anc)
figS11data$Environment<-factor(figS11data$Environment,levels=en)
str(figS11data)

#Color palette
anccolor<-c(paletteer_d("tidyquant::tq_dark"))

plotfigS11<-ggplot(data=figS11data,aes(x=Marked_Group,y=fit))+
  theme_bw()+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+
  geom_abline(linewidth=0.5,linetype="dashed",color="darkgrey",aes(slope=0,intercept=1))+
  geom_boxplot(color="black",size=0.5,alpha=0.2,outlier.shape=NA)+
  geom_jitter(aes(color = Ancestor,shape=Environment),size=2.5,width=0.3) +
  scale_fill_manual(name="Strain",values=anccolor)+
  scale_color_manual(name="Strain",values=anccolor)+
  scale_shape_manual(name="Environment",values=c(15,16,17,18))+
  scale_y_continuous(breaks=c(0.75,1,1.25,1.5,1.75,2,2.25,2.5),
                     labels=c(0.75,1.00,1.25,1.5,1.75,2.00,2.25,2.5))+
  scale_x_discrete(labels=c("Common" = "Common competitor\n(MG1655-YFP)", "Isogenic" = "Isogenic YFP-marked\nstrain"))+
  labs(x="Competitor used in fitness estimates\n of AMR mutations",y="Fitness relative to MG1655-YFP")+
  theme(legend.position = "right",legend.box="horizontal",legend.title = element_text(size=12),legend.text =   element_text(size=10))+
  guides(color = guide_legend(order = 2),
         shape = guide_legend(order = 1))+
  theme(axis.title.x = element_text(size=12,margin = margin(t = 0.25,unit="cm")))+
  theme(axis.text.x = element_text(size=10))+
  theme(axis.title.y = element_text(size=12,margin = margin(r = 0.25,unit="cm")))+
  theme(axis.text.y = element_text(size=10))
plotfigS11

#Save as png
ggsave("FigS11-final.png", plot = plotfigS11, dpi=1200, width = 18, height = 12, units = "cm",bg='white')
