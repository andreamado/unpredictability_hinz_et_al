library(ggplot2)
library(ggpubr)
library(lme4)
library(sjPlot)
library(report)

#Import data - MIC data for each mutant tested against three antibiotics in LB (full dataset)
micdata<-read.csv("MIC dataframe all.csv",na.strings = c("NA"),header = T,sep = ",")
micdata$log2_micfc<-log2(micdata$micfc) #log2 transformation

#Fig2 Dataframe - fold-changes for mutant relative to ancestor (median of 3 technical replicate measures)
#One value for each mutation x genetic background x antibiotic combination
fig2data<-aggregate(micfc ~ anc + mut + res + antibiotic, data = micdata, FUN = median)
fig2data$micfc_log2<-log2(fig2data$micfc) #log2 transformation
fig2legend<-read.csv("Fig2-legend.csv",na.strings = c("NA"),header = T,sep = ",") #Import legend file

#Color palette
cbcolor <- c("#009E73","#D55E00","#0072B2")

#Panel A-Fluoroquinolone resistance mutations
cipmuts<-subset(fig2data,res=="Fluoroquinolone")
plotfig2A<-ggplot(data=cipmuts,aes(x=mut,y=micfc_log2,fill=antibiotic,color=antibiotic))+
  theme_bw()+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+
  geom_abline(linewidth=0.5,linetype="dashed",color="darkgrey",aes(slope=0,intercept=0))+
  geom_vline(color="darkgrey",xintercept=seq(from=1.5,to=2.5,by=1))+
  geom_dotplot(binaxis='y',dotsize=1.1,alpha=1,stackdir='center',stackratio=1,position=position_dodge(0.85))+
  scale_y_continuous(limits=c(-2,6.8),
                     breaks=c(-2,-1,0,1,2,3,4,5,6),
                     labels=c(-2,"",0,"",2,"",4,"",6))+
  scale_x_discrete(labels=c("gyrA_S83L_D87N" = "GyrA\n(S83L, D87N)", "gyrB_D426N" = "GyrB\n(D426N)","marR_R77H" = "MarR\n(R77H)",
                            "rpoB_H526Y" = "RpoB\n(H526Y)", "rpoB_S531L" = "RpoB\n(S531L)",
                            "rpsL_K43R" = "RpsL\n(K43R)", "rpsL_K43T" = "RpsL\n(K43T)"))+
  scale_fill_manual(name="Antibiotic",values=cbcolor)+
  scale_color_manual(name="Antibiotic",values=cbcolor)+
  labs(y=bquote(paste(log[2],' (Fold change in MIC)')),x="Fluoroquinolone resistance mutations")+
  theme(legend.position="none")+
  theme(axis.title.x = element_text(size=14,margin = margin(t = 0.25,unit="cm")))+
  theme(axis.text.x = element_text(size=12))+
  theme(axis.title.y = element_text(size=14,margin = margin(t = 0.25,unit="cm")))+
  theme(axis.text.y = element_text(size=12))+
  theme(plot.margin = unit(c(0.5,0.5,0.5,1), "cm"))
plotfig2A

#Panel B-Rifampicin resistance mutations
rifmuts<-subset(fig2data,res=="Rifampicin")
plotfig2B<-ggplot(data=rifmuts,aes(x=mut,y=micfc_log2,fill=antibiotic,color=antibiotic))+
  theme_bw()+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+
  geom_abline(linewidth=0.5,linetype="dashed",color="darkgrey",aes(slope=0,intercept=0))+
  geom_vline(color="darkgrey",xintercept=1.5)+
  geom_dotplot(binaxis='y',dotsize=0.8,alpha=1,stackdir='center',stackratio=1,position=position_dodge(0.85))+
  scale_y_continuous(limits=c(-2,10),
                     breaks=c(-2,-1,0,1,2,3,4,5,6,7,8,9,10),
                     labels=c(-2,"",0,"",2,"",4,"",6,"",8,"",10))+
  scale_x_discrete(labels=c("gyrA_S83L_D87N" = "GyrA\n(S83L, D87N)", "gyrB_D426N" = "GyrB\n(D426N)","marR_R77H" = "MarR\n(R77H)",
                            "rpoB_H526Y" = "RpoB\n(H526Y)", "rpoB_S531L" = "RpoB\n(S531L)",
                            "rpsL_K43R" = "RpsL\n(K43R)", "rpsL_K43T" = "RpsL\n(K43T)"))+
  scale_fill_manual(name="Antibiotic",values=cbcolor)+
  scale_color_manual(name="Antibiotic",values=cbcolor)+
  labs(y=bquote(paste(log[2],' (Fold change in MIC)')),x="Rifampicin resistance mutations")+
  theme(legend.position="none")+
  theme(axis.title.x = element_text(size=14,margin = margin(t = 0.25,unit="cm")))+
  theme(axis.text.x = element_text(size=12))+
  theme(axis.title.y = element_text(size=14,margin = margin(t = 0.25,unit="cm")))+
  theme(axis.text.y = element_text(size=12))+
  theme(plot.margin = unit(c(0.5,0.5,0.5,1), "cm"))
plotfig2B

