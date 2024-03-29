library(ggplot2)
library(paletteer)

#Import data - Fitness of each AMR mutant relative to its ancestor in 4 growth environments
#Full dataset including technical replicate measures
fitnessdata<-read.csv("FigS5-data.csv",na.strings = c("NA"),header = T,sep = ",")

#Restructure dataframe
#Add column 'Resistance' to categorize mutations by resistance class
fitnessdata$Resistance = as.factor(fitnessdata$Mutation)
levels(fitnessdata$Resistance) <- list("None"="none","Fluoroquinolone"="gyrA_S83L_D87N", "Fluoroquinolone"="gyrB_D426N", "Fluoroquinolone"="marR_R77H", "Rifampicin"="rpoB_H526Y", "Rifampicin"="rpoB_S531L", "Aminoglycoside"="rpsL_K43R", "Aminoglycoside"="rpsL_K43T")
#Add column 'facetcol' for facet organization
fitnessdata$facetcol = as.factor(fitnessdata$Mutation)
levels(fitnessdata$facetcol) <- list("D"="none","A"="gyrA_S83L_D87N", "B"="gyrB_D426N", "C"="marR_R77H", "A"="rpoB_H526Y", "B"="rpoB_S531L", "A"="rpsL_K43R", "B"="rpsL_K43T")
#Reorder categorical variables
m<-c("none","gyrA_S83L_D87N","gyrB_D426N","marR_R77H","rpoB_H526Y","rpoB_S531L","rpsL_K43R","rpsL_K43T")
anc<-c("MG1655","OLC682","OLC809","OLC969","PB1","PB2","PB4","PB5","PB6","PB10","PB13","PB15")
en<-c("LB","M9-Glucose","Urine","Colon")
res<-c("None","Fluoroquinolone","Rifampicin","Aminoglycoside")
fitnessdata$Mutation<-factor(fitnessdata$Mutation,levels=m)
fitnessdata$Ancestor<-factor(fitnessdata$Ancestor,levels=anc)
fitnessdata$Environment<-factor(fitnessdata$Environment,levels=en)
fitnessdata$Resistance<-factor(fitnessdata$Resistance,levels=res)
str(fitnessdata)

#Create dataframe to print custom facet labels on plot
mut_labels <- data.frame(Resistance=c('Fluoroquinolone','Fluoroquinolone','Fluoroquinolone','Rifampicin','Rifampicin','Rifampicin','Aminoglycoside','Aminoglycoside','Aminoglycoside'),facetcol=c('A','B','C','A','B','C','A','B','C'),Environment=c('LB','LB','LB','LB','LB','LB','LB','LB','LB'),scaledfit=c(1.4,1.4,1.4,1.4,1.4,1.4,1.4,1.4,1.4),label=c('GyrA (S83L, D87N)','GyrB (D426N)','MarR (R77H)','RpoB (H526Y)','RpoB (S531L)','','RpsL (K43R)','RpsL (K43T)',''))
resist<-c("Fluoroquinolone","Rifampicin","Aminoglycoside")
mut_labels$Resistance<-factor(mut_labels$Resistance,levels=resist)

#Color palette
cbcolor <- c("#CC79A7", "#D55E00","#0072B2","#F0E442")
anccolor<-c(paletteer_d("tidyquant::tq_dark"))

#Subset dataframe to exclude Mutation='none' data from plot
mutationfit<-subset(fitnessdata,Mutation!="none")

plotfigS5<-ggplot(data=mutationfit,aes(x=Environment,y=scaledfit))+
  theme_bw()+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+
  geom_abline(linewidth=0.5,linetype="dashed",color="darkgrey",aes(slope=0,intercept=1))+
  stat_summary(aes(group = Ancestor,color = Ancestor),fun = mean, geom = "path",linewidth=0.75,alpha=0.75)+
  stat_summary(aes(group = Ancestor,color = Ancestor),fun = mean, geom = "point",size = 1.75) +
  stat_summary(aes(group = Ancestor,color = Ancestor),fun.data = mean_se, geom = "errorbar", width = 0.1) +
  coord_cartesian(ylim=c(0.3,1.5))+ #do not use +ylim() here or points used to calculate mean/se are excluded
  scale_y_continuous(breaks=c(0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3,1.4),
                     labels=c(0.4,'',0.6,'',0.8,'',1,'',1.2,'',1.4))+
  scale_fill_manual(values=anccolor)+
  scale_color_manual(values=anccolor)+
  theme(legend.position = "right")+
  labs(x="Environment",y="Relative fitness")+
  theme(axis.title.x = element_text(size=12,margin = margin(t = 0.25,unit="cm")))+
  theme(axis.text.x = element_text(size=10))+
  theme(axis.title.y = element_text(size=12,margin = margin(r = 0.25,unit="cm")))+
  theme(axis.text.y = element_text(size=10))+
  facet_grid(Resistance ~ facetcol)+ #Facets based on 'Resistance' and 'facetcol' categories
  geom_text(data = mut_labels,label=mut_labels$label,hjust = 0)+ #Custom annotate facet panels
  theme(strip.text.x = element_blank(),strip.text.y = element_text(size = 10))+
  theme(strip.background = element_rect(color="black", fill="gray95",linetype="solid"))
plotfigS5

#Save as png
ggsave("FigS5-final.png", plot = plotfigS5, dpi=1200, width = 25, height =18, units = "cm",bg='white')