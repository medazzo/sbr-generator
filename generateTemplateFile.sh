#!/bin/bash


generatedFile="easinTemplates.py"
WorkDirTemplates=".templates"
echo "# ----------------------------------------------- "  > $generatedFile
echo "# Generated Files  Containing temples as variables " >> $generatedFile
echo "# ----------------------------------------------- "  >> $generatedFile
echo "" >> $generatedFile
echo "templates = { ">> $generatedFile
for i in `ls $WorkDirTemplates`
do
  echo " adding file " $i
  content="$(cat $WorkDirTemplates/$i)"
  echo "    '$i' :  \"\"\"$content \"\"\"," >>  $generatedFile
done
 truncate -s-2  $generatedFile
 echo "}" >>  $generatedFile