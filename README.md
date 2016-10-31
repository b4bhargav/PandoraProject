## Configuration and Deployment:

For configuration and installation, I have used Ansible. Ansible uses playbooks for deployment and installing requirements.
site.yml is the playbook to install Hadoop and Spark on hosts defined in inventory directory. It also clones the git repository
on all of the hosts.

## Loading file into HDFS:

We can use linux piping along with curl to pipe the data into HDFS. Below is the command.

`curl http://dumps.wikimedia.org/other/pagecounts-raw/2012/2012-01/pagecounts-20120101-000000.gz | fs -appendToFile - /user/bhargav/pagecounts-20120101-000000.gz`

##  Processing Framework:

I have used Spark as data processing framework. File spark/spark_job.py is pysprak scirpt which loads the input file into rdd and outputs
top 10 pages by language.

Below is the spark command to run the spark Job.

`/user/spark/latest/bin/spark-submit
--master yarn-client --deploy-mode client
--py-files /user/all/spark/SparkCode/spark_job.py
--i_input_path /user/bhargav/pagecounts-20120101-000000.gz
--o_output_path /user/bhargav/result`