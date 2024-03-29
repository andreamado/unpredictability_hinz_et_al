library(ggplot2)

#Import data - Fitness of each AMR mutant relative to its ancestor in 4 growth environments
#Dataset includes mean values of four technical replicate measures
fig3data<-read.csv("Fig3-data.csv",na.strings = c("NA"),header = T,sep = ",")

#Reorder categorical variables
m<-c("none","gyrA_S83L_D87N","gyrB_D426N","marR_R77H","rpoB_H526Y","rpoB_S531L","rpsL_K43R","rpsL_K43T")
en<-c("LB","M9-Glucose","Urine","Colon")
res<-c("Fluoroquinolone resistance","Rifampicin resistance","Aminoglycoside resistance")
fig3data$Mutation<-factor(fig3data$Mutation,levels=m)
fig3data$Environment<-factor(fig3data$Environment,levels=en)
fig3data$Resistance<-factor(fig3data$Resistance,levels=res)
str(fig3data)

#Color palette
cbcolor <- c("#009E73","#D55E00","#0072B2")
cbfill <- c("dodgerblue3","darkorange2","green4","firebrick3")

#Subset data - AMR mutations only
mutonly<-subset(fig3data,Mutation!="none")

#Figure 3 plot
plotfig3<-ggplot(data=mutonly,aes(x=Mutation,y=scaledfit,fill=Environment))+
  theme_bw()+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+
  geom_abline(linewidth=0.5,linetype="dashed",color="darkgrey",aes(slope=0,intercept=1))+
  geom_boxplot(aes(fill=Environment),color="black",size=0.5,alpha=0.4,outlier.shape=NA)+
  geom_point(aes(color=Resistance),pch=16,size=2,alpha=.6,position = position_dodge(width=0.75))+
  scale_fill_manual(values=cbfill)+
  scale_color_manual(values=cbcolor)+
  labs(x="Mutation",y="Relative fitness")+
  scale_x_discrete(labels=c("gyrA_S83L_D87N" = "GyrA\n(S83L, D87N)", "gyrB_D426N" = "GyrB\n(D426N)","marR_R77H" = "MarR\n(R77H)",
                            "rpoB_H526Y" = "RpoB\n(H526Y)", "rpoB_S531L" = "RpoB\n(S531L)",
                            "rpsL_K43R" = "RpsL\n(K43R)", "rpsL_K43T" = "RpsL\n(K43T)"))+
  scale_y_continuous(breaks=c(0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3,1.4,1.5))+
  guides(fill=guide_legend(order=1,override.aes = list(shape = NA)),
         color=guide_legend(title="Mutation type"))+
  theme(legend.position = "right")+
  theme(axis.title.x = element_text(size=12,margin = margin(t = 0.25,unit="cm")))+
  theme(axis.title.y = element_text(size=12,margin = margin(r = 0.25,unit="cm")))+
  theme(axis.text.x = element_text(size=10))+
  theme(axis.text.y = element_text(size=10))
plotfig3

#Save as png
ggsave("Fig3-final.png", plot = plotfig3, dpi=1200,width = 9.06, height = 5.91, units = "in",bg='white')