#Panel C-Aminoglycoside resistance mutations
strmuts<-subset(fig2data,res=="Aminoglycoside")
plotfig2C<-ggplot(data=strmuts,aes(x=mut,y=micfc_log2,fill=antibiotic,color=antibiotic))+
  theme_bw()+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+
  geom_abline(linewidth=0.5,linetype="dashed",color="darkgrey",aes(slope=0,intercept=0))+
  geom_vline(color="darkgrey",xintercept=1.5)+
  geom_dotplot(binaxis='y',dotsize=0.8,alpha=1,stackdir='center',stackratio=1,position=position_dodge(0.85))+
  scale_y_continuous(limits=c(-2,10),
                     breaks=c(-2,-1,0,1,2,3,4,5,6,7,8,9,10),
                     labels=c(-2,"",0,"",2,"",4,"",6,"",8,"",10))+
  scale_x_discrete(labels=c("gyrA_S83L_D87N" = "GyrA\n(S83L, D87N)", "gyrB_D426N" = "GyrB\n(D426N)","marR_R77H" = "MarR\n(R77H)",
                            "rpoB_H526Y" = "RpoB\n(H526Y)", "rpoB_S531L" = "RpoB\n(S531L)",
                            "rpsL_K43R" = "RpsL\n(K43R)", "rpsL_K43T" = "RpsL\n(K43T)"))+
  scale_fill_manual(name="Antibiotic",values=cbcolor)+
  scale_color_manual(name="Antibiotic",values=cbcolor)+
  labs(y=bquote(paste(log[2],' (Fold change in MIC)')),x="Aminoglycoside resistance mutations")+
  theme(legend.position="none")+
  theme(axis.title.x = element_text(size=14,margin = margin(t = 0.25,unit="cm")))+
  theme(axis.text.x = element_text(size=12))+
  theme(axis.title.y = element_text(size=14,margin = margin(t = 0.25,unit="cm")))+
  theme(axis.text.y = element_text(size=12))+
  theme(plot.margin = unit(c(0.5,0.5,0.5,1), "cm"))
plotfig2C

#Legend panel
legendpanel<-ggplot(data=fig2legend,aes(x=xdata,y=ydata,fill=Antibiotic,color=Antibiotic))+
  geom_dotplot(binaxis='y',dotsize=0,alpha=1,stackdir='center',stackratio=1,position=position_dodge(0.85))+
  scale_fill_manual(name="Antibiotic",values=cbcolor)+
  scale_color_manual(name="Antibiotic",values=cbcolor)+
  lims(x = c(0,1), y = c(0,1))+
  theme_void()+
  theme(legend.position = c(0.45,0.65),
        legend.key.size = unit(0.7, "cm"),
        legend.title.align=0.15,
        legend.text = element_text(size =  14),
        legend.title = element_text(size = 16))
legendpanel

#Assemble panels into figure
fig2final<-ggarrange(ggarrange(plotfig2A,legendpanel, widths=c(1,0.3),ncol = 2,font.label = list(size = 18),labels = c("A","")),
                ggarrange(plotfig2B,plotfig2C, widths=c(1,1),ncol = 2,font.label = list(size = 18),labels = c("B", "C")),
                nrow = 2,align="v",heights=c(0.8,1))+
  theme(plot.margin = unit(c(0.5,0.5,0.5,0.5), "cm"))
fig2final

#Save as png
ggsave("Fig2-final.png", plot = fig2final, dpi=1200,width = 13.78, height = 7.87, units = "in",bg='white')

######################
##### MIC Stats ######
######################

#Multiple comparisons T-test
#Tests whether resistance to tested antibiotics increases when considering all genetic backgrounds
#The t-test compares median MIC fold-change values of mutants to the ancestors
#A Bonferroni correction accounts for multiple comparisons
fcttest<-compare_means(method = "t.test",ref.group = "none",micfc_log2 ~ mut, data = fig2data,group.by="antibiotic",p.adjust.method="bonferroni")
fcttest
#RESULTS: When considering all genetic backgrounds, all mutations significantly increased the MIC of respective target antibiotics.
#There were no significant collateral effects.
#Streptomycin sensitivity of RpoB H526Y mutants is marginally significant with unadjusted p-value (p=0.027), but not with the Bonferroni corrected p-value (p=0.54).

#Mixed effects model
#Tests predictability of MIC fold-changes to target antibiotics based on knowledge of mutation
#The mixed effects model predicts MIC fold-change from mutation with genetic background and Mutation:Genetic background interaction as random effects
lmerdata<-subset(micdata,mut_effect=="direct") #subset the MIC data to include direct effects only
lmertest<-lmer(log2_micfc~mut+(1|anc)+(1|anc:mut),data=lmerdata,REML=TRUE)
summary(lmertest) #summary of results
tab_model(lmertest) #table of results
report(lmertest) #plain language report of results
#RESULTS: The model explained a substantial amount of the variance (Conditional R-squared = 0.985). 
#Most of the variance was explained by the fixed effect of 'Mutation' (Marginal R-squared = 0.888).
#The remaining explained variance (0.096) was explained by the random effects of Genetic background and Mutation:Genetic background interaction.
