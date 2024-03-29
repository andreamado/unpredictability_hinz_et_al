library(ggplot2)
library(ggpubr)

#Import data - Summary statistics of fitness effects data
fig4data<-read.csv("Fig4-data.csv",na.strings = c("NA"),header = T,sep = ",")

#Reorder categorical variables
en<-c("LB","M9-Glucose","Urine","Colon")
fig4data$env<-factor(fig4data$env,levels=en)
str(fig4data)

#Color palette
envcolors <- c("dodgerblue3","darkorange2","green4","firebrick3")

#Panel A-Mean of fitness effects
meandata<-subset(fig4data,statistic=="mean")
plotfig4A<-ggplot(data=meandata,aes(x=env,y=value,fill=env))+
  theme_bw()+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+
  theme(legend.position="none")+
  theme(plot.margin = unit(c(0.5,0.5,0.5,0.5), "cm"))+ #Creates space between plots
  geom_abline(linewidth=0.5,linetype="solid",color="darkgrey",aes(slope=0,intercept=0))+
  geom_bar(stat='identity',width=0.75,alpha=0.75) +
  geom_text(aes(label = value), vjust = 3.5, size = 3,position = position_dodge(0.9))+
  geom_errorbar(aes(x=env, ymin=value+se, ymax=value-se),width=0.25)+
  scale_y_continuous(limits=c(-.15,.05),
                     breaks=c(-.2,-.15,-.1,-.05,0,0.05,.1,1.05,.2),
                     labels=c(-.2,-.15,-.1,-.05,0,0.05,.1,1.05,.2))+
  labs(x='Environment',y='Value')+
  scale_fill_manual(name="Environment",values=envcolors)+
  theme(legend.position = "none")+
  labs(x="Environment",y="Mean of fitness effects")+
  theme(axis.text.x = element_text())
plotfig4A

#Panel B-Variance of fitness effects
vardata<-subset(fig4data,statistic=="variance")
plotfig4B<-ggplot(data=vardata,aes(x=env,y=value,fill=env))+
  theme_bw()+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+
  theme(legend.position="none")+
  theme(plot.margin = unit(c(0.5,0.5,0.5,0.5), "cm"))+ #Creates space between plots
  geom_abline(linewidth=0.5,linetype="solid",color="darkgrey",aes(slope=0,intercept=0))+
  geom_bar(stat='identity',width=0.75,alpha=0.75) +
  geom_text(aes(label = value), vjust = -3.5, size = 3,position = position_dodge(0.9))+
  geom_errorbar(aes(x=env, ymin=value+se, ymax=value-se),width=0.25)+
  scale_y_continuous(limits=c(0,0.045),
                     breaks=c(0,0.01,0.02,0.03,0.04,0.05),
                     labels=c(0,0.01,0.02,0.03,0.04,0.05))+
  labs(x='Environment',y='Value')+
  scale_fill_manual(name="Environment",values=envcolors)+
  theme(legend.position = "none")+
  labs(x="Environment",y="Variance of fitness effects")+
  theme(axis.text.x = element_text())
plotfig4B

#Panel C-Gamma epistasis
gammadata<-subset(fig4data,statistic=="gamma")
plotfig4C<-ggplot(data=gammadata,aes(x=env,y=value,fill=env))+
  theme_bw()+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+
  theme(plot.margin = unit(c(0.5,0.5,0.5,0.5), "cm"))+ #Creates space between plots
  theme(legend.position="none")+
  geom_abline(linewidth=0.5,linetype="solid",color="darkgrey",aes(slope=0,intercept=0))+
  geom_bar(stat='identity',width=0.75,alpha=0.75) +
  geom_text(aes(label = value), vjust = -3.5, size = 3,position = position_dodge(0.9))+
  geom_errorbar(aes(x=env, ymin=value+se, ymax=value-se),width=0.25)+
  scale_y_continuous(limits=c(0,0.85),
                     breaks=c(0,0.2,0.4,0.6,0.8,1),
                     labels=c(0,0.2,0.4,0.6,0.8,1))+
  labs(x='Environment',y='Value')+
  scale_fill_manual(name="Environment",values=envcolors)+
  theme(legend.position = "none")+
  labs(x="Environment",y="Gamma epistasis")+
  theme(axis.text.x = element_text())
plotfig4C

#Assemble panels into figure
fig4final<-ggarrange(ggarrange(plotfig4A,plotfig4B,plotfig4C,ncol = 3,nrow=1,font.label = list(size = 18),labels = c("A","B","C")))
fig4final

#Save as png
ggsave("Fig4-final.png", plot = fig4final, dpi=1200,width = 9.84, height = 3.94, units = "in",bg='white')
