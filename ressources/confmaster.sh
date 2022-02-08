wget http://sd-127206.dedibox.fr/hagimont/software/hadoop-2.7.1.tar.gz
wget http://sd-127206.dedibox.fr/hagimont/software/spark-2.4.3-bin-hadoop2.7.tgz
wget http://sd-127206.dedibox.fr/hagimont/software/jdk-8u221-linux-x64.tar.gz

tar xvzf hadoop-2.7.1.tar.gz
tar xvzf spark-2.4.3-bin-hadoop2.7.tgz
tar xvzf jdk-8u221-linux-x64.tar.gz

rm *.gz
rm *.tgz


export HADOOP_HOME=/home/ubuntu/hadoop-2.7.1 ;  echo HADOOP_HOME=$HADOOP_HOME ;
export SPARK_HOME=/home/ubuntu/spark-2.4.3-bin-hadoop2.7 ; echo SPARK_HOME=$SPARK_HOME ;
export JAVA_HOME=/home/ubuntu/jdk1.8.0_221 ; echo JAVA_HOME=$JAVA_HOME ;
export PATH=$JAVA_HOME/bin:$PATH
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$SPARK_HOME/bin:$SPARK_HOME/sbin ; echo PATH=$PATH ;
export HADOOP_CLASSPATH=$(find $HADOOP_HOME -name '*.jar' | xargs echo | tr ' ' ':')


# netsh wlan show profile name='' key=clear