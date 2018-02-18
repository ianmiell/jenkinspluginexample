import shutit

s = shutit.create_session('bash',loglevel='info',echo=True)
s.login('docker run -p 19191:8080 -p 19292:8000 -ti ubuntu:16.04 bash')
# Java 8 required? See: https://stackoverflow.com/questions/32127424/java-nio-file-nosuchfileexception-and-java-io-eofexception-when-tring-to-build-j
s.install('locales')
s.install('openjdk-8-jdk')
s.install('maven')
s.install('vim')
s.send('mkdir -p /root/.m2')
s.send('export JAVA_HOME=/usr')
# Set the locale to avoid encoding errors
s.send('''sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen''')
s.send('locale-gen')
s.send('export LANG=en_US.UTF-8')
s.send('export LANGUAGE=en_US:en')
s.send('export LC_ALL=en_US.UTF-8')
s.send_file('/root/.m2/settings.xml','''<settings>
  <pluginGroups>
    <pluginGroup>org.jenkins-ci.tools</pluginGroup>
  </pluginGroups>
  <profiles>
    <!-- Give access to Jenkins plugins -->
    <profile>
      <id>jenkins</id>
      <activation>
        <activeByDefault>true</activeByDefault> 
          <!-- change this to false, if you don't like to have it on per default -->
      </activation>
      <repositories>
        <repository>
          <id>repo.jenkins-ci.org</id>
          <url>http://repo.jenkins-ci.org/public/</url>
        </repository>
      </repositories>
      <pluginRepositories>
        <pluginRepository>
          <id>repo.jenkins-ci.org</id>
          <url>http://repo.jenkins-ci.org/public/</url>
        </pluginRepository>
      </pluginRepositories>
    </profile>
  </profiles>
  <mirrors>
    <mirror>
      <id>repo.jenkins-ci.org</id>
      <url>http://repo.jenkins-ci.org/public/</url>
      <mirrorOf>m.g.o-public</mirrorOf>
    </mirror>
  </mirrors>
</settings>''')
s.send('mkdir -p /jenkinspluginexample')
s.send('cd /jenkinspluginexample')
s.multisend('mvn archetype:generate -Dfilter=io.jenkins.archetypes:',{'Choose archetype':'2',"""Define value for property 'artifactId'""":'imartifact1',"""Define value for property 'version'""":'','Y:':''})
s.send('cd imartifact1')
s.send('''export MAVEN_OPTS="-Xdebug -Xrunjdwp:transport=dt_socket,server=y,address=8000suspend=n"''')
s.send('mvn hpi:run')
s.pause_point('')
s.logout()

# TODO: mvnDebug hpi:run 
# and access on: localhost:8000
# If you examine the mvnDebug executable, you will see that it simply sets MAVEN_DEBUG_OPTS before running the normal mvn binary, as follows:
# MAVEN_DEBUG_OPTS="-Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=y,address=8000"
# echo Preparing to Execute Maven in Debug Mode
# env MAVEN_OPTS="$MAVEN_OPTS $MAVEN_DEBUG_OPTS" $(dirname $0)/mvn "$@"
