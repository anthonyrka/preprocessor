#!/bin/awk -f
##
## file: typeVars.awk
## created by: R. Todd Jobe <toddjobe@unc.edu>
## date: 2009.05.25
## This script will print the variable names and types from a 
## columnar text file.
## Specifically, it can generate a variable declaration for GRASS 
## input.
{ 
    # Set the types to default values if not defined
    if(str=="") str="var"
    if(it=="") it="integer"
    if(dbl=="") dbl="double_precision"

    # Get the column name from the 1st row
    if(NR==1){
 for(i=1; i <= NF; i++){
     type[i,1]=$(i)
 }
    }else if(NR==2){

        # Get the column type from the 2nd row
 j=0
 for(i=1; i <= NF; i++){
     if($i ~ /[^-.0-9]/){
  type[i,2]=str
  strf[++j]=i
  if(str=="var"){
      max[i]=length($i)
      type[i,2]=sprintf("%s(%.0f)",str,max[i])
  }
     }else if($i ~ /\./){
  type[i,2]=dbl
     }else{
  type[i,2]=it
     }
 }
    }else{
        # Get the maximum column width for strings
 if(str=="var"){
     for( k in strf ){
  if(length($(k)) > max[k]) {
      max[k] = length ($k)
      type[strf[k],2]=sprintf("%s(%.0f)",str,max[k])
  }
     }
 }
    }
}
END{
    ORS=""
    out=sprintf("%s %s",type[1,1],type[1,2])
    for(l=2;l<i;l++){
 out=sprintf("%s, %s %s",out,type[l,1],type[l,2])
    }
    print out
}
