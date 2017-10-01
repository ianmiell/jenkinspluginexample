FROM centos:7
RUN yum install -y maven
ADD settings.xml /root/.m2/settings.xml
RUN mkdir -p /jenkinspluginexample
WORKDIR /jenkinspluginexample
RUN mvn -U org.jenkins-ci.tools:maven-hpi-plugin:create
