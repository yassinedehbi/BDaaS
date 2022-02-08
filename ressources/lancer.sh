sh .profile
#hdfs namenode -format
#start-dfs.sh
#hdfs dfs -mkdir /input
#hdfs dfs -put datasample /input

#start-master.sh
#start-slaves.sh

#spark-submit --class ${APPNOM} --master spark://${MASTERIP}:7077 ${JARFILE}
# mkdir /home/ubuntu/result
#hdfs dfs -get /output/ /home/ubuntu/result
#tar -czvf /home/ubuntu/result.tar.gz /home/ubuntu/result
#scp