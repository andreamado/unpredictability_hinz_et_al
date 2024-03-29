library(ggplot2)

#Import data - Fitness of each AMR mutant relative to its ancestor in 4 growth environments
#Mutants are classified by type of competitor used in the competitions (common or isogenic)
#Dataset includes mean values of four technical replicate measures
figS12data<-read.csv("FigS12-data.csv",na.strings = c("NA"),header = T,sep = ",")

#Reorder categorical variables
m<-c("none","gyrA_S83L_D87N","gyrB_D426N","marR_R77H","rpoB_H526Y","rpoB_S531L","rpsL_K43R","rpsL_K43T")
figS12data$Mutation<-factor(figS12data$Mutation,levels=m)
str(figS12data)

#Color palette
cbcolor <- c("#CC3333","#003399")
cbfill <- c("#CC3333","#003399")

#Subset data - AMR mutants only
mutonly<-subset(figS12data,Mutation!="none")

plotfigS12<-ggplot(data=mutonly,aes(x=Mutation,y=scaledfit))+
  theme_bw()+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+
  geom_abline(linewidth=0.5,linetype="dashed",color="darkgrey",aes(slope=0,intercept=1))+
  geom_boxplot(aes(fill=Marked_type),color="black",size=0.5,alpha=0.2,outlier.shape=NA)+
  geom_point(aes(color=Marked_type),pch=16,size=1.5,alpha=.6, position = position_jitterdodge(dodge.width=0.75,jitter.width=0.2))+
  coord_cartesian(ylim=c(0.3,1.5))+ #do not use +ylim() here or points used to calculate mean/se are excluded
  scale_y_continuous(breaks=c(0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3,1.4),
                     labels=c(0.4,'',0.6,'',0.8,'',1,'',1.2,'',1.4))+
  scale_x_discrete(labels=c("gyrA_S83L_D87N" = "GyrA\n(S83L, D87N)", "gyrB_D426N" = "GyrB\n(D426N)","marR_R77H" = "MarR\n(R77H)",
                            "rpoB_H526Y" = "RpoB\n(H526Y)", "rpoB_S531L" = "RpoB\n(S531L)",
                            "rpsL_K43R" = "RpsL\n(K43R)", "rpsL_K43T" = "RpsL\n(K43T)"))+
  scale_fill_manual(name="Competitor",values=cbfill)+
  scale_color_manual(name="Competitor",values=cbcolor)+
  theme(legend.position = "right")+
  labs(x="Mutation",y="Relative fitness")+
  theme(axis.title.x = element_text(size=12,margin = margin(t = 0.25,unit="cm")))+
  theme(axis.text.x = element_text(size=10))+
  theme(axis.title.y = element_text(size=12,margin = margin(r = 0.25,unit="cm")))+
  theme(axis.text.y = element_text(size=10))
plotfigS12

#Save as png
ggsave("FigS12-final.png", plot = plotfigS12, dpi=1200,width = 9.06, height = 5.91, units = "in",bg='white')
