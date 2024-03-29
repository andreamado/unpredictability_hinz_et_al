library(ggplot2)
library(ggpubr)

#Import data - MIC data for each mutant tested against three antibiotics in LB (full dataset)
micdata<-read.csv("MIC dataframe all.csv",na.strings = c("NA"),header = T,sep = ",")

#FigS1 Dataframe - fold-changes for mutant relative to ancestor (median of 3 technical replicate measures)
#One value for each mutation x genetic background x antibiotic combination
figS1data<-aggregate(micfc ~ anc + mut + antibiotic+ mut_effect + max_mic_median + mic_anc_median, data = micdata, FUN = median)
figS1data$log2anc<-log2(figS1data$mic_anc_median) #log2 transformation
figS1data$log2fc<-log2(figS1data$micfc) #log2 transformation
str(figS1data)

#Subset data - direct effects only
mutsub<-subset(figS1data,mut_effect=='direct')

#Fig S1 Panel A - Ciprofloxacin - MIC ancestor vs. MIC mutant
cipdata<-subset(mutsub,antibiotic=='Ciprofloxacin')
cipcolors <- c("dodgerblue3","darkorange2","green4")
plotfigS1A<-ggplot(data=cipdata,aes(x=log2anc,y=log2fc,fill=mut))+
  theme_bw()+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+
  theme(plot.margin = unit(c(0.5,0.5,0.5,0.5), "cm"))+ #Creates space between plots
  ggtitle("Ciprofloxacin")+
  scale_x_continuous(limits=c(-5.5,-4),
                     breaks=c(-6,-5.5,-5,-4.5,-4,-3.5,-3),
                     labels=c(-6,-5.5,-5,-4.5,-4,-3.5,-3))+
  scale_y_continuous(limits=c(-.2,6),
                     breaks=c(0,1,2,3,4,5,6),
                     labels=c(0,1,2,3,4,5,6))+
  scale_fill_manual(name="Mutation",values=cipcolors,labels=c("gyrA_S83L_D87N" = "GyrA (S83L, D87N)", "gyrB_D426N" = "GyrB (D426N)","marR_R77H" = "MarR (R77H)"))+
  scale_color_manual(name="Mutation",values=cipcolors,labels=c("gyrA_S83L_D87N" = "GyrA (S83L, D87N)", "gyrB_D426N" = "GyrB (D426N)","marR_R77H" = "MarR (R77H)"))+
  labs(x=bquote(paste(log[2],' (MIC of isolate)')),y=bquote(paste(log[2],' (Fold change in MIC)')),fill="Mutation",color="Mutation")+
  theme(legend.position = "right")+
  geom_jitter(pch=21,alpha=0.5,width=0.05,height=0.15,size=3.5)+
  geom_smooth(formula = y ~ x,method="lm", se=TRUE,alpha=0.15,aes(color=mut))+
  stat_cor(method="pearson",data=subset(cipdata,cipdata$mut=='gyrA_S83L_D87N'),aes(color = mut), label.x = -4.5,label.y = 5.8,show.legend = FALSE)+
  stat_cor(method="pearson",data=subset(cipdata,cipdata$mut=='gyrB_D426N'),aes(color = mut), label.x = -4.5,label.y = 3.1,show.legend = FALSE)+
  stat_cor(method="pearson",data=subset(cipdata,cipdata$mut=='marR_R77H'),aes(color = mut), label.x = -4.5,label.y = 2.5,show.legend = FALSE)
plotfigS1A

#Fig S1 Panel B - Rifampicin - MIC ancestor vs. MIC mutant
rifdata<-subset(mutsub,antibiotic=='Rifampicin')
rifcolors <- c("firebrick3","darkorchid")
plotfigS1B<-ggplot(data=rifdata,aes(x=log2anc,y=log2fc,fill=mut))+
  theme_bw()+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+
  theme(plot.margin = unit(c(0.5,0.5,0.5,0.5), "cm"))+ #Creates space between plots
  ggtitle("Rifampicin")+
  scale_x_continuous(limits=c(1.5,5),
                     breaks=c(1.5,2,2.5,3,3.5,4,4.5,5,5.5),
                     labels=c(1.5,2,2.5,3,3.5,4,4.5,5,5.5))+
  scale_y_continuous(limits=c(3.5,11.1),
                     breaks=c(4,5,6,7,8,9,10,11,12),
                     labels=c(4,5,6,7,8,9,10,11,12))+
  scale_fill_manual(name="Mutation",values=rifcolors,labels=c("rpoB_H526Y" = "RpoB (H526Y)", "rpoB_S531L" = "RpoB (S531L)"))+
  scale_color_manual(name="Mutation",values=rifcolors,labels=c("rpoB_H526Y" = "RpoB (H526Y)", "rpoB_S531L" = "RpoB (S531L)"))+
  scale_shape_manual(values=c(22,21))+
  labs(x=bquote(paste(log[2],' (MIC of isolate)')),y=bquote(paste(log[2],' (Fold change in MIC)')),fill="Mutation",color="Mutation")+
  theme(legend.position = "right")+
  guides(shape = 'none')+
  geom_jitter(aes(shape=max_mic_median),alpha=0.5,width=0.05,height=0.15,size=3.5)+
  geom_smooth(formula = y ~ x,method="lm", se=TRUE,alpha=0.15,aes(color=mut))+
  stat_cor(method="pearson",aes(color = mut), label.x = 3.6,label.y = NULL,show.legend = FALSE)
plotfigS1B

#Assemble panels into figure
figS1final<-ggarrange(ggarrange(plotfigS1A,plotfigS1B,ncol = 1,nrow=2,align='v',font.label = list(size = 18),labels = c("A","B")))
figS1final

#Save as png
ggsave("FigS1-final.png", plot = figS1final, dpi=1200,width = 18, height = 20, units = "cm",bg='white')
