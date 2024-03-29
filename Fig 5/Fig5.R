library(ggplot2)
library(lme4)
library(tidyr)
library(ggpubr)

#Import data - Fitness of each AMR mutant relative to its ancestor in 4 growth environments
#Full dataset including technical replicate measures
finalcosts<-read.csv("Fig5-data.csv",na.strings = c("na"),header = T,sep = ",")
finalcosts$Replicate<-as.factor(finalcosts$Replicate)
str(finalcosts)

#The random effects model estimates fitness effects variance contributed by Genotype, Environment, and G x E interaction

#List of mutations
mutlist<-c("gyrA_S83L_D87N","gyrB_D426N","marR_R77H","rpoB_H526Y","rpoB_S531L","rpsL_K43R","rpsL_K43T")

#Loop through list of mutations, fit random effects model, extract variance components
random_model_output<-NULL
for(mut in mutlist){
  print(mut)
  modeldata<-subset(finalcosts,Mutation==mut) #Subset fitness effects data by mutation
  random_model<-lmer(scaledfit~1+(1|Ancestor)+(1|Environment)+(1|Ancestor:Environment),data=modeldata,REML=TRUE)
  output<-as.data.frame(VarCorr(random_model)) #Create a dataframe of the random effects with VarCorr
  #Change the names of vcov and sdcor columns to indicate mutation analyzed
  names(output)[names(output)=="vcov"]<-paste0("vcov_for_",mut)
  names(output)[names(output)=="sdcor"]<-paste0("sdcor_for_",mut)
  random_model_output[[mut]] <- output #Store the output dataframe as an object in a list
}
random_model_output

#Create summary dataframe of variance values
random_var<-data.frame(matrix(ncol=0,nrow=4))
for(obj in random_model_output){
  random_var<-cbind(random_var,obj[4]) #The 4th column is the vcov vector
}
random_var

#Restructure summary dataframe and calculate total variance and proportion explained by each factor

#Transpose dataframe
random_var<-t(random_var)
#Extract column titles from original random_model_output list
colnames(random_var)<-random_model_output[[1]][[1]]
#Convert matrix to dataframe and add 'Mutation' as factor
mut_var<-sub(".*_for_", "", dimnames(random_var)[[1]])
random_var<-as.data.frame(random_var)
random_var$Mutation<-as.factor(mut_var)
#Calculate total variance by summing the variances of each random effects term
random_var$Total_Var<-random_var$Ancestor+random_var$Environment+random_var$'Ancestor:Environment'+random_var$Residual
#Convert to long format
random_final <-gather(random_var, Factor, vcov,'Ancestor:Environment':Residual,factor_key=TRUE)
#Calculate proportion of variance explained (variance explained by each factor divided by total variance)
random_final$Proportion_of_Total<-random_final$vcov/random_final$Total_Var
#Recode factor levels
levels(random_final$Factor) <- list(Genotype  = "Ancestor", Environment = "Environment",'Genotype:Environment'="Ancestor:Environment",Residual="Residual")
random_final
str(random_final)

#Figure 5 Plot

#Color palette
cbcolor <- c("#CC79A7", "#D55E00","#0072B2","#F0E442")

#Figure 5A-Total Variance
plotfig5A<-ggplot()+
  theme_bw()+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+
  theme(plot.margin = unit(c(0.5,0.5,0.5,0.5), "cm"))+ #Creates space between plots
  geom_bar(aes(y = vcov, x = Mutation, fill = Factor), data = random_final,stat="identity")+
  scale_x_discrete(labels=c("gyrA_S83L_D87N" = "GyrA\n(S83L, D87N)", "gyrB_D426N" = "GyrB\n(D426N)","marR_R77H" = "MarR\n(R77H)",
                            "rpoB_H526Y" = "RpoB\n(H526Y)", "rpoB_S531L" = "RpoB\n(S531L)",
                            "rpsL_K43R" = "RpsL\n(K43R)", "rpsL_K43T" = "RpsL\n(K43T)"))+
  labs(x="Mutation",y="Variance Explained")+
  scale_y_continuous(limits=c(0,.031),breaks=c(0,0.01,0.02,0.03),labels=c(0,0.01,0.02,0.03))+
  scale_fill_manual(name="Factor",values=cbcolor)+
  theme(legend.text = element_text(size =  14),legend.title = element_text(size = 16))+
  theme(axis.title.x = element_text(size=14,margin = margin(t = 0.25,unit="cm")))+
  theme(axis.text.x = element_text(size=10))+
  theme(axis.title.y = element_text(size=14,margin = margin(r = 0.25,unit="cm")))+
  theme(axis.text.y = element_text(size=10))
plotfig5A

#Figure 5B-Proportion of Variance Explained
plotfig5B<-ggplot()+
  theme_bw()+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+
  theme(plot.margin = unit(c(0.5,0.5,0.5,0.5), "cm"))+ #Creates space between plots
  geom_bar(aes(y = Proportion_of_Total, x = Mutation, fill = Factor), data = random_final,stat="identity")+
  scale_x_discrete(labels=c("gyrA_S83L_D87N" = "GyrA\n(S83L, D87N)", "gyrB_D426N" = "GyrB\n(D426N)","marR_R77H" = "MarR\n(R77H)",
                            "rpoB_H526Y" = "RpoB\n(H526Y)", "rpoB_S531L" = "RpoB\n(S531L)",
                            "rpsL_K43R" = "RpsL\n(K43R)", "rpsL_K43T" = "RpsL\n(K43T)"))+
  labs(x="Mutation",y="Proportion of Variance Explained")+
  scale_y_continuous(limits=c(0,1),breaks=c(0,0.2,0.4,0.6,0.8,1),labels=c(0,0.2,0.4,0.6,0.8,1))+
  scale_fill_manual(name="Factor",values=cbcolor)+
  theme(legend.text = element_text(size =  14),legend.title = element_text(size = 16))+
  theme(axis.title.x = element_text(size=14,margin = margin(t = 0.25,unit="cm")))+
  theme(axis.text.x = element_text(size=10))+
  theme(axis.title.y = element_text(size=14,margin = margin(r=0.25,unit="cm")))+
  theme(axis.text.y = element_text(size=10))
plotfig5B

#Assemble panels into final figure
fig5final<-ggarrange(ggarrange(plotfig5A,plotfig5B,legend = c('right'),common.legend = TRUE,ncol = 2,nrow=1,font.label = list(size = 20),labels = c("A","B")))
fig5final

#Save as png
ggsave("Fig5-final.png", plot = fig5final, dpi=1200,width = 15.75, height = 5.91, units = "in",bg='white')
